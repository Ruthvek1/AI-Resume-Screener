import pdfplumber
import io
from fastapi import UploadFile, HTTPException

async def extract_text_from_pdf(file: UploadFile) -> str:
    """
    Extract clean, structured text from uploaded resume PDF.
    Handles multi-column layouts, tables, and bullet points.
    Uses pdfplumber for accurate text extraction with layout preservation.
    """
    if file.size > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(status_code=413, detail="PDF too large. Max 10MB.")

    content = await file.read()
    text_parts = []

    with pdfplumber.open(io.BytesIO(content)) as pdf:
        for page_num, page in enumerate(pdf.pages):
            # Extract text preserving layout
            text = page.extract_text(
                x_tolerance=3,
                y_tolerance=3,
                layout=True,
                x_density=7.25,
                y_density=13
            )
            if text:
                text_parts.append(f"--- Page {page_num + 1} ---\n{text}")

            # Also extract tables if present (skills tables, etc.)
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    row_text = " | ".join([cell or "" for cell in row])
                    text_parts.append(row_text)

    full_text = "\n\n".join(text_parts)

    if not full_text.strip():
        raise HTTPException(
            status_code=422,
            detail="Could not extract text from PDF. It may be scanned/image-based."
        )

    return full_text














