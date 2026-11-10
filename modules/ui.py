
"""
Presentation helpers: custom CSS and small HTML components
that give DrawImg its "artist's sketchbook" look.
"""

import streamlit as st


_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&family=Caveat:wght@500;700&display=swap');

__THEME_VARS__

/* ---------- Base ---------- */
html, body, [class*="css"], .stApp, .stMarkdown, button, input, label {
    font-family: 'DM Sans', system-ui, sans-serif;
}
.stApp { background: var(--body-bg); color: var(--ink); }
.stApp [data-testid="stMain"] { position: relative; z-index: 1; }

/* Falling-leaves iframe (modules/background.py): pinned behind the content */
iframe[srcdoc*="di-leaves-bg"] {
    position: fixed !important; inset: 0 !important;
    width: 100vw !important; height: 100vh !important;
    z-index: -1; pointer-events: none; border: 0;
    opacity: var(--leaf-strength, 1);
}
[data-testid="stElementContainer"]:has(iframe[srcdoc*="di-leaves-bg"]) {
    height: 0 !important; margin: 0 !important; min-height: 0 !important;
}

/* Keep the sidebar solid so the leaves never show behind it */
section[data-testid="stSidebar"] { z-index: 100; }

/* Text and native widgets follow the active theme */
.stApp p, .stApp label, .stApp li,
[data-testid="stWidgetLabel"] p,
[data-testid="stMarkdownContainer"],
[data-testid="stSliderTickBarMin"], [data-testid="stSliderTickBarMax"],
[data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stFileUploaderFileName"],
.stTabs [data-baseweb="tab"] p { color: var(--ink) !important; }
[data-testid="stFileUploaderDropzoneInstructions"] small,
[data-testid="stFileUploaderFile"] small { color: var(--graphite) !important; }
[data-testid="stTooltipIcon"] svg, [data-testid="stSidebarCollapseButton"] svg,
[data-testid="stExpandSidebarButton"] svg, [data-testid="stFileUploaderFile"] svg { color: var(--graphite); }
[data-testid="stFileUploaderFile"] { background: transparent; }
[data-testid="stTooltipIcon"] button { color: var(--graphite) !important; }

/* Toggle switch track when off (Streamlit's default is too faint on dark) */
[data-testid="stCheckbox"] input[role="switch"] + div,
[data-testid="stCheckbox"] label > span + div { background-color: var(--track); }
[data-testid="stCheckbox"] input[role="switch"]:checked + div,
[data-testid="stCheckbox"] label:has(input:checked) > span + div { background-color: var(--accent) !important; }

button[data-variant="segmented_control"],
[data-testid="stFileUploaderDropzone"] button,
[data-testid="stBaseButton-secondary"] {
    background: var(--card) !important; color: var(--ink) !important;
    border-color: var(--rule) !important;
}
button[data-variant="segmented_control"][aria-checked="true"] {
    background: var(--accent-soft) !important; color: var(--accent) !important;
    border-color: var(--accent) !important;
}
.block-container { padding-top: 2.2rem; max-width: 1240px; }
header[data-testid="stHeader"] { background: transparent; }

h1, h2, h3 {
    font-family: 'Instrument Serif', Georgia, serif !important;
    font-weight: 400 !important;
    color: var(--ink);
    letter-spacing: -.01em;
}

/* ---------- Hero ---------- */
.di-hero {
    display: flex; align-items: flex-end; justify-content: space-between;
    gap: 2rem; flex-wrap: wrap;
    padding: .25rem 0 1.4rem;
    border-bottom: 1.5px solid var(--ink);
    margin-bottom: 1.8rem;
}
.di-brand {
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: clamp(3rem, 7vw, 5.2rem);
    line-height: .9; color: var(--ink); margin: 0;
}
.di-brand em { color: var(--accent); }
.di-tag {
    font-family: 'Caveat', cursive; font-size: 1.6rem;
    color: var(--graphite); margin: .45rem 0 0; transform: rotate(-1.2deg);
}
.di-hero-meta {
    font-size: .78rem; letter-spacing: .14em; text-transform: uppercase;
    color: var(--graphite); text-align: right; line-height: 1.9;
}

/* ---------- Section labels ---------- */
.di-label {
    display: flex; align-items: baseline; gap: .7rem;
    margin: 1.6rem 0 .8rem;
}
.di-label .num {
    font-family: 'Instrument Serif', serif; font-style: italic;
    font-size: 1.4rem; color: var(--accent);
}
.di-label .txt {
    font-family: 'Instrument Serif', serif; font-size: 1.85rem; color: var(--ink);
}
.di-label .rule { flex: 1; height: 1px; background: var(--rule); align-self: center; }

/* ---------- Cards / frames ---------- */
.di-frame-cap {
    display: flex; justify-content: space-between; align-items: baseline;
    margin: 0 0 .45rem;
}
.di-frame-cap .t { font-family: 'Instrument Serif', serif; font-size: 1.35rem; }
.di-frame-cap .n { font-family: 'Caveat', cursive; font-size: 1.15rem; color: var(--graphite); }

[data-testid="stImage"] img {
    border-radius: 6px;
    background: var(--frame);
    padding: 8px;
    box-shadow: 0 1px 0 var(--rule), 0 10px 28px -14px rgba(43,42,40,.35);
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--card);
    border-color: var(--rule) !important;
    backdrop-filter: blur(6px);
    border-radius: 14px !important;
}

