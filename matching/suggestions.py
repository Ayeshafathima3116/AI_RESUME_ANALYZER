"""
Resume improvement suggestion engine.
Uses Groq LLM with engineered prompts to provide actionable resume improvements.
"""

import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from core.models import ResumeProfile, MatchResult, Suggestion
import config


SUGGESTION_PROMPT = """You are an expert career coach, resume reviewer, and ATS (Applicant Tracking System) specialist.

CANDIDATE RESUME PROFILE:
{resume_profile}

TARGET JOB MATCHES AND GAPS:
{match_context}

Analyze the resume and provide detailed improvement suggestions. Consider:
1. **Skills Gap** — What skills should the candidate learn to be more competitive?
2. **Experience** — How can they better present their experience?
3. **Education & Certifications** — What certifications would boost their profile?
4. **Format & ATS** — How to optimize the resume for ATS systems?
5. **Content Quality** — How to improve descriptions, quantify achievements, use action verbs?

Return your suggestions as valid JSON:
{{
  "suggestions": [
    {{
      "category": "One of: Skills Gap, Experience, Education & Certifications, Format & ATS, Content Quality",
      "priority": "One of: High, Medium, Low",
      "title": "Short title for the suggestion",
      "description": "Detailed explanation of the suggestion",
      "action_items": [
        "Specific action item 1",
        "Specific action item 2"
      ]
    }}
  ]
}}

RULES:
- Provide 5-8 actionable suggestions
- At least 2 should be High priority
- Each action_item should be specific and actionable
- Focus on what will have the most impact
- Include ATS-specific keywords advice
- Return ONLY valid JSON
"""


def get_improvement_suggestions(
    profile: ResumeProfile,
    match_results: list[MatchResult] | None = None,
) -> list[Suggestion]:
    """
    Generate resume improvement suggestions using LLM.
    If match_results are provided, suggestions are tailored to target roles.
    """
    # Build match context
    if match_results:
        match_context_parts = []
        for mr in match_results[:3]:  # Top 3 matches
            match_context_parts.append(
                f"Job: {mr.job.title} at {mr.job.company}\n"
                f"  Match Score: {mr.score:.0%}\n"
                f"  Matching Skills: {', '.join(mr.matching_skills)}\n"
                f"  Missing Skills: {', '.join(mr.missing_skills)}\n"
            )
        match_context = "\n".join(match_context_parts)
    else:
        match_context = "No specific target jobs provided. Give general resume improvement advice."

    llm = ChatGroq(
        model=config.GROQ_MODEL_NAME,
        api_key=config.GROQ_API_KEY,
        temperature=0.3,
        model_kwargs={"response_format": {"type": "json_object"}},
    )

    prompt = ChatPromptTemplate.from_template(SUGGESTION_PROMPT)
    chain = prompt | llm

    response = chain.invoke({
        "resume_profile": profile.to_embedding_text(),
        "match_context": match_context,
    })

    data = json.loads(response.content)

    suggestions = [
        Suggestion(
            category=s.get("category", ""),
            priority=s.get("priority", "Medium"),
            title=s.get("title", ""),
            description=s.get("description", ""),
            action_items=s.get("action_items", []),
        )
        for s in data.get("suggestions", [])
    ]

    # Sort by priority: High > Medium > Low
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    suggestions.sort(key=lambda s: priority_order.get(s.priority, 1))

    return suggestions
