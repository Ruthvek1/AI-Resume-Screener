from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.pdf_parser import extract_text_from_pdf
from services.model_router import route_analysis
from models.response_models import AnalysisResponse
import time

router = APIRouter(prefix="/api", tags=["analyze"])

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    resume: UploadFile = File(..., description="Resume PDF file"),
    job_description: str = Form(..., description="Job description text")
):
    if not resume.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files accepted.")

    if len(job_description.strip()) < 50:
        raise HTTPException(status_code=400, detail="Job description too short.")

    start_time = time.time()

    # Step 1: Extract text from PDF
    resume_text = await extract_text_from_pdf(resume)

    # Step 2: Route to best available AI model
    output = await route_analysis(resume_text, job_description)

    elapsed_ms = int((time.time() - start_time) * 1000)

    return AnalysisResponse(
        result=output["result"],
        model_used=output["model_used"],
        processing_time_ms=elapsed_ms
    )












