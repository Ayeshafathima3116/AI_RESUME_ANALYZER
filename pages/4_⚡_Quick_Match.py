"""
⚡ Quick Match — Direct JD Comparison Page
Directly compare your resume against a specific job description.
"""

import streamlit as st
from pathlib import Path
import json
import textwrap
from core.models import JobDescription, ResumeProfile
from matching.rag_chain import match_single_jd

# ── Page Config ─────────────────────────────────────────
st.set_page_config(page_title="Quick Match", page_icon="⚡", layout="wide")

from core.theme import init_theme
init_theme(current_page="Quick")

# ── Header ──────────────────────────────────────────────

st.markdown(
    """
<div style="margin-bottom: 2rem;">
    <h1 style="background: linear-gradient(135deg, #fba918, #f43f5e);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                font-weight: 800; font-size: 2.5rem; letter-spacing: -0.05em;">
        ⚡ Quick Match
    </h1>
    <p style="color: var(--text-secondary); font-size: 1.1rem;">
        Paste a job description below for an instant, targeted AI analysis of how your resume stacks up.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# ── Check Prerequisites ────────────────────────────────
if "resume_profile" not in st.session_state:
    st.markdown(
        """
        <div class="custom-card" style="border-color: var(--accent-rose); background: rgba(244, 63, 94, 0.05);">
            <h4 style="color: var(--accent-rose); margin-bottom: 0.5rem;">⚠️ Resume Missing</h4>
            <p style="color: var(--text-secondary);">Please upload and analyze your resume first to use the Quick Match feature.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("📄 Go to Resume Analysis", use_container_width=True):
        st.switch_page("pages/1_📄_Resume_Analysis.py")
    st.stop()

profile = st.session_state["resume_profile"]

# ── Layout ──────────────────────────────────────────────
col_input, col_results = st.columns([1, 1], gap="large")

with col_input:
    st.markdown('<div class="section-header">📋 Job Details</div>', unsafe_allow_html=True)
    
    with st.container(border=True):
        jd_title = st.text_input("Job Title", placeholder="e.g. Senior Software Engineer")
        jd_company = st.text_input("Company (Optional)", placeholder="e.g. Google")
        jd_text = st.text_area(
            "Job Description", 
            placeholder="Paste the full job description here...",
            height=400
        )
        
        analyze_btn = st.button("🚀 Analyze Match", use_container_width=True, type="primary")

if analyze_btn:
    if not jd_title or not jd_text:
        st.error("Please provide both a Job Title and Description.")
    else:
        with st.spinner("🧠 AI is performing laser-targeted analysis..."):
            try:
                # Build mock JobDescription
                job = JobDescription(
                    job_id="manual_match",
                    title=jd_title,
                    company=jd_company or "Target Company",
                    description=jd_text,
                    required_skills=[], # Will be extracted/analyzed by LLM
                    preferred_skills=[],
                    location="N/A",
                    experience_level="N/A"
                )
                
                result = match_single_jd(profile, job)
                st.session_state["direct_match_result"] = result
                st.success("✅ Analysis complete!")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

with col_results:
    st.markdown('<div class="section-header">📊 Analysis Results</div>', unsafe_allow_html=True)
    
    if "direct_match_result" in st.session_state:
        result = st.session_state["direct_match_result"]
        score_pct = result.score * 100
        
        if score_pct >= 80:
            badge_class = "score-high"
            badge_label = "Strong Match"
        elif score_pct >= 60:
            badge_class = "score-medium"
            badge_label = "Good Match"
        else:
            badge_class = "score-low"
            badge_label = "Partial Match"

        st.markdown(
            f"""
<div class="custom-card animate-fade-in">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
        <div>
            <h3 style="margin: 0; color: var(--text-primary);">{result.job.title}</h3>
            <p style="margin: 0; color: var(--text-secondary);">{result.job.company}</p>
        </div>
        <div class="score-badge {badge_class}" style="font-size: 1.2rem; padding: 12px 24px;">
            {score_pct:.0f}%
        </div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

        # Skills Breakout
        scol1, scol2 = st.columns(2)
        with scol1:
            st.markdown('<div style="color: var(--accent-emerald); font-weight: 700; margin-bottom: 0.5rem;">✅ Matching Skills</div>', unsafe_allow_html=True)
            if result.matching_skills:
                tags = " ".join(f'<span class="skill-tag match">{s}</span>' for s in result.matching_skills)
                st.markdown(tags, unsafe_allow_html=True)
            else:
                st.caption("No matching skills detected.")

        with scol2:
            st.markdown('<div style="color: var(--accent-rose); font-weight: 700; margin-bottom: 0.5rem;">❌ Missing Skills</div>', unsafe_allow_html=True)
            if result.missing_skills:
                tags = " ".join(f'<span class="skill-tag missing">{s}</span>' for s in result.missing_skills)
                st.markdown(tags, unsafe_allow_html=True)
            else:
                st.caption("No major gaps found.")

        st.markdown("---")
        
        # Action Items Section
        st.markdown('<div class="section-header" style="font-size: 1.2rem;">💡 Strategic Recommendations</div>', unsafe_allow_html=True)
        
        # If we have missing skills, provide specific advice
        if result.missing_skills:
            st.warning(f"**Top Gap:** To be more competitive, consider highlighting or acquiring: **{', '.join(result.missing_skills[:3])}**")
        
        # Action Buttons
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
        qcol1, qcol2 = st.columns(2)
        with qcol1:
            st.markdown('<div class="btn-premium">', unsafe_allow_html=True)
            if st.button("📈 Get Detailed Improvement Plan", use_container_width=True):
                st.session_state["match_results"] = [result]
                st.switch_page("pages/3_💡_Improvements.py")
            st.markdown('</div>', unsafe_allow_html=True)
        with qcol2:
            st.markdown('<div class="btn-premium">', unsafe_allow_html=True)
            if st.button("🔄 Reset Analysis", use_container_width=True):
                if "direct_match_result" in st.session_state:
                    del st.session_state["direct_match_result"]
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown(
            """
            <div style="text-align: center; padding: 4rem 2rem; color: var(--text-secondary); border: 1px dashed var(--border-color); border-radius: 16px; opacity: 0.7;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
                <p>Fill in the job details on the left and click <b>Analyze Match</b> to see your personalized results here.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ── Footer ──────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center; color: var(--text-secondary); font-size: 0.8rem; opacity: 0.6;">
        ⚡ Instant Resume-JD Correlation Powered by Groq & Llama 3
    </div>
    """,
    unsafe_allow_html=True,
)
