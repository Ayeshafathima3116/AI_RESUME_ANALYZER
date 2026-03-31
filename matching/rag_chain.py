"""
RAG (Retrieval-Augmented Generation) chain.
Retrieves relevant job descriptions from Pinecone and uses Groq LLM
to generate intelligent match analysis and recommendations.
"""

import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from core.models import ResumeProfile, MatchResult, JobDescription
from vectordb.pinecone_manager import get_index, query_similar
from vectordb.embeddings import embed_text
import config


RAG_MATCH_PROMPT = """You are an expert career advisor and job matching specialist.

CANDIDATE PROFILE:
{resume_profile}

RETRIEVED JOB DESCRIPTIONS:
{job_descriptions}

Analyze how well the candidate matches each job. For each job, provide:
1. A match score from 0.0 to 1.0 (be realistic and precise)
2. Skills that match between the candidate and job
3. Skills the candidate is missing for this job
4. A brief explanation of why this is or isn't a good match

Return your analysis as valid JSON:
{{
  "matches": [
    {{
      "job_id": "the job id",
      "score": 0.85,
      "matching_skills": ["skill1", "skill2"],
      "missing_skills": ["skill3"],
      "explanation": "Brief explanation of the match quality"
    }}
  ]
}}

RULES:
- Be honest and accurate with scoring
- A score of 0.9+ means nearly perfect match
- A score of 0.7-0.89 means strong match with minor gaps
- A score of 0.5-0.69 means moderate match
- Below 0.5 means weak match
- Return ONLY valid JSON
"""


def match_resume_with_rag(profile: ResumeProfile, top_k: int = 5) -> list[MatchResult]:
    """
    Full RAG pipeline:
    1. Embed the resume profile
    2. Retrieve similar jobs from Pinecone
    3. Use Groq LLM to analyze matches in detail
    """
    # Step 1: Embed the resume
    resume_embedding = embed_text(profile.to_embedding_text())

    # Step 2: Retrieve similar jobs from Pinecone
    index = get_index()
    pinecone_results = query_similar(index, resume_embedding, top_k=top_k)

    if not pinecone_results:
        return []

    # Build job descriptions context from Pinecone metadata
    jobs_context = []
    job_map = {}
    for match in pinecone_results:
        meta = match.get("metadata", {})
        job_id = match.get("id", "")
        job = JobDescription(
            job_id=job_id,
            title=meta.get("title", ""),
            company=meta.get("company", ""),
            location=meta.get("location", ""),
            required_skills=json.loads(meta.get("required_skills", "[]")),
            preferred_skills=json.loads(meta.get("preferred_skills", "[]")),
            description=meta.get("description", ""),
            experience_level=meta.get("experience_level", ""),
        )
        job_map[job_id] = job
        jobs_context.append(
            f"Job ID: {job_id}\n"
            f"Title: {job.title} at {job.company}\n"
            f"Required Skills: {', '.join(job.required_skills)}\n"
            f"Preferred Skills: {', '.join(job.preferred_skills)}\n"
            f"Description: {job.description}\n"
            f"Experience Level: {job.experience_level}\n"
        )

    # Step 3: LLM analysis with RAG context
    llm = ChatGroq(
        model=config.GROQ_MODEL_NAME,
        api_key=config.GROQ_API_KEY,
        temperature=0,
        model_kwargs={"response_format": {"type": "json_object"}},
    )

    prompt = ChatPromptTemplate.from_template(RAG_MATCH_PROMPT)
    chain = prompt | llm

    response = chain.invoke({
        "resume_profile": profile.to_embedding_text(),
        "job_descriptions": "\n---\n".join(jobs_context),
    })

    data = json.loads(response.content)

    # Build MatchResult objects
    results = []
    for m in data.get("matches", []):
        job_id = m.get("job_id", "")
        if job_id in job_map:
            results.append(
                MatchResult(
                    job=job_map[job_id],
                    score=m.get("score", 0.0),
                    matching_skills=m.get("matching_skills", []),
                    missing_skills=m.get("missing_skills", []),
                    explanation=m.get("explanation", ""),
                )
            )

    # Sort by score descending
    results.sort(key=lambda r: r.score, reverse=True)
    return results


def match_single_jd(profile: ResumeProfile, job: JobDescription) -> MatchResult:
    """
    Directly match a single job description against a resume profile.
    No vector search needed.
    """
    llm = ChatGroq(
        model=config.GROQ_MODEL_NAME,
        api_key=config.GROQ_API_KEY,
        temperature=0,
        model_kwargs={"response_format": {"type": "json_object"}},
    )

    jobs_context = (
        f"Job ID: {job.job_id}\n"
        f"Title: {job.title} at {job.company}\n"
        f"Required Skills: {', '.join(job.required_skills)}\n"
        f"Preferred Skills: {', '.join(job.preferred_skills)}\n"
        f"Description: {job.description}\n"
        f"Experience Level: {job.experience_level}\n"
    )

    prompt = ChatPromptTemplate.from_template(RAG_MATCH_PROMPT)
    chain = prompt | llm

    response = chain.invoke({
        "resume_profile": profile.to_embedding_text(),
        "job_descriptions": jobs_context,
    })

    data = json.loads(response.content)
    
    # Extract the first match (since we only sent one)
    m = data.get("matches", [{}])[0]
    
    return MatchResult(
        job=job,
        score=m.get("score", 0.0),
        matching_skills=m.get("matching_skills", []),
        missing_skills=m.get("missing_skills", []),
        explanation=m.get("explanation", ""),
    )
