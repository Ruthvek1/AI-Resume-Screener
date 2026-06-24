from groq import AsyncGroq
from config import settings
from models.response_models import AnalysisResult
import json

client = AsyncGroq(api_key=settings.GROQ_API_KEY)

async def analyze_with_groq(resume_text: str, job_description: str) -> AnalysisResult:
    # Truncate for Groq's 8192 token context limit
    resume_trimmed = resume_text[:4000]
    jd_trimmed = job_description[:2000]

    response = await client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are an ATS resume scoring engine. Always respond with valid JSON only."
            },
            {
                "role": "user",
                "content": f"""Score this resume against the job description.
Return JSON with: match_score, score_breakdown, matching_skills, missing_skills,
extra_skills, ats_keywords, improvement_suggestions, summary, hire_likelihood.

RESUME:
{resume_trimmed}

JOB DESCRIPTION:
{jd_trimmed}"""
            }
        ],
        temperature=0.1,
        max_tokens=3000,
        response_format={"type": "json_object"}
    )

    data = json.loads(response.choices[0].message.content)
    return AnalysisResult(**data)















