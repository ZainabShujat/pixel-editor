import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.set_page_config(
    page_title="Tiny Pixel Editor",
    layout="centered"
)

st.title("🎨 Tiny Pixel Editor")

st.write(
    "Tiny browser-based pixel art editor built with Python."
)

stroke_color = st.color_picker(
    "Pick a color",
    "#ffffff"
)

stroke_width = st.slider(
    "Pixel Size",
    5,
    40,
    20
)

canvas_result = st_canvas(
    fill_color="rgba(255,255,255,0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color="#111111",
    width=640,
    height=640,
    drawing_mode="freedraw",
    key="canvas",
)

st.info(
    "Use the toolbar to undo, redo, clear, and download."
)
