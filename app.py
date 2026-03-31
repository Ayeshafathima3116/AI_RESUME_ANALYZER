"""
AI-Powered Resume Analyzer & Job Matcher
Main Streamlit application — Dashboard home page.
"""

import streamlit as st
from pathlib import Path
import config
import textwrap
from core.theme import init_theme

# ── Page Config ─────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Theme & Custom CSS ──────────────────────────────────
init_theme(current_page="Home", show_nav=False)


# ── Main Dashboard ──────────────────────────────────────
st.markdown("""<style>
    [data-testid="stAppViewBlockContainer"] { max-width: 1200px; }
</style>""", unsafe_allow_html=True)

st.markdown(
    """
<div style="text-align: center; padding: 4rem 1rem; margin-bottom: 2rem;">
    <div class="ai-badge">Powered by AI & RAG Technology</div>
    <h1 style="font-size: 4rem; font-weight: 800; margin-bottom: 1.5rem; line-height: 1.1;">
        <span style="background: linear-gradient(135deg, #60a5fa, #34d399); 
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            AI Resume Analyzer
        </span><br>
        <span style="color: var(--text-primary); -webkit-text-fill-color: var(--text-primary);">
            & Job Matcher
        </span>
    </h1>
    <p style="color: var(--text-secondary); font-size: 1.25rem; max-width: 800px; margin: 0 auto 2.5rem; line-height: 1.6;">
        Upload your resume and let our AI-powered system analyze your skills, 
        match you with the best job opportunities, and suggest improvements — all in seconds.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# Center the CTA button
_, c_btn, _ = st.columns([1, 1.5, 1])
with c_btn:
    if st.button("🚀 Get Started", use_container_width=True):
        st.switch_page("pages/1_📄_Resume_Analysis.py")

st.markdown("---")

# ── Feature Cards ───────────────────────────────────────
def feature_card(icon, title, desc, slug, is_featured=False):
    featured_class = "featured-card" if is_featured else ""
    st.markdown(f"""
<a href="/{slug}" target="_self" style="text-decoration: none; color: inherit; display: block;">
<div class="custom-card {featured_class}" style="cursor: pointer;">
    <div style="font-size: 3rem; margin-bottom: 1.25rem;">{icon}</div>
    <h3 style="color: var(--text-primary); font-weight: 700; margin-bottom: 0.75rem; font-size: 1.5rem;">{title}</h3>
    <p style="color: var(--text-secondary); font-size: 1rem; line-height: 1.5;">{desc}</p>
</div>
</a>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")
with col1:
    feature_card("📄", "Resume Analysis", "Upload your resume and get instant AI-powered skill extraction.", "Resume_Analysis")
with col2:
    feature_card("🎯", "Job Matching", "Semantic correlation matching using RAG architecture.", "Job_Matching")

# Row 2: Improvements & Quick Match
c3, c4 = st.columns(2, gap="large")
with c3:
    feature_card("💡", "Improvements", "Get personalized suggestions to optimize your resume for better visibility.", "Improvements")
with c4:
    feature_card("⚡", "Quick Match", "Instant compatibility scoring — paste a job description and see how well you fit.", "Quick_Match", is_featured=True)

# ── How It Works ────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<h2 style="text-align: center; font-weight: 800; background: linear-gradient(90deg, #60a5fa, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.25rem; margin-bottom: 2rem;">How It Works</h2>', unsafe_allow_html=True)

timeline_html = """
<div class="timeline-container">
    <div class="timeline-line"></div>
    <div class="timeline-step">
        <div class="step-number">1</div>
        <div class="step-title">Upload Resume</div>
        <div class="step-desc">Upload your resume in PDF or text format</div>
    </div>
    <div class="timeline-step">
        <div class="step-number">2</div>
        <div class="step-title">AI Analysis</div>
        <div class="step-desc">Our AI extracts skills, experience & entities</div>
    </div>
    <div class="timeline-step">
        <div class="step-number">3</div>
        <div class="step-title">Vector Embedding</div>
        <div class="step-desc">Resume is converted to semantic vectors</div>
    </div>
    <div class="timeline-step">
        <div class="step-number">4</div>
        <div class="step-title">RAG Matching</div>
        <div class="step-desc">Retrieval-augmented matching against jobs</div>
    </div>
    <div class="timeline-step">
        <div class="step-number">5</div>
        <div class="step-title">Get Results</div>
        <div class="step-desc">Receive matches, scores & improvement tips</div>
    </div>
</div>"""
st.markdown(timeline_html, unsafe_allow_html=True)

# ── Footer ──────────────────────────────────────────────
st.markdown("---")
st.markdown(
    textwrap.dedent("""
        <div style="text-align: center; padding: 1rem; color: var(--text-muted); font-size: 0.8rem;">
            Built with ❤️ using Groq, HuggingFace, Pinecone & Streamlit &nbsp;·&nbsp;
            AI-Powered Resume Analyzer & Job Matcher
        </div>
    """),
    unsafe_allow_html=True,
)
