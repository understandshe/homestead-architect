import streamlit as st
import os

from engine.layout_engine import LayoutEngine
from engine.scene_builder import SceneBuilder
from render.renderer_2d import Renderer2D
from render.renderer_3d import Renderer3D
from export.pdf_export import PDFExporter

# -------------------------
# CONFIG
# -------------------------

st.set_page_config(
    page_title="Homestead Architect",
    layout="wide"
)

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------
# UI HEADER
# -------------------------

st.title("Homestead Architect")
st.caption("Generate premium 2D & 3D homestead layouts instantly")

# -------------------------
# SIDEBAR INPUT
# -------------------------

st.sidebar.header("Project Settings")

plot_width = st.sidebar.slider("Plot Width (meters)", 50, 300, 150)
plot_height = st.sidebar.slider("Plot Height (meters)", 50, 300, 150)

beds = st.sidebar.slider("Garden Beds", 2, 30, 10)
trees = st.sidebar.slider("Trees", 2, 40, 15)

# -------------------------
# GENERATE BUTTON
# -------------------------

if st.sidebar.button("Generate Layout"):

    with st.spinner("Generating layout..."):

        # -------------------------
        # STEP 1: LAYOUT
        # -------------------------
        engine = LayoutEngine(plot_width, plot_height)
        layout_data = engine.generate(beds=beds, trees=trees)

        # -------------------------
        # STEP 2: SCENE BUILD
        # -------------------------
        builder = SceneBuilder(layout_data)
        scene = builder.build()

        # -------------------------
        # STEP 3: 2D RENDER
        # -------------------------
        renderer2d = Renderer2D(scene)
        image_path = os.path.join(OUTPUT_DIR, "map_2d.png")
        renderer2d.render(image_path)

        # -------------------------
        # STEP 4: 3D EXPORT
        # -------------------------
        renderer3d = Renderer3D(scene)
        model_path = os.path.join(OUTPUT_DIR, "map_3d.glb")
        renderer3d.export(model_path)

        # -------------------------
        # STEP 5: PDF EXPORT
        # -------------------------
        pdf = PDFExporter(scene, image_path)
        pdf_path = os.path.join(OUTPUT_DIR, "report.pdf")
        pdf.export(pdf_path)

    st.success("Layout generated successfully")

    # -------------------------
    # DISPLAY OUTPUT
    # -------------------------

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("2D Map Preview")
        st.image(image_path)

    with col2:
        st.subheader("Downloads")

        with open(model_path, "rb") as f:
            st.download_button(
                "Download 3D Model (.glb)",
                f,
                file_name="homestead_3d.glb"
            )

        with open(pdf_path, "rb") as f:
            st.download_button(
                "Download PDF Report",
                f,
                file_name="homestead_report.pdf"
            )

# -------------------------
# FOOTER
# -------------------------

st.markdown("---")
st.caption("Built for global homestead planning")
