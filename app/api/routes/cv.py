from typing import Annotated

from fastapi import APIRouter, Form
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile

from app.domain.schemas.cv import CVAnalysisResponse
from app.services.cv_optimization_service import CVAnalysisService
from app.core.logger import logger

router = APIRouter(prefix="/cv", tags=["cv"])

service = CVAnalysisService()


@router.post(
    "/analyze",
    response_model=CVAnalysisResponse,
)
async def analyze_cv(
    file: UploadFile = File(...),
    job_offer: Annotated[
        str | None,
        Form(
            description="Job offer to be analyzed",
            max_length=10000,
            examples=[""],
        ),
    ] = "",
):
    """Analyze a CV and provide insights.
    This endpoint takes a PDF file as input and an optional job offer.
    Calls the CV analysis service that should return a CVAnalysisResponse using langchain.
    """
    logger.info("CV analysis request received", filename=file.filename)
    if file.content_type != "application/pdf":
        logger.error("Invalid file type", file_type=file.content_type)
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported",
        )

    pdf_bytes = await file.read()
    job_offer = job_offer.strip() if job_offer else ""
    logger.info("CV analysis started", job_offer=job_offer, filename=file.filename)
    return await service.analyze(pdf_bytes=pdf_bytes, job_offer=job_offer)
