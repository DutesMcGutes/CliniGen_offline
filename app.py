import streamlit as st
from core.protocol_generator import generate_structured_protocol
from utils.file_exporter import (
    save_structured_protocol_as_docx,
    save_structured_protocol_as_pdf,
    save_protocol_as_json,
)
from streamlit_quill import st_quill
import pandas as pd

st.set_page_config(page_title="CliniGen", layout="wide")
st.title("CliniGen")

mode = st.sidebar.radio("Choose a mode", ["Generate Trial Protocol", "Query Clinical Trials"], index=0)

# === STRUCTURED PROTOCOL BUILDER ===
if mode == "Generate Trial Protocol":
    st.subheader("Structured Clinical Trial Protocol Generator")

    with st.form("protocol_form"):
        condition = st.text_input("Condition", value="Type 2 Diabetes")
        population = st.text_input("Target Population", value="Adults aged 40-65 with uncontrolled diabetes")
        intervention = st.text_input("Intervention", value="A novel GLP-1 receptor agonist")
        comparator = st.text_input("Comparator", value="Standard metformin treatment")
        primary_endpoint = st.text_input("Primary Endpoint", value="HbA1c reduction after 12 weeks")
        phase = st.selectbox("Trial Phase", ["Phase 1", "Phase 2", "Phase 3", "Phase 4"])
        study_type = st.selectbox("Study Design Type", ["Randomized Controlled Trial", "Single-Arm", "Crossover", "Observational"])
        duration = st.text_input("Study Duration", value="6 months")
        location = st.text_input("Location", value="United States")
        submitted = st.form_submit_button("Generate Structured Protocol")

    if submitted:
        inputs = {
            "condition": condition,
            "population": population,
            "intervention": intervention,
            "comparator": comparator,
            "primary_endpoint": primary_endpoint,
            "phase": phase,
            "study_type": study_type,
            "duration": duration,
            "location": location
        }
        with st.spinner("Generating protocol..."):
            structured_protocol = generate_structured_protocol(inputs)
            st.session_state["protocol"] = structured_protocol
            st.session_state["inputs"] = inputs

    if "protocol" in st.session_state:
        st.markdown("## 📝 Editable Clinical Trial Protocol")

        protocol = st.session_state["protocol"]

        # Editable Sections with Numbered Headings
        def editable_section(number, title, key, default):
            st.markdown(f"### {number}. {title}")
            content = st_quill(value=default, html=False, key=key)
            return content or default

        edited = {
            "title": editable_section("1", "Title", "title", protocol["title"]),
            "background": editable_section("2", "Background", "background", protocol["background"]),
            "rationale": editable_section("3", "Rationale", "rationale", protocol["rationale"]),
            "objectives": {
                "primary": editable_section("4", "Primary Objective", "obj_primary", protocol["objectives"]["primary"]),
                "secondary": editable_section("5", "Secondary Objectives", "obj_secondary", protocol["objectives"]["secondary"]),
            },
            "study_design": editable_section("6", "Study Design", "study_design", protocol["study_design"]),
            "population": {
                "inclusion_criteria": editable_section("7", "Inclusion Criteria", "inclusion", protocol["population"]["inclusion_criteria"]),
                "exclusion_criteria": editable_section("8", "Exclusion Criteria", "exclusion", protocol["population"]["exclusion_criteria"]),
            },
            "intervention": editable_section("9", "Intervention", "intervention", protocol["intervention"]),
            "endpoints": {
                "primary": editable_section("10", "Primary Endpoint", "ep_primary", protocol["endpoints"]["primary"]),
                "secondary": editable_section("11", "Secondary Endpoints", "ep_secondary", protocol["endpoints"]["secondary"]),
            },
            "safety_monitoring": editable_section("12", "Safety Monitoring", "safety", protocol["safety_monitoring"]),
            "statistical_analysis": editable_section("13", "Statistical Analysis", "stats", protocol["statistical_analysis"]),
            "ethical_considerations": editable_section("14", "Ethical Considerations", "ethics", protocol["ethical_considerations"]),
        }

        st.markdown("---")
        st.markdown("### Download Protocol")

        docx_path = save_structured_protocol_as_docx(edited)
        pdf_path = save_structured_protocol_as_pdf(edited)
        json_path = save_protocol_as_json(st.session_state["inputs"], edited)

        with open(docx_path, "rb") as docx_file:
            st.download_button("📄 Download DOCX", docx_file, file_name="structured_protocol.docx")

        with open(pdf_path, "rb") as pdf_file:
            st.download_button("📄 Download PDF", pdf_file, file_name="structured_protocol.pdf")

        with open(json_path, "rb") as json_file:
            st.download_button("📄 Download JSON", json_file, file_name="structured_protocol.json")

# === Placeholder for Q&A Mode ===
else:
    st.subheader("🧪 Clinical Trials Q&A coming soon...")
