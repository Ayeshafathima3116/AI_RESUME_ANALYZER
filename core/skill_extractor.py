"""
Skill extraction from resume text using Groq LLM via LangChain.
Uses carefully engineered prompts with structured JSON output to extract
skills, experience, education, and other profile data.
"""

import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from core.models import ResumeProfile, SkillCategory, Experience, Education, Certification
import config


EXTRACTION_PROMPT = """You are an expert resume analyst and HR professional. 
Analyze the following resume text and extract structured information.

RESUME TEXT:
{resume_text}

Extract the following information and return it as valid JSON:

{{
  "name": "Full name of the candidate",
  "email": "Email address",
  "phone": "Phone number",
  "summary": "A 2-3 sentence professional summary based on the resume",
  "skills": [
    {{
      "category": "Category name (e.g., Programming Languages, Web Development, Machine Learning & AI, Cloud & DevOps, Databases, Data Science & Analytics, Soft Skills, Tools & Platforms)",
      "skills": ["skill1", "skill2"]
    }}
  ],
  "experience": [
    {{
      "title": "Job title",
      "company": "Company name",
      "duration": "Time period (e.g., Jan 2020 - Present)",
      "description": "Brief description of responsibilities and achievements"
    }}
  ],
  "education": [
    {{
      "degree": "Degree name",
      "institution": "University/College name",
      "year": "Year or period",
      "gpa": "GPA if mentioned, otherwise null"
    }}
  ],
  "certifications": [
    {{
      "name": "Certification name",
      "issuer": "Issuing organization",
      "year": "Year if mentioned, otherwise null"
    }}
  ]
}}

IMPORTANT RULES:
1. Extract ALL technical and soft skills mentioned, categorize them properly.
2. If a field is not found in the resume, use empty string "" or empty list [].
3. Be thorough — scan for skills in project descriptions, job duties, and summary.
4. Categorize skills accurately into the provided categories.
5. Return ONLY valid JSON, no additional text or markdown.
"""


def extract_profile(resume_text: str) -> ResumeProfile:
    """
    Extract a structured ResumeProfile from raw resume text using LLM.
    """
    llm = ChatGroq(
        model=config.GROQ_MODEL_NAME,
        api_key=config.GROQ_API_KEY,
        temperature=0,
        model_kwargs={"response_format": {"type": "json_object"}},
    )

    prompt = ChatPromptTemplate.from_template(EXTRACTION_PROMPT)
    chain = prompt | llm

    response = chain.invoke({"resume_text": resume_text})
    data = json.loads(response.content)

    # Build the ResumeProfile from extracted data
    profile = ResumeProfile(
        name=data.get("name", ""),
        email=data.get("email", ""),
        phone=data.get("phone", ""),
        summary=data.get("summary", ""),
        skills=[
            SkillCategory(category=s.get("category", ""), skills=s.get("skills", []))
            for s in data.get("skills", [])
        ],
        experience=[
            Experience(
                title=e.get("title", ""),
                company=e.get("company", ""),
                duration=e.get("duration", ""),
                description=e.get("description", ""),
            )
            for e in data.get("experience", [])
        ],
        education=[
            Education(
                degree=ed.get("degree", ""),
                institution=ed.get("institution", ""),
                year=ed.get("year", ""),
                gpa=ed.get("gpa"),
            )
            for ed in data.get("education", [])
        ],
        certifications=[
            Certification(
                name=c.get("name", ""),
                issuer=c.get("issuer", ""),
                year=c.get("year"),
            )
            for c in data.get("certifications", [])
        ],
        raw_text=resume_text,
    )

    return profile
