import streamlit as st
from pathlib import Path

# Navigation steps definition
NAV_STEPS = [
    {"icon": "🏠", "label": "Home",     "slug": "/"},
    {"icon": "📄", "label": "Analysis", "slug": "/Resume_Analysis"},
    {"icon": "🎯", "label": "Matching", "slug": "/Job_Matching"},
    {"icon": "💡", "label": "Improve",  "slug": "/Improvements"},
    {"icon": "⚡", "label": "Quick",    "slug": "/Quick_Match"},
]

def init_theme(current_page="Home", show_nav=True):
    """
    Initializes theme, renders the top navigation timeline, and injects CSS.
    current_page: one of "Home", "Analysis", "Matching", "Improve", "Quick"
    show_nav: whether to display the top navigation bar
    """
    # ── Theme persistence ───────────────────────────────
    if "theme" in st.query_params:
        st.session_state["theme"] = st.query_params["theme"]
    if "theme" not in st.session_state:
        st.session_state["theme"] = "Dark"

    # ── Hide sidebar entirely ───────────────────────────
    st.markdown("""<style>
        section[data-testid="stSidebar"] { display: none !important; }
        [data-testid="stSidebarCollapsedControl"] { display: none !important; }
        [data-testid="stAppViewBlockContainer"] { max-width: 1200px; }
    </style>""", unsafe_allow_html=True)

    # ── Top Navigation Bar with Timeline + Theme Toggle ─
    if show_nav:
        _render_nav_bar(current_page)
    else:
        # Still need the theme toggle even if nav is hidden
        _render_theme_toggle_only()

    # ── Inject CSS ──────────────────────────────────────
    _inject_theme_css(st.session_state["theme"])


def _render_nav_bar(current_page):
    """Renders the horizontal navigation timeline and theme toggle."""
    current_theme = st.session_state["theme"]
    theme_icon = "🌙" if current_theme == "Light" else "☀️"
    is_light = current_theme == "Light"

    # Build the timeline HTML
    steps_html = ""
    for step in NAV_STEPS:
        is_active = step["label"] == current_page
        active_class = "nav-step-active" if is_active else ""
        steps_html += f'''
        <a href="{step['slug']}" target="_self" class="nav-step {active_class}">
            <div class="nav-step-icon">{step['icon']}</div>
            <div class="nav-step-label">{step['label']}</div>
        </a>'''

    # Colors adapt based on theme
    bg_steps = "rgba(0,0,0,0.03)" if is_light else "rgba(255,255,255,0.04)"
    border_steps = "rgba(0,0,0,0.06)" if is_light else "rgba(255,255,255,0.08)"
    connector_color = "rgba(0,0,0,0.1)" if is_light else "rgba(255,255,255,0.1)"
    label_color = "rgba(0,0,0,0.4)" if is_light else "rgba(255,255,255,0.5)"
    label_hover = "#1e293b" if is_light else "rgba(255,255,255,0.9)"
    active_bg = "rgba(79,70,229,0.08)" if is_light else "rgba(99,102,241,0.15)"
    active_label = "#4f46e5" if is_light else "#a5b4fc"

    # Self-contained HTML + CSS component
    nav_component = f'''
    <style>
    .nav-timeline-bar {{
        display: flex; align-items: center; justify-content: center;
        padding: 0.6rem 1rem; margin-bottom: 0.5rem;
    }}
    .nav-timeline-steps {{
        display: flex; align-items: center; gap: 0;
        background: {bg_steps};
        backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
        border: 2px solid {border_steps};
        border-radius: 60px; padding: 6px 10px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15), 0 0 15px {border_steps}; /* Prominent shadow & glow */
        transition: all 0.3s ease;
    }}
    .nav-timeline-steps:hover {{
        border-color: {active_label};
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2), 0 0 20px {active_bg};
    }}
    .nav-step + .nav-step::before {{
        content: ''; display: inline-block;
        width: 28px; height: 2px;
        background: {connector_color};
        vertical-align: middle; margin: 0 -2px;
        border-radius: 1px; transition: background 0.3s ease;
    }}
    .nav-step {{
        display: inline-flex; flex-direction: column; align-items: center;
        text-decoration: none !important;
        padding: 8px 16px; border-radius: 40px;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative; cursor: pointer;
    }}
    .nav-step:hover {{
        background: {active_bg};
        transform: translateY(-2px);
    }}
    .nav-step-icon {{ font-size: 1.25rem; line-height: 1; margin-bottom: 2px; }}
    .nav-step-label {{
        font-size: 0.6rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.08em;
        color: {label_color}; transition: color 0.3s ease;
        font-family: 'Inter', sans-serif;
    }}
    .nav-step:hover .nav-step-label {{ color: {label_hover}; }}
    .nav-step-active {{ background: {active_bg}; }}
    .nav-step-active .nav-step-label {{ color: {active_label}; font-weight: 700; }}
    .nav-step-active::after {{
        content: ''; position: absolute; bottom: 3px;
        left: 50%; transform: translateX(-50%);
        width: 16px; height: 3px;
        background: linear-gradient(135deg, #6366f1, #a855f7);
        border-radius: 2px;
    }}
    </style>
    <div class="nav-timeline-bar">
        <div class="nav-timeline-steps">
            {steps_html}
        </div>
    </div>
    '''
    st.html(nav_component)

