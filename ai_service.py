import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load .env from current folder
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

def get_client():
    return genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )


def generate_health_remark(glucose, haemoglobin, cholesterol):

    prompt = f"""
You are an experienced healthcare assistant.

Analyze the patient's blood report.

Blood Report:

Glucose: {glucose} mg/dL

Haemoglobin: {haemoglobin} g/dL

Cholesterol: {cholesterol} mg/dL

Return your answer in markdown using EXACTLY this format.

# 🩺 Health Status

(Overall condition)

# ⚠ Findings

• Finding 1

• Finding 2

# 💡 Recommendations

• Recommendation 1

• Recommendation 2

# 📌 Disclaimer

Mention that this is not a medical diagnosis and consultation with a healthcare professional is recommended.

Keep response under 180 words.
"""

    client = get_client()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text