import httpx
from config import settings
from models.response_models import AnalysisResult
import json

async def analyze_with_openrouter(resume_text: str, job_description: str) -> AnalysisResult:
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://yourwebsite.com",
        "X-Title": "AI Resume Screener",
        "Content-Type": "application/json"
    }

    payload = {
        "model": settings.OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "You are an expert ATS scoring AI. Return JSON only."},
            {"role": "user", "content": f"""Analyze resume vs job description.
Return JSON: match_score, matching_skills, missing_skills, improvement_suggestions, summary.

RESUME: {resume_text[:3500]}
JOB DESCRIPTION: {job_description[:2000]}"""}
        ],
        "temperature": 0.1,
        "response_format": {"type": "json_object"}
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        return AnalysisResult(**parsed)















