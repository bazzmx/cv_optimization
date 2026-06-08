from pathlib import Path

from app.domain.schemas.cv import CVAnalysisResponse
from app.infra.llm.provider import get_llm
from app.infra.pdf.extractor import extract_pdf_text
from app.infra.vectorstore.chroma import ChromaService
from app.core.logger import logger


class CVAnalysisService:
    """CV analysis service.
    This service takes a CV in PDF format and an optional job offer, analyzes the CV using a language model,
    and provides insights on how to optimize the CV for ATS and HR specialists.
    """

    def __init__(self):
        self.llm = get_llm()
        self.vectorstore = ChromaService()

    def _load_knowledge_base(self):
        """Load knowledge base from the knowledge folder."""
        logger.info("Loading knowledge base from the knowledge folder")
        knowledge_path = Path("knowledge")

        for file in knowledge_path.glob("*.txt"):
            content = file.read_text(encoding="utf-8")
            self.vectorstore.add_documents(content)

    async def analyze(
        self, pdf_bytes: bytes, job_offer: str | None = None
    ) -> CVAnalysisResponse:
        """Analyze a CV and provide insights.
        Takes as input a PDF file and an optional job offer.
        """

        logger.info("CV analysis started")

        self._load_knowledge_base()
        cv_text = extract_pdf_text(pdf_bytes)
        self.vectorstore.add_documents(cv_text)

        retrieved_docs = self.vectorstore.similarity_search(
            query="CV best practices and ATS optimization",
            k=8,
        )

        context = "\n\n".join(doc.page_content for doc in retrieved_docs)

        structured_llm = self.llm.with_structured_output(
            CVAnalysisResponse, method="json_schema"
        )

        prompt = f"""
                    You are an automated HR specialist and ATS optimization expert that returns JSON-only response API. 
                
                    Analyze the following CV and adjust your insights if a job offer is provided.
                    
                    Evaluate:
                    - structure
                    - clarity
                    - ATS compatibility
                    - quantified achievements
                    - grammar
                    - missing sections
                    - technical skills presentation
                    - readability
                    
                    ALWAYS MUST Return:
                    - concise summary
                    - list of strengths
                    - list of improvements. CRITICAL, never return an empty list.
                    
                    Knowledge base:
                    {context}
                    
                    CV:
                    {cv_text}
                    
                    Job offer:
                    {job_offer if job_offer else "N/A"}
                    
                    You MUST respond with valid JSON and nothing else.
                    No markdown, no explanation, no code blocks — just raw JSON.
                    
                    Schema:
                    
                    {{
                      "summary": "...",
                      "strengths": ["...", "...", "..."],
                      "improvements": [
                        {{
                          "category": "...",
                          "issue": "...",
                          "recommendation": "...",
                          "priority": 1
                        }}
                      ]
                    }}
                    
                    Do not include any extra text.
                    If you fail, return:
                    
                    {{
                      "summary": "",
                      "strengths": [],
                      "improvements": []
                    }}
                
                """

        response = structured_llm.invoke(prompt)
        logger.info("CV analysis completed")
        return response
