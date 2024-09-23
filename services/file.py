import os
import tempfile
from fastapi import UploadFile
from langchain_core.documents import Document
from langchain_community.document_loaders import JSONLoader, PyPDFLoader, CSVLoader

class FileService:
    def __init__(self):
        self.supported_files = ["application/pdf", "text/csv", "application/json"]

    def _validate_file_type(self, file_type: str) -> None:
        """
        Validates if a file type is supported.

        Args:
            file_type (str): The type of the file.
        """
        if not isinstance(file_type, str):
            raise ValueError("File type must be a string.")
        if file_type not in self.supported_files:
            raise ValueError(f"Unsupported file type: {file_type}.")

    async def _read_file_content(self, file: UploadFile) -> bytes:
        """Reads the content of the uploaded file."""
        return await file.read()

    def _create_temp_file(self, file_content: bytes, filename: str) -> str:
        """Creates a temp file from the uploaded file content and returns the file path."""
        temp_dir = tempfile.mkdtemp()  # Create a temporary directory
        path = os.path.join(temp_dir, filename)  # Create a path for the temp file

        # Write the file content into the temp file
        with open(path, "wb") as f:
            f.write(file_content)
        
        return path

    async def load(self, file: UploadFile) -> list[Document]:
        content_type = file.content_type
        self._validate_file_type(content_type)
        file_content = await self._read_file_content(file)
        file_path = self._create_temp_file(file_content, file.filename)

        if content_type == "application/json":
            return JSONLoader(file_path=file_path, jq_schema='.', text_content=False).load()
        elif content_type == "application/pdf":
            return PyPDFLoader(file_path=file_path).load()
        elif content_type == "text/csv":
            return CSVLoader(file_path=file_path).load()