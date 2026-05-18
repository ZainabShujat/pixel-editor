import streamlit as st
import numpy as np
from PIL import Image

st.set_page_config(page_title="Pixel Art Editor")

GRID_SIZE = 16
PIXEL_SIZE = 30

if "grid" not in st.session_state:
    st.session_state.grid = np.full(
        (GRID_SIZE, GRID_SIZE),
        "#111111",
        dtype=object
    )

st.title("🎮 Tiny Pixel Art Editor")

selected_color = st.color_picker(
    "Pick a color",
    "#ffffff"
)

st.write("Click cells to place pixels.")

# Create grid
for row in range(GRID_SIZE):

    cols = st.columns(GRID_SIZE)

    for col in range(GRID_SIZE):

        current_color = st.session_state.grid[row][col]

        button_style = f"""
            <style>
            div[data-testid="stButton"] button {{
                background-color: {current_color};
                width: 30px;
                height: 30px;
                padding: 0;
                border-radius: 0;
                border: 1px solid #333;
            }}
            </style>
        """

        cols[col].markdown(button_style, unsafe_allow_html=True)

        if cols[col].button(
            " ",
            key=f"{row}-{col}"
        ):
            st.session_state.grid[row][col] = selected_color
            st.rerun()

st.divider()

# Clear button
if st.button("Clear Canvas"):
    st.session_state.grid = np.full(
        (GRID_SIZE, GRID_SIZE),
        "#111111",
        dtype=object
    )
    st.rerun()

# Export image
if st.button("Export PNG"):

    image = Image.new(
        "RGB",
        (GRID_SIZE, GRID_SIZE)
    )

    pixels = image.load()

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):

            hex_color = st.session_state.grid[y][x]

            rgb = tuple(
                int(hex_color[i:i+2], 16)
                for i in (1, 3, 5)
            )

            pixels[x, y] = rgb

    image = image.resize(
        (GRID_SIZE * PIXEL_SIZE,
         GRID_SIZE * PIXEL_SIZE),
        Image.Resampling.NEAREST
    )

    image.save("pixel_art.png")

    with open("pixel_art.png", "rb") as file:
        st.download_button(
            "Download PNG",
            file,
            file_name="pixel_art.png"
        )
