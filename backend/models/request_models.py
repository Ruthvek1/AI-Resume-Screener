from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    job_description: str = Field(..., min_length=50, description="The job description text")



