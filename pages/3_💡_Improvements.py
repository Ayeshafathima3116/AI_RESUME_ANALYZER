"""
💡 Resume Improvement Suggestions Page
AI-powered actionable suggestions to improve your resume.
"""

import streamlit as st
from pathlib import Path
import textwrap

# ── Page Config ─────────────────────────────────────────
st.set_page_config(page_title="Improvements", page_icon="💡", layout="wide")

from core.theme import init_theme
init_theme(current_page="Improve")


# ── Helper Functions (defined before use) ───────────────
def _render_suggestion(s):
    """Render a single suggestion card."""
    priority_class = f"priority-{s.priority.lower()}"

    with st.expander(f"{s.title}", expanded=(s.priority == "High")):
        st.markdown(
            f'<div style="margin-bottom: 1rem;">'
            f'<span class="{priority_class}">{s.priority} Priority</span>'
            f'<span class="category-tag">{s.category}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f'<p style="line-height: 1.6;">{s.description}</p>', unsafe_allow_html=True)

        if s.action_items:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div style="font-weight: 700; margin-bottom: 0.75rem; color: var(--text-primary);">🎯 Action Items:</div>', unsafe_allow_html=True)
            for item in s.action_items:
                st.markdown(
                    f'<div class="action-item">'
                    f'<span class="action-item-check">✓</span>'
                    f'<span>{item}</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )

# ── Header ──────────────────────────────────────────────
st.markdown(
    """
<div style="margin-bottom: 1.5rem;">
    <h1 style="background: linear-gradient(135deg, #f59e0b, #f43f5e);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                font-weight: 800; font-size: 2rem;">
        💡 Resume Improvements
    </h1>
    <p style="color: var(--text-secondary);">
        Get personalized, actionable suggestions to strengthen your resume and close skill gaps.
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
match_results = st.session_state.get("match_results", None)

# ── Context Banner ──
if match_results:
    st.markdown(
        f"""
<div class="custom-card" style="padding: 1rem 1.25rem;">
    <span style="color: var(--accent-emerald);">✅</span>
    <span style="color: var(--text-secondary);">
        Generating suggestions based on your profile and
        <b style="color: var(--text-primary);">{len(match_results)} job matches</b>.
    </span>
</div>
""",
        unsafe_allow_html=True,
    )
else:
    st.info("💡 For tailored suggestions, run **Job Matching** first. Otherwise, you'll get general improvement advice.")

st.markdown("")


# ── Generate Suggestions ───────────────────────────────
if st.button("🧠 Generate Improvement Suggestions", use_container_width=True):
    with st.spinner("🤔 AI is crafting personalized suggestions..."):
        try:
            from matching.suggestions import get_improvement_suggestions

            suggestions = get_improvement_suggestions(profile, match_results)
            st.session_state["suggestions"] = suggestions
            st.success(f"✅ Generated {len(suggestions)} suggestions!")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


# ── Display Suggestions ────────────────────────────────
if "suggestions" in st.session_state:
    suggestions = st.session_state["suggestions"]

    st.markdown("---")

    # ── Summary Metrics ──
    high = sum(1 for s in suggestions if s.priority == "High")
    medium = sum(1 for s in suggestions if s.priority == "Medium")
    low = sum(1 for s in suggestions if s.priority == "Low")

    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    mcol1.metric("Total Suggestions", len(suggestions))
    mcol2.metric("🔴 High Priority", high)
    mcol3.metric("🟡 Medium Priority", medium)
    mcol4.metric("🔵 Low Priority", low)

    st.markdown("---")

    # ── Category Tabs ──
    categories = list(set(s.category for s in suggestions))
    if categories:
        tabs = st.tabs(["📋 All"] + [f"{'🔴' if c == 'Skills Gap' else '🟡' if c == 'Content Quality' else '🔵'} {c}" for c in categories])

        # All tab
        with tabs[0]:
            for s in suggestions:
                _render_suggestion(s)

        # Category tabs
        for i, cat in enumerate(categories):
            with tabs[i + 1]:
                cat_suggestions = [s for s in suggestions if s.category == cat]
                for s in cat_suggestions:
                    _render_suggestion(s)

    # ── Skill Gap Analysis Visual ──
    if match_results:
        st.markdown("---")
        st.markdown('<div class="section-header">📊 Skill Gap Analysis</div>', unsafe_allow_html=True)

        # Collect all matching and missing skills
        all_matching = set()
        all_missing = set()
        for mr in match_results[:5]:
            all_matching.update(mr.matching_skills)
            all_missing.update(mr.missing_skills)

        # Remove skills that appear in both
        only_missing = all_missing - all_matching

        gcol1, gcol2 = st.columns(2)

        with gcol1:
            st.markdown("**✅ Your Strong Skills**")
            if all_matching:
                tags = " ".join(f'<span class="skill-tag match">{s}</span>' for s in sorted(all_matching))
                st.markdown(tags, unsafe_allow_html=True)
            else:
                st.caption("No matching skills detected")

        with gcol2:
            st.markdown("**🎯 Skills to Acquire**")
            if only_missing:
                tags = " ".join(f'<span class="skill-tag missing">{s}</span>' for s in sorted(only_missing))
                st.markdown(tags, unsafe_allow_html=True)
            else:
                st.caption("Great — no major skill gaps!")

        # Progress indicator
        if all_matching or only_missing:
            total = len(all_matching) + len(only_missing)
            coverage = len(all_matching) / total if total > 0 else 0
            st.markdown("")
            st.markdown(f"**Skill Coverage: {coverage:.0%}**")
            st.progress(coverage)

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
    # Only the "Analyze Another Resume" button is needed here
    st.markdown('<div class="btn-premium">', unsafe_allow_html=True)
    if st.button("📄 Analyze Another Resume", use_container_width=True):
        # Clear session state
        for key in list(st.session_state.keys()):
            if key != "db_initialized":
                del st.session_state[key]
        st.switch_page("pages/1_📄_Resume_Analysis.py")
    st.markdown('</div>', unsafe_allow_html=True)


