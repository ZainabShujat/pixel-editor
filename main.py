import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.set_page_config(
    page_title="Tiny Pixel Editor",
    layout="centered"
)

st.title("🎮 Tiny Pixel Editor")

st.write(
    "A tiny retro-style pixel painter built with Python."
)

# Color Picker
color = st.color_picker(
    "Choose Color",
    "#ffffff"
)

# Pixel Size Slider
pixel_size = st.slider(
    "Pixel Size",
    min_value=5,
    max_value=50,
    value=20
)

st.write("Paint chunky pixel-style squares onto the canvas.")

# Canvas
canvas_result = st_canvas(
    fill_color=color,
    stroke_width=pixel_size,
    stroke_color=color,
    background_color="#111111",
    width=640,
    height=640,
    drawing_mode="freedraw",
    point_display_radius=0,
    key="canvas",
)

st.info(
    "Use the toolbar for undo, redo, clear, and download."
)
