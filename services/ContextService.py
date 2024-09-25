import os
import shutil
from typing import List, Optional
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class ContextService:
    def __init__(self, base_dir: Optional[str] = None, embedding_model: Optional[str] = None):
        self.base_dir = base_dir or os.getenv('DB_DIR')
        if not self.base_dir:
            raise ValueError("Base directory must be provided or set in DB_DIR environment variable.")
        self.embedding_model = embedding_model or os.getenv("EMBEDDING_MODEL_NAME")
        if not self.embedding_model:
            raise ValueError("Embedding model must be provided or set in EMBEDDING_MODEL_NAME environment variable.")

    def _validate_context_name(self, context_name: str) -> None:
        if not isinstance(context_name, str) or not context_name.strip():
            raise ValueError("Store name must be a non-empty string.")

    def _get_embeddings(self) -> OllamaEmbeddings:
        return OllamaEmbeddings(model=self.embedding_model, show_progress=True)

    def _get_store_path(self, context_name: str) -> str:
        return os.path.join(self.base_dir, context_name)

    def _get(self, context_name: str) -> Chroma:
        return Chroma(
            collection_name=context_name,
            embedding_function=self._get_embeddings(),
            persist_directory=self._get_store_path(context_name)
        )

    def get_all(self) -> List[str]:
        if not os.path.exists(self.base_dir):
            return []
        return [d for d in os.listdir(self.base_dir) if os.path.isdir(self._get_store_path(d))]

    def get(self, context_name: str) -> Chroma:
        self._validate_context_name(context_name)
        if not self.exists(context_name):
            raise ValueError(f"Vector store '{context_name}' does not exist.")
        return self._get(context_name)

    def exists(self, context_name: str) -> bool:
        self._validate_context_name(context_name)
        return context_name in self.get_all()

    def create(self, context_name: str) -> Chroma:
        self._validate_context_name(context_name)
        if self.exists(context_name):
            raise ValueError(f"Vector store '{context_name}' already exists.")
        return self._get(context_name)

    def update(self, docs: List[Document], context_name: str, chunk_size: int = 1000, chunk_overlap: int = 100) -> None:
        self._validate_context_name(context_name)
        if not self.exists(context_name):
            raise ValueError(f"Vector store '{context_name}' does not exist.")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = text_splitter.split_documents(docs)

        Chroma.from_documents(
            collection_name=context_name,
            documents=chunks,
            embedding=self._get_embeddings(),
            persist_directory=self._get_store_path(context_name)
        )

    def delete(self, context_name: str) -> None:
        self._validate_context_name(context_name)
        if not self.exists(context_name):
            raise ValueError(f"Vector store '{context_name}' does not exist.")

        store_dir = self._get_store_path(context_name)
        try:
            shutil.rmtree(store_dir)
            print(f"Vector store '{context_name}' successfully deleted.")
        except OSError as e:
            raise ValueError(f"Failed to delete vector store '{context_name}': {e}")