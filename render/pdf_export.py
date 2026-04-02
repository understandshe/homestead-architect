from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet


class PDFExporter:

    def __init__(self, scene, image_path):
        self.scene = scene
        self.image_path = image_path
        self.styles = getSampleStyleSheet()

    # -------------------------
    # SUMMARY DATA
    # -------------------------

    def generate_summary(self):

        elements = self.scene["elements"]

        beds = sum(1 for e in elements if e["type"] == "bed")
        trees = sum(1 for e in elements if e["type"] == "tree")

        plot = self.scene["plot"]

        return {
            "Plot Size": f'{plot["width"]} x {plot["height"]} meters',
            "Garden Beds": beds,
            "Trees": trees,
            "Paths": "Curved layout"
        }

    # -------------------------
    # TABLE DESIGN
    # -------------------------

    def build_table(self, data_dict):

        data = [["Parameter", "Value"]]

        for k, v in data_dict.items():
            data.append([k, str(v)])

        table = Table(data, colWidths=[200, 200])

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2F4F4F")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F5F5F5")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("ALIGN", (0, 0), (-1, -1), "LEFT")
        ]))

        return table

    # -------------------------
    # BUILD PDF
    # -------------------------

    def export(self, output_path="output/homestead_report.pdf"):

        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        elements = []

        # Title
        elements.append(Paragraph(
            "Homestead Layout Report",
            self.styles["Title"]
        ))

        elements.append(Spacer(1, 20))

        # Subtitle
        elements.append(Paragraph(
            "Generated Layout Overview",
            self.styles["Heading2"]
        ))

        elements.append(Spacer(1, 12))

        # Image
        elements.append(Image(self.image_path, width=450, height=450))

        elements.append(Spacer(1, 20))

        # Summary
        elements.append(Paragraph(
            "Project Summary",
            self.styles["Heading2"]
        ))

        elements.append(Spacer(1, 10))

        summary = self.generate_summary()

        table = self.build_table(summary)

        elements.append(table)

        elements.append(Spacer(1, 20))

        # Footer note
        elements.append(Paragraph(
            "This layout is generated using automated planning algorithms and can be customized further based on terrain and personal requirements.",
            self.styles["Normal"]
        ))

        doc.build(elements)

        return output_path
