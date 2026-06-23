import pytest
from unittest.mock import MagicMock, patch
from app.services.cv_optimization_service import CVAnalysisService


@pytest.mark.asyncio
@patch("app.services.cv_optimization_service.extract_pdf_text")
@patch("app.services.cv_optimization_service.ChromaService")
@patch("app.services.cv_optimization_service.get_llm")
async def test_analyze(
    mock_get_llm,
    mock_chroma_service,
    mock_extract_pdf,
):

    mock_extract_pdf.return_value = "my cv"

    doc = MagicMock()
    doc.page_content = "best practices"

    vectorstore = MagicMock()
    vectorstore.similarity_search.return_value = [doc]

    mock_chroma_service.return_value = vectorstore

    response = MagicMock()

    structured_llm = MagicMock()
    structured_llm.invoke.return_value = response

    llm = MagicMock()
    llm.with_structured_output.return_value = structured_llm

    mock_get_llm.return_value = llm

    service = CVAnalysisService()

    result = await service.analyze(b"pdf bytes", "python developer")

    assert result == response

    mock_extract_pdf.assert_called_once()

    vectorstore.similarity_search.assert_called_once_with(
        query="CV best practices and ATS optimization",
        k=8,
    )

    llm.with_structured_output.assert_called_once()
    structured_llm.invoke.assert_called_once()


@pytest.mark.asyncio
@patch("app.services.cv_optimization_service.extract_pdf_text")
@patch("app.services.cv_optimization_service.ChromaService")
@patch("app.services.cv_optimization_service.get_llm")
async def test_analyze_without_job_offer(
    mock_get_llm,
    mock_chroma_service,
    mock_extract_pdf,
):

    mock_extract_pdf.return_value = "my cv"

    doc = MagicMock()
    doc.page_content = "best practices"

    vectorstore = MagicMock()
    vectorstore.similarity_search.return_value = [doc]

    mock_chroma_service.return_value = vectorstore

    response = MagicMock()

    structured_llm = MagicMock()
    structured_llm.invoke.return_value = response

    llm = MagicMock()
    llm.with_structured_output.return_value = structured_llm

    mock_get_llm.return_value = llm

    service = CVAnalysisService()

    await service.analyze(b"fake pdf")

    prompt = structured_llm.invoke.call_args[0][0]

    assert "N/A" in prompt


@pytest.mark.asyncio
@patch("app.services.cv_optimization_service.extract_pdf_text")
@patch("app.services.cv_optimization_service.ChromaService")
@patch("app.services.cv_optimization_service.get_llm")
async def test_analyze_with_job_offer(
    mock_get_llm,
    mock_chroma_service,
    mock_extract_pdf,
):

    mock_extract_pdf.return_value = "my cv"

    doc = MagicMock()
    doc.page_content = "best practices"

    vectorstore = MagicMock()
    vectorstore.similarity_search.return_value = [doc]

    mock_chroma_service.return_value = vectorstore

    response = MagicMock()

    structured_llm = MagicMock()
    structured_llm.invoke.return_value = response

    llm = MagicMock()
    llm.with_structured_output.return_value = structured_llm

    mock_get_llm.return_value = llm

    service = CVAnalysisService()

    await service.analyze(
        b"fake pdf",
        "Senior Python Developer",
    )

    prompt = structured_llm.invoke.call_args[0][0]

    assert "Senior Python Developer" in prompt


@pytest.mark.asyncio
@patch("app.services.cv_optimization_service.extract_pdf_text")
@patch("app.services.cv_optimization_service.ChromaService")
@patch("app.services.cv_optimization_service.get_llm")
async def test_analyze_builds_context_from_retrieved_documents(
    mock_get_llm,
    mock_chroma_service,
    mock_extract_pdf,
):

    mock_extract_pdf.return_value = "my cv"

    doc1 = MagicMock()
    doc1.page_content = "chunk1"

    doc2 = MagicMock()
    doc2.page_content = "chunk2"

    doc3 = MagicMock()
    doc3.page_content = "chunk3"

    vectorstore = MagicMock()
    vectorstore.similarity_search.return_value = [
        doc1,
        doc2,
        doc3,
    ]

    mock_chroma_service.return_value = vectorstore

    response = MagicMock()

    structured_llm = MagicMock()
    structured_llm.invoke.return_value = response

    llm = MagicMock()
    llm.with_structured_output.return_value = structured_llm

    mock_get_llm.return_value = llm

    service = CVAnalysisService()

    await service.analyze(b"fake pdf")

    prompt = structured_llm.invoke.call_args[0][0]

    assert "chunk1" in prompt
    assert "chunk2" in prompt
    assert "chunk3" in prompt
