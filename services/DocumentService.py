import os
import tempfile
from typing import List, Dict, Any
from fastapi import UploadFile
from langchain_community.document_loaders import (
    JSONLoader, PyPDFLoader, CSVLoader, TextLoader, WebBaseLoader
)
from langchain_core.documents import Document

class DocumentService:
    def __init__(self):
        self.supported_formats: Dict[str, Any] = {
            "application/pdf": PyPDFLoader,
            "text/csv": CSVLoader,
            "application/json": JSONLoader,
            "text/plain": TextLoader
        }

    def _validate_format(self, content_type: str) -> None:
        """
        Validates if a content type is supported.

        Args:
            content_type (str): The MIME type of the content.

        Raises:
            ValueError: If the content type is not supported or not a string.
        """
        if not isinstance(content_type, str):
            raise ValueError("Content type must be a string.")
        if content_type not in self.supported_formats:
            raise ValueError(f"Unsupported content type: {content_type}. Supported types are: {', '.join(self.supported_formats.keys())}.")

    def _create_temp_file(self, file_content: bytes, filename: str) -> str:
        """
        Creates a temp file from the uploaded file content and returns the file path.

        Args:
            file_content (bytes): The content of the file.
            filename (str): The name of the file.

        Returns:
            str: The path to the temporary file.
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
            temp_file.write(file_content)
            return temp_file.name

    async def load_file(self, file: UploadFile) -> List[Document]:
        """
        Loads a file and returns a list of Documents.

        Args:
            file (UploadFile): The uploaded file.

        Returns:
            List[Document]: A list of loaded documents.

        Raises:
            ValueError: If the file type is not supported.
        """
        content_type = file.content_type
        self._validate_format(content_type)
        file_content = await file.read()
        file_path = self._create_temp_file(file_content, file.filename)

        try:
            loader_class = self.supported_formats[content_type]
            if content_type == "application/json":
                return loader_class(file_path=file_path, jq_schema='.', text_content=False).load()
            else:
                return loader_class(file_path=file_path).load()
        finally:
            os.unlink(file_path)  # Clean up the temporary file

    async def load_web(self, url: str) -> List[Document]:
        """
        Loads content from a web URL and returns a list of Documents.

        Args:
            url (str): The URL to load content from.

        Returns:
            List[Document]: A list of loaded documents.
        """
        return WebBaseLoader(url).load()

    def add_format(self, content_type: str, loader_class: Any) -> None:
        """
        Adds a new content type and its corresponding loader to the supported formats.

        Args:
            content_type (str): The MIME type of the content.
            loader_class (Any): The loader class for the content type.
        """
        self.supported_formats[content_type] = loader_class