from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings
from app.core.logger import logger


class ChromaService:
    def __init__(self):
        """Initialize the Chroma service with the appropriate embeddings.
        Currently, we only support Ollama, supporting multiple embeddings means having multiple
        chroma databases, which for the purpose of this project is not required.
        """
        self.embeddings = OllamaEmbeddings(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_EMBEDDING_MODEL,
        )

        Path(settings.chroma_path).mkdir(
            parents=True,
            exist_ok=True,
        )

        self.vectorstore = Chroma(
            persist_directory=settings.chroma_path,
            embedding_function=self.embeddings,
        )

    def add_documents(self, text: str):
        """Add documents to the vector store.
        Chunks the text into smaller chunks and adds them to the vector store.
        """
        logger.info("Adding documents to the vector store")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )

        chunks = splitter.split_text(text)

        docs = [Document(page_content=chunk) for chunk in chunks]

        self.vectorstore.add_documents(docs)

    def similarity_search(self, query: str, k: int = 5):
        """Perform similarity search in the vector store."""
        logger.info("Performing similarity search")
        return self.vectorstore.similarity_search(query, k=k)

    def clear(self):
        """Clear the vector store."""
        self.vectorstore.delete_collection()
        self.vectorstore = Chroma(
            persist_directory=settings.chroma_path,
            embedding_function=self.embeddings,
        )
