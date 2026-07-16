import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load .env
load_dotenv(dotenv_path=Path(__file__).parent / ".env")


def get_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise Exception("GEMINI_API_KEY not found in .env file")

    return genai.Client(api_key=api_key)


def generate_health_remark(glucose, haemoglobin, cholesterol):

    prompt = f"""
You are a healthcare assistant.

Patient Blood Report

Glucose: {glucose} mg/dL
Haemoglobin: {haemoglobin} g/dL
Cholesterol: {cholesterol} mg/dL

Generate the report exactly in this format:

Health Status:
(one sentence)

Findings:
(two short sentences)

Recommendations:
(three short recommendations)

Disclaimer:
(one sentence)

Keep the entire response under 120 words.
Do not use markdown.
Do not use HTML.
Do not use bullet symbols.
"""

    client = get_client()

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=180,
        ),
    )

    return response.text