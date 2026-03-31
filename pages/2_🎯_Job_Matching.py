"""
🎯 Job Matching Page
Uses RAG architecture to find best-fit jobs from Pinecone.
"""

import streamlit as st
from pathlib import Path
import plotly.graph_objects as go
import textwrap

# ── Page Config ─────────────────────────────────────────
st.set_page_config(page_title="Job Matching", page_icon="🎯", layout="wide")

from core.theme import init_theme
init_theme(current_page="Matching")

# ── Header ──────────────────────────────────────────────

st.markdown(
    """
<div style="margin-bottom: 1.5rem;">
    <h1 style="background: linear-gradient(135deg, #06b6d4, #10b981);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                font-weight: 800; font-size: 2rem;">
        🎯 Job Matching
    </h1>
    <p style="color: var(--text-secondary);">
        Semantic similarity matching using RAG architecture with Pinecone vector database.
    </p>
</div>
""",
    unsafe_allow_html=True,
)


# ── Check Prerequisites ────────────────────────────────
if "resume_profile" not in st.session_state:
    st.warning("⚠️ Please upload and analyze your resume first on the **Resume Analysis** page.")
    st.stop()

profile = st.session_state["resume_profile"]

st.markdown(
    f"""
    <div class="custom-card" style="padding: 1rem 1.25rem;">
        <span style="color: var(--text-secondary);">Matching for: </span>
        <span style="color: var(--text-primary); font-weight: 600;">{profile.name}</span>
        <span style="color: var(--text-secondary); opacity: 0.8;"> · {len(profile.all_skills_flat)} skills detected</span>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("")

# ── Controls ────────────────────────────────────────────
col_k, col_btn = st.columns([1, 2])
with col_k:
    top_k = st.slider("Number of matches", 1, 10, 5)
with col_btn:
    st.markdown("")
    run_match = st.button("🚀 Find Matching Jobs", use_container_width=True)


# ── Run Matching ────────────────────────────────────────
if run_match:
    with st.spinner("🔎 Searching Pinecone for matching jobs via RAG..."):
        try:
            from matching.rag_chain import match_resume_with_rag

            results = match_resume_with_rag(profile, top_k=top_k)
            st.session_state["match_results"] = results

            if results:
                st.success(f"✅ Found {len(results)} matching jobs!")
            else:
                st.warning("No matches found. Make sure the job database is initialized.")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


# ── Display Results ─────────────────────────────────────
if "match_results" in st.session_state and st.session_state["match_results"]:
    results = st.session_state["match_results"]

    st.markdown("---")

    # ── Score Overview Chart ──
    st.markdown('<div class="section-header">📊 Match Scores Overview</div>', unsafe_allow_html=True)

    titles = [f"{r.job.title}\n({r.job.company})" for r in results]
    scores = [r.score * 100 for r in results]
    colors = [
        "#10b981" if s >= 80 else "#f59e0b" if s >= 60 else "#f43f5e"
        for s in scores
    ]

    # Theme-aware colors for Plotly
    theme = st.session_state.get("theme", "Dark")
    chart_font_color = "#1e293b" if theme == "Light" else "#f8fafc"
    chart_grid_color = "rgba(0,0,0,0.15)" if theme == "Light" else "rgba(255,255,255,0.1)"

    fig = go.Figure(go.Bar(
        x=scores,
        y=titles,
        orientation="h",
        marker_color=colors,
        text=[f"{s:.0f}%" for s in scores],
        textposition="auto",
        textfont=dict(color="white", size=13, family="Inter"),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=chart_font_color, family="Inter"),
        xaxis=dict(
            title=dict(
                text="Match Score (%)",
                font=dict(color=chart_font_color, size=12)
            ),
            gridcolor=chart_grid_color,
            tickfont=dict(color=chart_font_color),
            range=[0, 105],
        ),
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(color=chart_font_color, size=11),
            title=dict(
                font=dict(color=chart_font_color, size=12)
            ),
        ),
        margin=dict(l=10, r=20, t=20, b=40),
        height=max(250, len(results) * 60),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Detailed Job Cards ──
    st.markdown("---")
    st.markdown('<div class="section-header">📋 Detailed Results</div>', unsafe_allow_html=True)

    for i, mr in enumerate(results):
        score_pct = mr.score * 100
        if score_pct >= 80:
            badge_class = "score-high"
            badge_label = "Strong Match"
        elif score_pct >= 60:
            badge_class = "score-medium"
            badge_label = "Good Match"
        else:
            badge_class = "score-low"
            badge_label = "Partial Match"

        with st.expander(
            f"#{i+1}  ·  {mr.job.title} at {mr.job.company}  ·  {score_pct:.0f}%",
            expanded=(i == 0),
        ):
            # Score badge
            st.markdown(
                f"""
<div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
    <span class="score-badge {badge_class}">{score_pct:.0f}% · {badge_label}</span>
    <span style="color: var(--text-secondary); font-size: 0.85rem;">📍 {mr.job.location}</span>
    <span style="color: var(--text-secondary); font-size: 0.85rem;">🏢 {mr.job.experience_level}</span>
</div>
""",
                unsafe_allow_html=True,
            )

            # Description
            st.markdown(f"**Description:** {mr.job.description}")
            st.markdown("")

            # Skills comparison
            scol1, scol2 = st.columns(2)

            with scol1:
                st.markdown("**✅ Matching Skills**")
                if mr.matching_skills:
                    match_tags = " ".join(
                        f'<span class="skill-tag match">{s}</span>'
                        for s in mr.matching_skills
                    )
                    st.markdown(match_tags, unsafe_allow_html=True)
                else:
                    st.caption("None detected")

            with scol2:
                st.markdown("**❌ Missing Skills**")
                if mr.missing_skills:
                    miss_tags = " ".join(
                        f'<span class="skill-tag missing">{s}</span>'
                        for s in mr.missing_skills
                    )
                    st.markdown(miss_tags, unsafe_allow_html=True)
                else:
                    st.caption("None — great match!")

            # Explanation
            if mr.explanation:
                st.markdown("")
                st.info(f"**AI Analysis:** {mr.explanation}")

    # ── Add Custom Job ──────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-header">➕ Add Custom Job Description</div>', unsafe_allow_html=True)

    with st.form("custom_job_form"):
        cj_title = st.text_input("Job Title")
        cj_company = st.text_input("Company")
        cj_desc = st.text_area("Job Description")
        cj_skills = st.text_input("Required Skills (comma separated)")
        cj_submitted = st.form_submit_button("Add & Match", use_container_width=True)

    if cj_submitted and cj_title and cj_desc:
        with st.spinner("Adding custom job and re-matching..."):
            try:
                from core.models import JobDescription
                from matching.matcher import ingest_custom_job

                custom_job = JobDescription(
                    title=cj_title,
                    company=cj_company or "Custom",
                    description=cj_desc,
                    required_skills=[s.strip() for s in cj_skills.split(",") if s.strip()],
                )
                job_id = ingest_custom_job(custom_job)
                st.success(f"✅ Custom job added (ID: {job_id}). Click 'Find Matching Jobs' to re-match!")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

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
    # Only one main action button here as Home is in the nav bar
    st.markdown('<div class="btn-premium">', unsafe_allow_html=True)
    if st.button("💡 Get Improvement Suggestions", use_container_width=True):
        st.switch_page("pages/3_💡_Improvements.py")
    st.markdown('</div>', unsafe_allow_html=True)
