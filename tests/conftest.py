import pytest
from unittest.mock import patch


@pytest.fixture(autouse=True)
def disable_chroma_directory_creation():

    with patch("app.infra.vectorstore.chroma.Path.mkdir"):
        yield
