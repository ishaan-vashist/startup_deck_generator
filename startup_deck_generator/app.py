import streamlit as st
import os

# Import core logic for generating markdown and PDF
from main import run_deck_generation
from pdf_generator import generate_pdf

# Output file paths
OUTPUT_MD = "deck_output.md"
OUTPUT_PDF = "deck_output.pdf"

# Configure Streamlit page settings
st.set_page_config(page_title="Startup Deck Generator", layout="centered")

# Page title
st.title("AI-Powered Startup Deck Generator")

# Form UI: input field for startup idea
with st.form("startup_form"):
    idea = st.text_area("Enter your startup idea", height=150)
    submitted = st.form_submit_button("Generate Pitch Deck")

# Trigger generation process after form submission
if submitted and idea:
    # Display progress spinner
    with st.spinner("Generating your deck..."):
        # Run CrewAI pipeline to generate markdown
        run_deck_generation(idea)

        # Convert markdown to PDF
        generate_pdf()

    # Success message after generation is complete
    st.success("Pitch deck generation complete.")

    # Preview generated markdown deck
    if os.path.exists(OUTPUT_MD):
        st.markdown("Markdown Preview")
        with open(OUTPUT_MD, "r", encoding="utf-8") as f:
            st.code(f.read(), language="markdown")

    # Provide PDF download button
    if os.path.exists(OUTPUT_PDF):
        with open(OUTPUT_PDF, "rb") as pdf_file:
            st.download_button(
                label="Download Pitch Deck (PDF)",
                data=pdf_file,
                file_name="startup_pitch_deck.pdf",
                mime="application/pdf"
            )