/* ---------- Empty state ---------- */
.di-steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1.4rem; }
.di-step {
    background: var(--card); backdrop-filter: blur(6px); border: 1px solid var(--rule); border-radius: 14px;
    padding: 1.3rem 1.3rem 1.1rem;
}
.di-step .k { font-family: 'Instrument Serif', serif; font-style: italic; color: var(--accent); font-size: 1.5rem; }
.di-step h4 { font-family: 'Instrument Serif', serif; font-weight: 400; font-size: 1.45rem; margin: .1rem 0 .3rem; }
.di-step p { color: var(--graphite); font-size: .92rem; margin: 0; line-height: 1.5; }
@media (max-width: 760px) { .di-steps { grid-template-columns: 1fr; } }

/* ---------- Uploader ---------- */
[data-testid="stFileUploaderDropzone"] {
    background: var(--card);
    backdrop-filter: blur(6px);
    border: 1.5px dashed var(--dash);
    border-radius: 14px;
    padding: 1.6rem;
    transition: border-color .2s, background .2s;
}
section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] { padding: 1rem .9rem; }
[data-testid="stFileUploaderDropzone"]:hover { border-color: var(--accent); }

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: var(--paper-deep);
    border-right: 1px solid var(--rule);
}
section[data-testid="stSidebar"] h2 { font-size: 1.9rem; margin: 0; padding: 0 0 .35rem; }

/* No sidebar scrolling: compact layout that fits the screen, scrollbar hidden */
[data-testid="stSidebarContent"] { overflow: hidden !important; scrollbar-width: none; }
[data-testid="stSidebarContent"]::-webkit-scrollbar { display: none; }
[data-testid="stSidebarUserContent"] { padding-top: 0 !important; padding-bottom: 1rem !important; }
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: .55rem; }
section[data-testid="stSidebar"] [data-testid="stSlider"] { padding-bottom: 0; }
section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] { padding: .7rem .8rem !important; }
/* Very short screens: still reachable with the wheel/trackpad, just no visible bar */
@media (max-height: 640px) { [data-testid="stSidebarContent"] { overflow-y: auto !important; } }

/* Round sun/moon theme button, top-left of the sidebar header */
.st-key-theme_btn {
    position: fixed; top: .85rem; left: 1.1rem; z-index: 1000; width: auto !important;
}
.st-key-theme_btn button {
    width: 2.5rem; height: 2.5rem; min-height: 0; padding: 0 !important;
    border-radius: 50% !important; font-size: 1.15rem; line-height: 1;
    background: var(--card) !important; border: 1px solid var(--rule) !important;
    box-shadow: 0 4px 14px -6px rgba(0,0,0,.35);
    transition: transform .25s ease;
}
.st-key-theme_btn button:hover { transform: rotate(20deg) scale(1.06); border-color: var(--accent) !important; }
.st-key-theme_btn button p { font-size: 1.15rem !important; margin: 0; }
.di-side-note { font-family: 'Caveat', cursive; font-size: 1.2rem; color: var(--graphite); margin-top: -.2rem; }

/* ---------- Buttons ---------- */
.stDownloadButton button, .stButton button {
    border-radius: 999px; font-weight: 600; padding: .55rem 1.3rem;
}
.stDownloadButton button[kind="primary"] { box-shadow: 0 6px 18px -8px rgba(194,85,45,.7); }

/* ---------- Metric chips ---------- */
.di-chips { display: flex; flex-wrap: wrap; gap: .6rem; }
.di-chip {
    background: var(--card); backdrop-filter: blur(6px); border: 1px solid var(--rule); border-radius: 999px;
    padding: .4rem .95rem; font-size: .88rem; color: var(--graphite);
}
.di-chip b { color: var(--ink); font-weight: 600; margin-left: .3rem; }

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] { gap: 1.4rem; border-bottom: 1px solid var(--rule); }
.stTabs [data-baseweb="tab"] { font-family: 'Instrument Serif', serif; font-size: 1.3rem; padding: .3rem 0; }

footer, #MainMenu { visibility: hidden; }
.di-footer {
    margin-top: 3rem; padding-top: 1rem; border-top: 1px solid var(--rule);
    font-family: 'Caveat', cursive; font-size: 1.2rem; color: var(--graphite); text-align: center;
}
</style>
"""


THEMES = {
    # Light: the warm peach gradient from assets/falling_maple_leaves.html
    "light": """
