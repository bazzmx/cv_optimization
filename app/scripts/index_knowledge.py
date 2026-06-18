from pathlib import Path

from app.core.logger import logger
from app.infra.vectorstore.chroma import ChromaService

ROOT_DIR = Path(__file__).resolve().parents[2]
KNOWLEDGE_PATH = ROOT_DIR / "knowledge"


def index_knowledge_if_needed():
    vectors = ChromaService()
    count = vectors.vectorstore._collection.count()

    if count > 0:
        logger.info("Knowledge base already indexed")
        return

    logger.info("Building knowledge base")

    for file in KNOWLEDGE_PATH.glob("*.txt"):
        logger.info(f"Indexing {file.name}")
        text = file.read_text(encoding="utf-8")

        vectors.add_documents(text)

    logger.info("Knowledge base initialized")


if __name__ == "__main__":
    index_knowledge_if_needed()
