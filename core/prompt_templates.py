# core/prompt_templates.py

question_template = """
You are a clinical trial research assistant. Given the following user query, search for the most relevant 
information from clinicaltrials.gov and summarize the findings clearly.

Query:
"{query}"

Answer format:
- Summary of the most relevant clinical trials
- Trial Phases, Locations, Enrollment, and Conditions
- Any key eligibility criteria
- (If applicable) Direct links to trial entries
"""

def format_prompt(user_query: str) -> str:
    return question_template.format(query=user_query)