:root {
    --body-bg: __LIGHT_BG__;
    --paper-deep: #F3E6D2;
    --card: rgba(253,247,238,.80);
    --frame: #FFFFFF;
    --ink: #3A2416;
    --graphite: #7A5A43;
    --rule: #E3CCAE;
    --dash: #C9A983;
    --accent: #C2552D;
    --accent-soft: #F6D9C6;
    --leaf-strength: .85;
    --track: #E3CCAE;
}""",
    # Dark: a deep forest green, so the autumn leaves glow against it
    "dark": """
:root {
    --body-bg:
        radial-gradient(ellipse at 50% 15%, rgba(100,112,57,.35), transparent 55%),
        linear-gradient(145deg, #182b20, #263b2b 48%, #18251e);
    --paper-deep: #14231A;
    --card: rgba(12,24,17,.55);
    --frame: #FBF8F2;
    --ink: #FFF8E9;
    --graphite: #C9C6B4;
    --rule: rgba(255,255,255,.16);
    --dash: rgba(255,255,255,.32);
    --accent: #F28B24;
    --accent-soft: rgba(242,139,36,.18);
    --leaf-strength: 1;
    --track: rgba(255,255,255,.22);
}""",
}


def inject_styles(theme="light"):
    # Light theme uses the background gradient from the leaves asset
    from modules.background import light_background
    theme_vars = THEMES[theme].replace("__LIGHT_BG__", light_background())
    st.html(_CSS.replace("__THEME_VARS__", theme_vars))


def hero():
    st.html(
        """
        <div class="di-hero">
          <div>
            <h1 class="di-brand">Draw<em>Img</em></h1>
            <p class="di-tag">photographs, redrawn in graphite.</p>
          </div>
          <div class="di-hero-meta">Upload<br>Adjust<br>Download</div>
        </div>
        """
    )


def section(number, title):
    st.html(
        f"""
        <div class="di-label">
          <span class="num">{number}</span>
          <span class="txt">{title}</span>
          <span class="rule"></span>
        </div>
        """
    )


def frame_caption(title, note=""):
    st.html(
        f'<div class="di-frame-cap"><span class="t">{title}</span>'
        f'<span class="n">{note}</span></div>'
    )


def empty_state():
    st.html(
        """
        <div class="di-steps">
          <div class="di-step"><span class="k">i.</span><h4>Upload</h4>
            <p>Use the uploader in the sidebar: a JPG or PNG, at least 100&nbsp;×&nbsp;100 px. Portraits and pets work beautifully.</p></div>
          <div class="di-step"><span class="k">ii.</span><h4>Adjust</h4>
            <p>Pick a pencil style or fine-tune blur and darkness from the sidebar. Optionally lift the background.</p></div>
          <div class="di-step"><span class="k">iii.</span><h4>Download</h4>
            <p>Save your finished sketch as a crisp PNG, ready to print or share.</p></div>
        </div>
        """
    )


def chips(items):
    inner = "".join(f'<span class="di-chip">{k}<b>{v}</b></span>' for k, v in items)
    st.html(f'<div class="di-chips">{inner}</div>')


def footer():
    st.html('<div class="di-footer">made with a sharp pencil &amp; a little Python ✎</div>')


def _installed_version(package):
    from importlib.metadata import version, PackageNotFoundError
    try:
        return version(package)
    except PackageNotFoundError:
        return "not installed"


def background_removal_error(error):
    """
    Explain a background-removal failure. The common one is a numba/NumPy
    mismatch, which almost always means the fix was installed into a
    different Python than the one running Streamlit, so show which one.
    """
    import sys

    message = str(error)
    st.error(f"Background removal failed: {message}", icon="⚠️")

    if "Numba needs NumPy" not in message and "numba" not in message.lower():
        return

    python = sys.executable
    with st.expander("How to fix this", expanded=True):
        st.markdown(
            "rembg relies on **numba**, and the numba this app is running with "
            "is too old for NumPy 2.x. It must be **0.61 or newer**."
        )
        st.markdown(
            f"""
| | This app is using |
|---|---|
| Python | `{python}` |
| numba | `{_installed_version("numba")}` |
| NumPy | `{_installed_version("numpy")}` |
"""
        )
        st.markdown(
            "**1.** Stop Streamlit (Ctrl + C in its terminal).  \n"
            "**2.** Run this, which installs into *exactly* the Python above:"
        )
        st.code(f'"{python}" -m pip install --upgrade "numba==0.61.2" "llvmlite==0.44.0"', language="bash")
        st.markdown(
            "**3.** Start the app again with that same Python:"
        )
        st.code(f'"{python}" -m streamlit run app.py', language="bash")
        st.caption(
            "Running plain `pip install` often targets a different Python "
            "(for example the system one instead of your PyCharm venv), "
            "which is why the error can come back after installing."
        )
