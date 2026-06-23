from unittest.mock import MagicMock, patch
from app.infra.vectorstore.chroma import ChromaService


@patch("app.infra.vectorstore.chroma.Path.mkdir")
@patch("app.infra.vectorstore.chroma.Chroma")
def test_add_documents(mock_chroma, mock_mkdir):

    vectorstore = MagicMock()
    mock_chroma.return_value = vectorstore

    service = ChromaService()

    service.add_documents("a" * 5000)

    mock_mkdir.assert_called_once()

    assert vectorstore.add_documents.called


@patch("app.infra.vectorstore.chroma.Chroma")
def test_similarity_search(mock_chroma):

    vectorstore = MagicMock()
    mock_chroma.return_value = vectorstore

    docs = [MagicMock(page_content="doc1")]

    vectorstore.similarity_search.return_value = docs

    service = ChromaService()

    result = service.similarity_search(
        query="python",
        k=3,
    )

    vectorstore.similarity_search.assert_called_once_with(
        "python",
        k=3,
    )

    assert result == docs


@patch("app.infra.vectorstore.chroma.Chroma")
def test_clear(mock_chroma):

    vectorstore = MagicMock()

    mock_chroma.return_value = vectorstore

    service = ChromaService()

    service.clear()

    vectorstore.delete_collection.assert_called_once()

    assert mock_chroma.call_count == 2
