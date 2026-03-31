"""
Pydantic v2 data models for the Resume Analyzer application.
"""

from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional


# ── Resume Models ───────────────────────────────────────


class Experience(BaseModel):
    title: str = ""
    company: str = ""
    duration: str = ""
    description: str = ""


class Education(BaseModel):
    degree: str = ""
    institution: str = ""
    year: str = ""
    gpa: Optional[str] = None


class Certification(BaseModel):
    name: str = ""
    issuer: str = ""
    year: Optional[str] = None


class SkillCategory(BaseModel):
    category: str = ""
    skills: list[str] = Field(default_factory=list)


class ResumeProfile(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""
    summary: str = ""
    skills: list[SkillCategory] = Field(default_factory=list)
    experience: list[Experience] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    certifications: list[Certification] = Field(default_factory=list)
    raw_text: str = ""

    @property
    def all_skills_flat(self) -> list[str]:
        """Return a flat list of all skills across categories."""
        return [s for cat in self.skills for s in cat.skills]

    def to_embedding_text(self) -> str:
        """Convert profile to a single text string for embedding."""
        parts = []
        if self.summary:
            parts.append(f"Summary: {self.summary}")
        if self.all_skills_flat:
            parts.append(f"Skills: {', '.join(self.all_skills_flat)}")
        for exp in self.experience:
            parts.append(f"Experience: {exp.title} at {exp.company} ({exp.duration}). {exp.description}")
        for edu in self.education:
            parts.append(f"Education: {edu.degree} from {edu.institution} ({edu.year})")
        for cert in self.certifications:
            parts.append(f"Certification: {cert.name} by {cert.issuer}")
        return "\n".join(parts)


# ── Job Models ──────────────────────────────────────────


class JobDescription(BaseModel):
    job_id: str = ""
    title: str = ""
    company: str = ""
    location: str = ""
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    description: str = ""
    experience_level: str = ""

    def to_embedding_text(self) -> str:
        """Convert job description to a text string for embedding."""
        parts = [
            f"Job Title: {self.title}",
            f"Company: {self.company}",
            f"Description: {self.description}",
            f"Required Skills: {', '.join(self.required_skills)}",
            f"Preferred Skills: {', '.join(self.preferred_skills)}",
            f"Experience Level: {self.experience_level}",
        ]
        return "\n".join(parts)


# ── Match & Suggestion Models ──────────────────────────


class MatchResult(BaseModel):
    job: JobDescription
    score: float = 0.0
    matching_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    explanation: str = ""


class Suggestion(BaseModel):
    category: str = ""
    priority: str = "Medium"  # High / Medium / Low
    title: str = ""
    description: str = ""
    action_items: list[str] = Field(default_factory=list)
