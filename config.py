"""
Central configuration module.
Loads environment variables and provides project-wide settings.
"""

import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def get_secret(key, default=""):
    """Helper to get secret from Streamlit or environment."""
    try:
        if key in st.secrets:
            return st.secrets[key]
    except:
        pass
    return os.getenv(key, default)

# ── Groq (Free LLM) ──────────────────────────────────────
GROQ_API_KEY = get_secret("GROQ_API_KEY")
GROQ_MODEL_NAME = get_secret("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")

# ── HuggingFace (Free Embeddings) ────────────────────────
HF_EMBEDDING_MODEL = get_secret("HF_EMBEDDING_MODEL", "all-MiniLM-L6-v2")
EMBEDDING_DIMENSION = 384  # dimension for all-MiniLM-L6-v2

# ── Pinecone ────────────────────────────────────────────
PINECONE_API_KEY = get_secret("PINECONE_API_KEY")
PINECONE_INDEX_NAME = get_secret("PINECONE_INDEX_NAME", "resume-analyzer-free")
PINECONE_CLOUD = "aws"
PINECONE_REGION = "us-east-1"

# ── App Settings ────────────────────────────────────────
MAX_FILE_SIZE_MB = 10
SUPPORTED_FILE_TYPES = ["pdf", "docx"]
TOP_K_MATCHES = 5

# ── Skill Categories ───────────────────────────────────
SKILL_CATEGORIES = [
    "Programming Languages",
    "Web Development",
    "Machine Learning & AI",
    "Cloud & DevOps",
    "Databases",
    "Data Science & Analytics",
    "Mobile Development",
    "Soft Skills",
    "Tools & Platforms",
    "Certifications",
]


def validate_config():
    """Check that required API keys are set and look valid."""
    missing = []
    
    # Check Groq Key
    if not GROQ_API_KEY:
        missing.append("GROQ_API_KEY is missing")
    elif not GROQ_API_KEY.startswith("gsk_"):
        missing.append("GROQ_API_KEY is invalid (must start with 'gsk_')")
        
    # Check Pinecone Key
    if not PINECONE_API_KEY:
        missing.append("PINECONE_API_KEY is missing")
    elif not PINECONE_API_KEY.startswith("pcsk_"):
         # Some pinecone keys are just uuid-like, but premium/serverless ones usually have a prefix
         # Let's just check for non-empty for now unless we're sure
         pass

    return missing
