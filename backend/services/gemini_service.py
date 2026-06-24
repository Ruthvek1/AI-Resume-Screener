import google.generativeai as genai
from config import settings
from models.response_models import AnalysisResult

genai.configure(api_key=settings.GEMINI_API_KEY)

ANALYSIS_PROMPT = """
You are an expert ATS (Applicant Tracking System) and career coach AI.

Analyze the resume below against the provided job description.
Return ONLY a valid JSON object with this exact structure:

{
  "match_score": <integer 0-100>,
  "score_breakdown": {
    "skills_match": <integer 0-100>,
    "experience_match": <integer 0-100>,
    "education_match": <integer 0-100>,
    "keyword_density": <integer 0-100>
  },
  "matching_skills": [<list of skills found in both resume and JD>],
  "missing_skills": [<list of skills in JD not found in resume>],
  "extra_skills": [<list of notable skills in resume not in JD>],
  "ats_keywords": {
    "found": [<keywords present in resume>],
    "missing": [<critical keywords absent from resume>]
  },
  "experience_analysis": "<2-3 sentence analysis of experience fit>",
  "improvement_suggestions": [
    {
      "section": "<Resume section name>",
      "original": "<Example of weak bullet point>",
      "improved": "<AI-rewritten stronger version>",
      "reason": "<Why this change helps>"
    }
  ],
  "summary": "<3-sentence executive summary of overall fit>",
  "hire_likelihood": "<Unlikely | Possible | Likely | Strong>"
}

RESUME:
{resume}

JOB DESCRIPTION:
{job_description}

Return ONLY the JSON. No explanation, no markdown fences.
"""

async def analyze_with_gemini(resume_text: str, job_description: str) -> AnalysisResult:
    model = genai.GenerativeModel(
        model_name=settings.GEMINI_MODEL,
        generation_config={
            "temperature": 0.2,       # Low for consistent scoring
            "max_output_tokens": 4096,
            "response_mime_type": "application/json"
        }
    )

    prompt = ANALYSIS_PROMPT.format(
        resume=resume_text[:50000],  # Gemini 2.5 Flash handles 1M tokens
        job_description=job_description[:8000]
    )

    response = model.generate_content(prompt)
    import json
    text = response.text
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Fallback to repair json or raise
        print(f"Failed to parse Gemini output: {text}")
        raise
    return AnalysisResult(**data)















