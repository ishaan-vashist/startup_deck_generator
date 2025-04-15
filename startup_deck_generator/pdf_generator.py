import os
from markdown2 import markdown
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from bs4 import BeautifulSoup

# File paths
INPUT_FILE = "deck_output.md"
OUTPUT_FILE = "deck_output.pdf"

# Convert Markdown content into structured blocks (heading, paragraph, bullet)
def markdown_to_text_blocks(md_content):
    html = markdown(md_content)
    soup = BeautifulSoup(html, "html.parser")

    blocks = []
    for tag in soup.children:
        if tag.name == "h1":
            blocks.append(("heading", tag.text))
        elif tag.name == "h2":
            blocks.append(("subheading", tag.text))
        elif tag.name == "p":
            blocks.append(("paragraph", tag.text))
        elif tag.name == "ul":
            for li in tag.find_all("li"):
                blocks.append(("bullet", "• " + li.text))
        elif tag.name == "ol":
            for i, li in enumerate(tag.find_all("li"), 1):
                blocks.append(("bullet", f"{i}. {li.text}"))
        else:
            blocks.append(("paragraph", tag.text.strip()))
    return blocks

# Main function to convert Markdown into PDF using ReportLab
def generate_pdf():
    if not os.path.exists(INPUT_FILE):
        print(f"{INPUT_FILE} not found.")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        md_content = f.read()

    blocks = markdown_to_text_blocks(md_content)

    # Set up PDF document
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=letter,
        rightMargin=72, leftMargin=72,
        topMargin=72, bottomMargin=72
    )

    styles = getSampleStyleSheet()
    flowables = []

    # Render each block of content into PDF
    for block_type, content in blocks:
        if block_type == "heading":
            flowables.append(Paragraph(f"<b><font size=18>{content}</font></b>", styles["Title"]))
        elif block_type == "subheading":
            flowables.append(Paragraph(f"<b><font size=14>{content}</font></b>", styles["Heading2"]))
        elif block_type == "paragraph":
            flowables.append(Paragraph(content, styles["BodyText"]))
        elif block_type == "bullet":
            flowables.append(Paragraph(content, styles["BodyText"]))
        flowables.append(Spacer(1, 0.2 * inch))

    # Build the PDF
    doc.build(flowables)
    print(f"PDF created: {OUTPUT_FILE}")

# Run if script is executed directly
if __name__ == "__main__":
    generate_pdf()
