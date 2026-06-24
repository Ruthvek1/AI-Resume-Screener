from services.gemini_service import analyze_with_gemini
from services.groq_service import analyze_with_groq
from services.openrouter_service import analyze_with_openrouter
from utils.rate_limiter import RateLimiter

gemini_limiter = RateLimiter(requests_per_minute=15)
groq_limiter = RateLimiter(requests_per_minute=30)

async def route_analysis(resume_text: str, job_description: str) -> dict:
    """
    Returns: { result: AnalysisResult, model_used: str }
    """
    # Try Gemini first (best for long resumes)
    if gemini_limiter.allow():
        try:
            result = await analyze_with_gemini(resume_text, job_description)
            return {"result": result, "model_used": "Gemini 2.5 Flash"}
        except Exception as e:
            print(f"[Router] Gemini failed: {e}. Falling to Groq.")

    # Try Groq (fast, good for scoring)
    if groq_limiter.allow():
        try:
            result = await analyze_with_groq(resume_text, job_description)
            return {"result": result, "model_used": "Groq Llama 70B"}
        except Exception as e:
            print(f"[Router] Groq failed: {e}. Falling to OpenRouter.")

    # OpenRouter as final fallback
    result = await analyze_with_openrouter(resume_text, job_description)
    return {"result": result, "model_used": "OpenRouter (Llama 70B)"}








