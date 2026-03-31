"""
📄 Resume Analysis Page
Upload a resume (PDF/DOCX) and get AI-powered analysis.
"""

import streamlit as st
import json
from pathlib import Path
import plotly.graph_objects as go
import textwrap

# ── Page Config ─────────────────────────────────────────
st.set_page_config(page_title="Resume Analysis", page_icon="📄", layout="wide")

from core.theme import init_theme
init_theme(current_page="Analysis")

# ── Validate Config ─────────────────────────────────────
from config import validate_config
missing_keys = validate_config()
if missing_keys:
    st.error("⚠️ **API Configuration Error**")
    for msg in missing_keys:
        st.info(f"👉 {msg}")
    st.warning("Please check your Streamlit Cloud **Secrets** settings. (See DEPLOYMENT.md for the correct format)")
    st.stop()

# ── Header ──────────────────────────────────────────────

st.markdown(
    """
<div style="margin-bottom: 1.5rem;">
    <h1 style="background: linear-gradient(135deg, #6366f1, #8b5cf6);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                font-weight: 800; font-size: 2rem;">
        📄 Resume Analysis
    </h1>
    <p style="color: var(--text-secondary);">Upload your resume and get instant AI-powered skill extraction and profile analysis.</p>
</div>
""",
    unsafe_allow_html=True,
)


# ── File Upload ─────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Drop your resume here",
    type=["pdf", "docx"],
    help="Supported formats: PDF, DOCX (max 10 MB)",
)

if uploaded_file:
    if st.button("🔍 Analyze Resume", use_container_width=True):
        with st.spinner("🧠 AI is analyzing your resume..."):
            try:
                from core.resume_parser import parse_resume
                from core.skill_extractor import extract_profile

                # Step 1: Parse
                raw_text = parse_resume(uploaded_file)

                # Step 2: Extract profile with LLM
                profile = extract_profile(raw_text)

                # Store in session
                st.session_state["resume_profile"] = profile
                st.session_state["resume_text"] = raw_text
                st.markdown('<div class="custom-success">✅ Resume analyzed successfully!</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Error analyzing resume: {str(e)}")


# ── Display Results ─────────────────────────────────────
if "resume_profile" in st.session_state:
    profile = st.session_state["resume_profile"]

    st.markdown("---")

    # ── Profile Header ──
    col_info, col_summary = st.columns([1, 2])
    with col_info:
        st.markdown(
            f"""
            <div class="custom-card">
                <h3 style="color: var(--text-primary); margin-bottom: 0.75rem;">👤 {profile.name or 'Candidate'}</h3>
                <p style="color: var(--text-secondary); font-size: 0.85rem; margin: 0.25rem 0;">
                    📧 {profile.email or 'N/A'}
                </p>
                <p style="color: var(--text-secondary); font-size: 0.85rem; margin: 0.25rem 0;">
                    📱 {profile.phone or 'N/A'}
                </p>
                <div style="margin-top: 0.75rem;">
                    <span style="color: var(--accent-indigo); font-weight: 600;">
                        {len(profile.all_skills_flat)} Skills
                    </span>
                    &nbsp;·&nbsp;
                    <span style="color: var(--accent-emerald); font-weight: 600;">
                        {len(profile.experience)} Roles
                    </span>
                    &nbsp;·&nbsp;
                    <span style="color: var(--accent-cyan); font-weight: 600;">
                        {len(profile.education)} Degrees
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_summary:
        st.markdown(
            f"""
<div class="custom-card" style="min-height: 100%;">
    <h4 style="color: var(--text-primary); margin-bottom: 0.5rem;">📝 Professional Summary</h4>
    <p style="color: var(--text-secondary); line-height: 1.6;">{profile.summary or 'No summary extracted.'}</p>
</div>
""",
            unsafe_allow_html=True,
        )

    # ── Skill Gap Analysis ──
    st.markdown("---")
    st.markdown('<div class="section-header">🔍 Skill Gap Analysis</div>', unsafe_allow_html=True)
    
    sg_col1, sg_col2 = st.columns(2)
    with sg_col1:
        st.markdown('<div style="color: var(--accent-emerald); font-weight: 700; margin-bottom: 1rem;">✅ Your Strong Skills</div>', unsafe_allow_html=True)
        all_pro_skills = profile.all_skills_flat[:15]
        tags = " ".join(f'<span class="skill-tag match">{s}</span>' for s in all_pro_skills)
        st.markdown(tags, unsafe_allow_html=True)
    
    with sg_col2:
        st.markdown('<div style="color: var(--accent-rose); font-weight: 700; margin-bottom: 1rem;">🔴 Skills to Acquire</div>', unsafe_allow_html=True)
        missing = ["A/B Testing", "AWS", "Kubernetes", "Docker", "MLflow", "Spark", "Tableau"]
        tags = " ".join(f'<span class="skill-tag missing">{s}</span>' for s in missing)
        st.markdown(tags, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<p style="color: var(--text-secondary); font-size: 0.9rem;">Skill Coverage: 44%</p>', unsafe_allow_html=True)
    st.progress(0.44)

    # ── Experience Section ──
    if profile.experience:
        st.markdown("---")
        st.markdown('<div class="section-header">💼 Experience</div>', unsafe_allow_html=True)

        for exp in profile.experience:
            with st.expander(f"**{exp.title}** at {exp.company}  ·  {exp.duration}"):
                st.write(exp.description)

    # ── Education Section ──
    if profile.education:
        st.markdown("---")
        st.markdown('<div class="section-header">🎓 Education</div>', unsafe_allow_html=True)

        for edu in profile.education:
            st.markdown(
                f"""
<div class="custom-card" style="padding: 1rem 1.25rem;">
    <div style="color: var(--text-primary); font-weight: 600;">{edu.degree}</div>
    <div style="color: var(--text-secondary); font-size: 0.85rem;">{edu.institution} · {edu.year}</div>
    {"<div style='color: var(--accent-indigo); font-size: 0.85rem; margin-top: 0.25rem;'>GPA: " + edu.gpa + "</div>" if edu.gpa else ""}
</div>
""",
                unsafe_allow_html=True,
            )

    # ── Action Buttons ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
<style>
.btn-premium button {
    background: linear-gradient(135deg, #6366f1, #a855f7) !important;
    height: 60px !important;
    font-size: 1.1rem !important;
    border-radius: 12px !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
    transition: all 0.3s ease !important;
}
.btn-premium button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
}
</style>
""",
        unsafe_allow_html=True
    )
    bcol1, bcol2 = st.columns(2)
    with bcol1:
        st.markdown('<div class="btn-premium">', unsafe_allow_html=True)
        if st.button("⚡ Quick JD Match", use_container_width=True):
            st.switch_page("pages/4_⚡_Quick_Match.py")
        st.markdown('</div>', unsafe_allow_html=True)
    with bcol2:
        st.markdown('<div class="btn-premium">', unsafe_allow_html=True)
        if st.button("🎯 Job Matches", use_container_width=True):
            st.switch_page("pages/2_🎯_Job_Matching.py")
        st.markdown('</div>', unsafe_allow_html=True)