def _render_theme_toggle_only():
    """Renders just the theme toggle button when the full nav is hidden."""
    current_theme = st.session_state["theme"]
    theme_icon = "🌙" if current_theme == "Light" else "☀️"
    
    col_spacer, col_btn = st.columns([30, 1])
    with col_btn:
        if st.button(theme_icon, key="theme_toggle_btn"):
            new_theme = "Dark" if current_theme == "Light" else "Light"
            st.session_state["theme"] = new_theme
            st.query_params["theme"] = new_theme
            st.rerun()



def _inject_theme_css(theme):
    """Inject base CSS + nav timeline styles + theme overrides."""
    css_path = Path(__file__).parent.parent / "assets" / "style.css"
    if not css_path.exists():
        return
    base_css = css_path.read_text(encoding='utf-8')

    # ── Theme Toggle Button Styles ────────────────────────
    toggle_css = """
    /* Theme toggle button positioning */
    [data-testid="stButton"][class*="st-key-theme_toggle_btn"] {
        position: fixed !important;
        top: 0.5rem !important;
        right: 0.7rem !important;
        z-index: 999999 !important;
    }
    [data-testid="stButton"][class*="st-key-theme_toggle_btn"] button {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 14px !important;
        padding: 4px 8px !important;
        font-size: 1rem !important;
        min-height: 0 !important;
        min-width: 0 !important;
        width: auto !important;
        line-height: 1 !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stButton"][class*="st-key-theme_toggle_btn"] button:hover {
        transform: scale(1.1) !important;
        background: rgba(255, 255, 255, 0.2) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
    }
    """

    # ── Light Mode Overrides ────────────────────────────
    light_css = ""
    if theme == "Light":
        light_css = """
        :root {
            --bg-primary: #ffffff;
            --bg-secondary: #f8fafc;
            --bg-card: rgba(255, 255, 255, 0.9);
            --bg-card-hover: rgba(255, 255, 255, 1);
            --border-color: rgba(0, 0, 0, 0.08);
            --border-glow: rgba(99, 102, 241, 0.2);
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --text-muted: #64748b;
            --accent-indigo: #4338ca;
            --accent-purple: #6d28d9;
            --accent-emerald: #059669;
            --accent-rose: #be123c;
            --accent-amber: #b45309;
            --shadow-card: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            --shadow-glow: 0 0 20px rgba(99, 102, 241, 0.1);
            --gradient-text: linear-gradient(135deg, #0f172a 0%, #334155 100%);
        }

        /* ── Background ─── */
        .stApp {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
            background-attachment: fixed !important;
        }

        /* ── Text Visibility Fixes ─── */
        .stApp, .stApp p, .stApp span, .stApp div, .stApp label, .stApp li { 
            color: var(--text-primary) !important; 
        }
        .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown li { 
            color: var(--text-primary) !important; 
        }
        h1, h2, h3, h4, h5, h6 { color: var(--text-primary) !important; }
        
        /* Specific overrides for common Streamlit components */
        [data-testid="stMetricValue"] { color: var(--text-primary) !important; }
        [data-testid="stMetricDelta"] { color: var(--accent-emerald) !important; }
        [data-testid="stMetricLabel"] { color: var(--text-secondary) !important; }
        [data-testid="stCaptionContainer"] { color: var(--text-muted) !important; }
        
        /* Streamlit Native Label Visibility */
        [data-testid="stWidgetLabel"] p { color: var(--text-primary) !important; font-weight: 600 !important; }
        [data-testid="stHeader"] { background-color: rgba(255, 255, 255, 0.8) !important; backdrop-filter: blur(8px); }
        
        /* ── Form Inputs & File Uploader ─── */
        .stTextInput input, .stTextArea textarea, .stSelectbox select {
            background-color: #ffffff !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-color) !important;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: var(--accent-indigo) !important;
            box-shadow: 0 0 0 1px var(--accent-indigo) !important;
        }
        
        [data-testid="stFileUploader"] {
            background-color: #ffffff !important;
            border: 2px dashed var(--accent-indigo) !important;
            padding: 2rem !important;
        }
        [data-testid="stFileUploaderDropzone"] {
            background-color: #f8fafc !important;
            border-radius: 12px !important;
        }
        [data-testid="stFileUploaderDropzone"] p {
            color: var(--text-secondary) !important;
        }
        [data-testid="stFileUploader"] button {
            background-color: #ffffff !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-color) !important;
        }
        [data-testid="stFileUploader"] button:hover {
            border-color: var(--accent-indigo) !important;
            color: var(--accent-indigo) !important;
        }

        /* ── Buttons ─── */
        .stButton > button, .stFormSubmitButton > button {
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2) !important;
        }
        .stFormSubmitButton > button {
            background: var(--gradient-primary) !important;
            color: white !important;
            font-weight: 700 !important;
        }
        .secondary-button button {
            background: #ffffff !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-color) !important;
        }
        .secondary-button button:hover {
            border-color: var(--accent-indigo) !important;
            background: #f8fafc !important;
        }

        /* ── Cards ─── */
        .custom-card {
            background: #ffffff !important;
            border: 1px solid var(--border-color) !important;
            box-shadow: var(--shadow-card) !important;
        }
        .custom-card::before { background: #ffffff !important; opacity: 1 !important; }
        .custom-card p { color: var(--text-secondary) !important; }
        
        .section-header {
            background: var(--gradient-primary);
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* ── Metrics, Tags, Badges ─── */
        div[data-testid="stMetric"] { background: #ffffff !important; border: 1px solid var(--border-color) !important; }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: var(--text-primary) !important; }
        
        .skill-tag { background: #f1f5f9 !important; color: var(--text-secondary) !important; border-color: var(--border-color) !important; }
        .skill-tag.match { background: rgba(5, 150, 105, 0.1) !important; color: #059669 !important; border-color: rgba(5, 150, 105, 0.2) !important; }
        .skill-tag.missing { background: rgba(190, 18, 60, 0.1) !important; color: #be123c !important; border-color: rgba(190, 18, 60, 0.2) !important; }
        
        /* ── Success/Info/Warning Messages ─── */
        .stAlert { background-color: #ffffff !important; color: var(--text-primary) !important; border: 1px solid var(--border-color) !important; }
        .custom-success {
            background: rgba(5, 150, 105, 0.05) !important;
            color: #059669 !important;
            border: 1px solid rgba(5, 150, 105, 0.2) !important;
        }
        
        /* ── Charts ─── */
        .stPlotlyChart { background: #ffffff !important; border: 1px solid var(--border-color) !important; }
        
        /* ── Sidebar (if visible) ─── */
        section[data-testid="stSidebar"] { background-color: #f8fafc !important; border-right: 1px solid var(--border-color) !important; }
        
        /* ── Expanders ─── */
        div[data-testid="stExpander"] { 
            background: #ffffff !important; 
            border: 1px solid rgba(0, 0, 0, 0.12) !important; 
            border-radius: 14px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
            margin-bottom: 1rem !important;
            transition: all 0.3s ease !important;
        }
        div[data-testid="stExpander"]:hover {
            box-shadow: 0 10px 20px rgba(99, 102, 241, 0.08) !important;
            border-color: var(--accent-indigo) !important;
        }
        div[data-testid="stExpander"] summary { 
            background-color: #ffffff !important; 
            color: var(--text-primary) !important; 
            border-radius: 14px !important;
            padding: 0.5rem 1rem !important;
        }
        div[data-testid="stExpander"] summary:hover { 
            background-color: #f8fafc !important; 
        }
        div[data-testid="stExpander"] summary p, div[data-testid="stExpander"] summary span {
            color: var(--text-primary) !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
        }
        div[data-testid="stExpander"] > div[role="region"] { 
            background-color: #ffffff !important; 
            color: var(--text-secondary) !important; 
            padding: 1.5rem !important;
            border-top: 1px solid rgba(0, 0, 0, 0.05) !important;
        }
        div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] p {
            color: var(--text-secondary) !important;
        }

        /* ── Priority Badges & Highlights ─── */
        .priority-high {
            background: #fee2e2 !important;
            color: #991b1b !important;
            padding: 4px 12px !important;
            border-radius: 20px !important;
            font-size: 0.75rem !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            border: 1px solid #fecaca !important;
            display: inline-block !important;
        }
        .priority-medium {
            background: #fef3c7 !important;
            color: #92400e !important;
            padding: 4px 12px !important;
            border-radius: 20px !important;
            font-size: 0.75rem !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            border: 1px solid #fde68a !important;
            display: inline-block !important;
        }
        .priority-low {
            background: #e0e7ff !important;
            color: #3730a3 !important;
            padding: 4px 12px !important;
            border-radius: 20px !important;
            font-size: 0.75rem !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            border: 1px solid #c7d2fe !important;
            display: inline-block !important;
        }

        /* ── Category Tags ─── */
        .category-tag {
            background: #f1f5f9 !important;
            color: #475569 !important;
            padding: 4px 10px !important;
            border-radius: 6px !important;
            font-size: 0.75rem !important;
            font-weight: 600 !important;
            margin-left: 8px !important;
            border: 1px solid rgba(0,0,0,0.05) !important;
            display: inline-block !important;
        }

        /* ── Action Items ─── */
        .action-item {
            background: #f8fafc !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 10px !important;
            padding: 12px 16px !important;
            margin-bottom: 10px !important;
            display: flex !important;
            align-items: flex-start !important;
            font-size: 0.95rem !important;
            color: var(--text-secondary) !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
        }
        .action-item-check {
            color: #10b981 !important;
            margin-right: 12px !important;
            font-weight: 900 !important;
            font-size: 1.1rem !important;
        }

        """

    st.markdown(f"<style>{base_css}\n{toggle_css}\n{light_css}</style>", unsafe_allow_html=True)
