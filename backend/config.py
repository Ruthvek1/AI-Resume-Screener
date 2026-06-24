from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Keys
    GEMINI_API_KEY: str = "your_gemini_key"
    GROQ_API_KEY: str = "your_groq_key"
    OPENROUTER_API_KEY: str = "your_openrouter_key"

    # Model names
    GEMINI_MODEL: str = "gemini-2.5-flash"
    GROQ_MODEL: str = "llama3-70b-8192"
    OPENROUTER_MODEL: str = "meta-llama/llama-3-70b-instruct"

    # Limits
    MAX_PDF_SIZE_MB: int = 10
    MAX_JD_LENGTH: int = 8000
    CACHE_TTL_SECONDS: int = 300

    # Rate limits (requests per minute)
    GEMINI_RPM: int = 15
    GROQ_RPM: int = 30

    class Config:
        env_file = ".env"

settings = Settings()





