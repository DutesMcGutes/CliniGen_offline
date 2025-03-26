# 🧬 CliniGen: Structured Clinical Trial Protocol Generator

CliniGen is a fast, editable, and exportable app for generating full clinical trial protocols using GPT-4 Turbo. Unlike typical AI text generators, CliniGen produces sectioned content tailored to trial phase, population, endpoints, and location — structured to match real-world protocols like those used in regulatory and investigator-initiated studies.

Built with [Streamlit](https://streamlit.io), OpenAI GPT-4, and rich export tools.

---

## ✨ Key Features (With How They Work)

### 1. **Structured Protocol Generation**
> 🧠 Instead of a long blob of text, CliniGen builds a protocol as a structured Python dictionary with 14 core fields:
- Title
- Background
- Rationale
- Primary and Secondary Objectives
- Study Design
- Inclusion/Exclusion Criteria
- Intervention and Comparator
- Endpoints
- Safety Monitoring
- Statistical Plan
- Ethical Considerations

Each section is generated individually with tailored prompts and then cleaned up using a post-processing function that removes LLM filler.

Example Use Cases
- Quickly draft a protocol for IRB review
- Generate consistent trial sections across conditions
- Use JSON output to integrate with eCRFs or CTMS tools
- Rapid prototyping for CRO or pharma consulting

---

### 2. **Protocol Editing (Live)**
> Every protocol section is editable right in the browser before download.

- Uses `streamlit-quill` (rich text editor with formatting toolbar)
- Automatically syncs changes into the final export structure
- Falls back to plain `st.text_area()` if the rich editor isn’t available

---

### 3. **Numbered Section Display**
> 📑 Each section is rendered with a numbered heading:
1. Title
2. Background
...
3. Ethical Considerations

This helps align the output to ICH-GCP structure and makes review easier for collaborators.

---

### 4. **DOCX, PDF, and JSON Export**
> 📤 Generate ready-to-use protocol files from your session.

- **DOCX**: Microsoft Word–compatible, with heading styles and spacing
- **PDF**: Unicode-safe (supports characters like μg, ≥, ±); formatted using DejaVuSans
- **JSON**: Structured protocol object useful for APIs, re-import, or version control

All generated files are saved temporarily in `/tmp/` to support Streamlit Cloud deployment.

---

### 5. **Prompt Quality + Cleanup**
> 🔬 All prompts use formal, regulatory-style language. Responses are post-processed to:
- Strip speculative or apologetic AI text
- Enforce clean, concise formatting
- Remove unnecessary filler like "In conclusion..." or "I do not have access..."

The result is output that looks closer to what you'd find in a real protocol.

---

### 6. **Speed + Modularity**
> 🚀 Because each section is generated separately, CliniGen:
- Runs quickly
- Recovers gracefully from partial errors
- Can support “regen just this section” workflows in the future

---

## Setup Instructions

### Installation with Anaconda (recommended)

```bash
conda create -n clinigen python=3.11
conda activate clinigen
pip install -r requirements.txt

### Or through venv

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### Project File Tree

ClinicGen/
├── app.py
├── core/
│   └── protocol_generator.py
├── utils/
│   └── file_exporter.py
│   └── DejaVuSans.ttf
│   └── DejaVuSans-Bold.ttf
├── .env
├── requirements.txt

### Environmental Variables

- Create .env in the root folder
- add OPENAI_API_KEY=your-openai-key-here

### Running the app
streamlit run app.py

and open with http://localhost:8501 in your browser