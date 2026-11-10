
from io import BytesIO

import streamlit as st
from PIL import Image, ImageOps

from modules.image_upload import validate_image
from modules.background_removal import remove_background
from modules.sketch_engine import (
    convert_to_grayscale,
    generate_pencil_sketch,
    sharpen_image
)
from modules import ui
from modules.background import render_leaves


# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="DrawImg | Image to Pencil Sketch",
    page_icon="✏️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Theme is read before the sidebar toggle is drawn, so styles apply on the same run
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

ui.inject_styles("dark" if st.session_state.dark_mode else "light")
render_leaves()


# ---------------------------------------------------------------------------
# Pencil style presets
# ---------------------------------------------------------------------------
PRESETS = {
    "Soft":    {"blur": 35, "dark": 1.3, "sharp": 0.0},
    "Classic": {"blur": 21, "dark": 1.8, "sharp": 0.5},
    "Bold":    {"blur": 11, "dark": 2.6, "sharp": 1.2},
}

if "blur" not in st.session_state:
    st.session_state.blur = PRESETS["Classic"]["blur"]
    st.session_state.dark = PRESETS["Classic"]["dark"]
    st.session_state.sharp = PRESETS["Classic"]["sharp"]
    st.session_state.preset = "Classic"


def apply_preset():
    choice = st.session_state.preset
    if choice in PRESETS:
        st.session_state.blur = PRESETS[choice]["blur"]
        st.session_state.dark = PRESETS[choice]["dark"]
        st.session_state.sharp = PRESETS[choice]["sharp"]


def mark_custom():
    st.session_state.preset = "Custom"


# ---------------------------------------------------------------------------
# Cached processing (background removal is slow, so never repeat it
# just because a slider moved)
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False, max_entries=8)
def cached_remove_background(image_bytes):
    # Same orientation fix as the upload step, so both images line up
    image = ImageOps.exif_transpose(Image.open(BytesIO(image_bytes)))
    return remove_background(image)


def to_png_bytes(image):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


# ---------------------------------------------------------------------------
# Sidebar: controls
# ---------------------------------------------------------------------------
def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode


with st.sidebar:
    # Round sun/moon theme button, pinned to the top-left corner by CSS
    st.button(
        "☀️" if st.session_state.dark_mode else "🌙",
        key="theme_btn",
        on_click=toggle_theme,
    )

    st.header("Studio")

    uploaded_file = st.file_uploader(
        "Photograph",
        type=["jpg", "jpeg", "png"],
        help="JPG or PNG, at least 100 × 100 px.",
    )

    remove_bg = st.toggle(
        "Remove background",
        value=False,
        help="Isolates the subject on clean white paper before sketching. "
             "Your original photo is never changed. The first run downloads a model, so it can take a moment.",
    )

    st.segmented_control(
        "Pencil style",
        options=list(PRESETS) + ["Custom"],
        key="preset",
        on_change=apply_preset,
        width="stretch",
    )

    st.slider(
        "Blur strength",
        min_value=5, max_value=51, step=2,
        key="blur",
        on_change=mark_custom,
        help="Higher values give softer shading; lower values keep fine detail.",
    )
    st.slider(
        "Pencil darkness",
        min_value=1.0, max_value=3.0, step=0.1,
        key="dark",
        on_change=mark_custom,
        help="Controls how heavy the pencil strokes look.",
    )
    st.slider(
        "Sharpness",
        min_value=0.0, max_value=3.0, step=0.1,
        key="sharp",
        on_change=mark_custom,
        help="Crisps up edges and pencil lines. 0 = off; higher values give harder, more defined strokes.",
    )


# ---------------------------------------------------------------------------
# Main area
# ---------------------------------------------------------------------------
ui.hero()

if uploaded_file is None:
    ui.empty_state()
    ui.footer()
    st.stop()

is_valid, result = validate_image(uploaded_file)

if not is_valid:
    st.error(result, icon="⚠️")
    ui.footer()
    st.stop()

original = result
processed_image = original

if remove_bg:
    with st.spinner("Lifting the background off the page…"):
        try:
            processed_image = cached_remove_background(uploaded_file.getvalue())
        except Exception as error:
            ui.background_removal_error(error)

grayscale_image = convert_to_grayscale(processed_image)
pencil_sketch = generate_pencil_sketch(
    grayscale_image,
    blur_strength=st.session_state.blur,
    darkness=st.session_state.dark,
)
pencil_sketch = sharpen_image(pencil_sketch, amount=st.session_state.sharp)

# ---- 01 · Before / after ---------------------------------------------------
ui.section("01", "Before &amp; after")

left, right = st.columns(2, gap="large")
with left:
    ui.frame_caption("Photograph", "the original")
    st.image(original, width="stretch")
with right:
    ui.frame_caption("Pencil sketch", f"{st.session_state.preset.lower()} pencil")
    st.image(pencil_sketch, width="stretch")

stem = uploaded_file.name.rsplit(".", 1)[0]
dl_col, _ = st.columns([1, 2])
with dl_col:
    st.download_button(
        "Download sketch (PNG)",
        data=to_png_bytes(pencil_sketch),
        file_name=f"{stem}_sketch.png",
        mime="image/png",
        type="primary",
        icon=":material/download:",
        width="stretch",
    )

# ---- 02 · Process ----------------------------------------------------------
ui.section("02", "How it was drawn")

tab_steps, tab_info = st.tabs(["Every stage", "Image details"])

with tab_steps:
    stages = [
        ("Original", "as uploaded", original),
        ("Processed", "background removed" if remove_bg else "unchanged", processed_image),
        ("Grayscale", "colour dropped", grayscale_image),
        ("Sketch", "dodge, blend + sharpen", pencil_sketch),
    ]
    cols = st.columns(4, gap="medium")
    for col, (title, note, img) in zip(cols, stages):
        with col:
            ui.frame_caption(title, note)
            st.image(img, width="stretch")

with tab_info:
    ui.chips([
        ("Format", original.format or "—"),
        ("Dimensions", f"{original.width} × {original.height} px"),
        ("Colour mode", original.mode),
        ("File size", f"{len(uploaded_file.getvalue()) / 1024:,.0f} KB"),
        ("Blur", st.session_state.blur),
        ("Darkness", f"{st.session_state.dark:.1f}"),
        ("Sharpness", f"{st.session_state.sharp:.1f}"),
    ])

ui.footer()
