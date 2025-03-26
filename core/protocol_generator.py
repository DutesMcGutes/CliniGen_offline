# core/protocol_generator.py

import os
from openai import OpenAI
from dotenv import load_dotenv
import re

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_section(prompt: str, model="gpt-4-turbo") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a clinical trial protocol assistant. Write clearly, concisely, and in formal regulatory style."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,
    )
    return response.choices[0].message.content.strip()

def clean_text(text: str) -> str:
    """Remove filler language, apologies, and speculative disclaimers."""
    replacements = [
        r"(?i)i\s+(do|don't|cannot|can't|am unable|have no access)[^\.\n]*[\.\n]",  # remove AI-style disclaimers
        r"(?i)please note[^\.\n]*[\.\n]",
        r"(?i)in conclusion[^\.\n]*[\.\n]",
        r"(?i)this section aims to[^\.\n]*[\.\n]",
        r"(?i)here (is|are)[^\.\n]*[\.\n]"
    ]
    for pattern in replacements:
        text = re.sub(pattern, '', text).strip()
    return text.strip()

def generate_structured_protocol(inputs: dict) -> dict:
    condition = inputs['condition']
    drug = inputs['intervention']
    population = inputs['population']
    comparator = inputs['comparator']
    primary_endpoint = inputs['primary_endpoint']
    phase = inputs['phase']
    study_type = inputs['study_type']
    duration = inputs['duration']
    location = inputs['location']

    prompts = {
        "title": f"Write the full formal title for a {phase} {study_type} evaluating {drug} vs {comparator} in {population} with {condition}.",
        "background": f"Briefly summarize the pathophysiology of {condition}, current standard treatments including {comparator}, and the role of {drug}. Limit to 3 paragraphs.",
        "rationale": f"Justify the need for this study comparing {drug} and {comparator} in {population} with {condition}, using clinical rationale. Include innovation and unmet need.",
        "objectives_primary": f"State the primary objective of the {phase} {study_type} trial in 1–2 sentences.",
        "objectives_secondary": f"List up to 3 secondary objectives related to efficacy, safety, or PK/PD.",
        "study_design": f"Describe the {phase} {study_type} study design including randomization, blinding, arms, duration ({duration}), and overall structure. Write formally.",
        "population_inclusion": f"List 5–7 inclusion criteria for eligible participants: {population} with {condition}.",
        "population_exclusion": f"List 5–7 exclusion criteria for this trial population.",
        "intervention": f"Describe how {drug} and {comparator} will be administered, including route, dose, frequency, and duration. Write clearly for a protocol.",
        "endpoints_primary": f"Define the primary endpoint (e.g., {primary_endpoint}) and explain how and when it will be measured.",
        "endpoints_secondary": f"List up to 3 secondary endpoints and how they will be assessed.",
        "safety_monitoring": f"Outline the safety monitoring plan for this {phase} trial including AE/SAE procedures, labs, DSMB, and follow-up.",
        "statistical_analysis": f"Write the SAP for this {phase} {study_type} trial targeting HbA1c reduction as the primary endpoint. Include methods, populations, and software.",
        "ethical_considerations": f"List the key ethical elements (informed consent, IRB/IEC approval, risk-benefit, rescue meds) for a trial in {location}."
    }

    output = {
        "title": clean_text(generate_section(prompts["title"])),
        "background": clean_text(generate_section(prompts["background"])),
        "rationale": clean_text(generate_section(prompts["rationale"])),
        "objectives": {
            "primary": clean_text(generate_section(prompts["objectives_primary"])),
            "secondary": clean_text(generate_section(prompts["objectives_secondary"])),
        },
        "study_design": clean_text(generate_section(prompts["study_design"])),
        "population": {
            "inclusion_criteria": clean_text(generate_section(prompts["population_inclusion"])),
            "exclusion_criteria": clean_text(generate_section(prompts["population_exclusion"])),
        },
        "intervention": clean_text(generate_section(prompts["intervention"])),
        "endpoints": {
            "primary": clean_text(generate_section(prompts["endpoints_primary"])),
            "secondary": clean_text(generate_section(prompts["endpoints_secondary"])),
        },
        "safety_monitoring": clean_text(generate_section(prompts["safety_monitoring"])),
        "statistical_analysis": clean_text(generate_section(prompts["statistical_analysis"])),
        "ethical_considerations": clean_text(generate_section(prompts["ethical_considerations"])),
    }

    return output
