
"""
Uses assets/falling_maple_leaves.html as the animated page background.

The asset draws leaves on a <canvas> with JavaScript. Streamlit strips
scripts from st.html, so the asset runs inside a components iframe that
CSS (in modules/ui.py) pins full-screen behind the main content. The
sidebar sits above it, so leaves never appear there.

Only two changes are made to the asset before it runs:
  * its own page text (<main>) is removed
  * its body background is made transparent, because the app's
    light/dark theme paints the background instead
"""

import re
from functools import lru_cache
from pathlib import Path

import streamlit.components.v1 as components

ASSET = Path(__file__).resolve().parent.parent / "assets" / "falling_maple_leaves.html"

# Unique marker so CSS can find this iframe (iframe[srcdoc*="di-leaves-bg"])
MARKER = "<!-- di-leaves-bg -->"

# Used for the light theme if the asset has no body background
_FALLBACK_LIGHT_BG = "linear-gradient(180deg, #fdf3e3 0%, #f8e2c4 55%, #f1cfa6 100%)"


@lru_cache(maxsize=1)
def _load_asset():
    try:
        return ASSET.read_text(encoding="utf-8")
    except OSError:
        return ""


@lru_cache(maxsize=1)
def light_background():
    """The body background defined in the asset (used by the light theme)."""
    match = re.search(r"body\s*\{[^}]*?background:\s*([^;]+);", _load_asset(), re.S)
    return match.group(1).strip() if match else _FALLBACK_LIGHT_BG


@lru_cache(maxsize=1)
def _prepared_html():
    html = _load_asset()
    if not html:
        return ""

    # Drop the demo text that the asset shows over the leaves
    html = re.sub(r"<main>.*?</main>", "", html, flags=re.S)

    # Let the themed Streamlit background show through
    html = html.replace(
        "</style>",
        "  html, body { background: transparent !important; overflow: hidden; }\n</style>",
        1,
    )
    return MARKER + html


def render_leaves():
    """Draw the falling-leaves layer. Call once per run, near the top."""
    html = _prepared_html()
    if html:
        # The HTML never changes between reruns, so Streamlit keeps the
        # same iframe alive and the animation doesn't restart.
        components.html(html, height=0)
