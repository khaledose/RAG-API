import os
from uuid import UUID
from typing import AsyncGenerator, Dict, Optional, Any
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.retrievers import RetrieverOutputLike
from langchain_core.runnables import Runnable
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_ollama.llms import OllamaLLM
from services.SessionService import SessionService
from services.ContextService import ContextService
from config import SYSTEM_PROMPT

class ChatService:
    def __init__(
            self, 
            context_service: ContextService, 
            session_service: SessionService, 
            model_name: Optional[str] = None, 
            model_temperature: Optional[str] = None):
        self.context_service = context_service
        self.session_service = session_service
        self.model_name = model_name or os.getenv('MODEL_NAME')
        self.model_temperature = float(model_temperature or os.getenv('MODEL_TEMPERATURE'))
        self.llm: Optional[OllamaLLM] = None
        self.retriever = None
        self.rag_chain = None
    
    def _create_llm(self) -> None:
        self.llm = OllamaLLM(
            model=self.model_name,
            temperature=self.model_temperature,
        )

    def _create_retriever(self, context_name: str) -> None:
        vectorstore = self.context_service.get(context_name)
        self.retriever = vectorstore.as_retriever()

    def _get_system_prompt(self, prompt_key: str = "default") -> str:
        return SYSTEM_PROMPT.get(prompt_key, SYSTEM_PROMPT["default"])

    def _create_question_contextualizer(self) -> RetrieverOutputLike:
        prompt = self._get_system_prompt("history")
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt),
                MessagesPlaceholder("history"),
                ("human", "{input}"),
            ]
        )
        return create_history_aware_retriever(self.llm, self.retriever, contextualize_q_prompt)

    def _create_qa_chain(self, context_name: str) -> Runnable[Dict[str, Any], Any]:
        prompt = self._get_system_prompt(context_name)
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt),
                MessagesPlaceholder("history"),
                ("human", "{input}"),
            ]
        )
        return create_stuff_documents_chain(self.llm, qa_prompt)

    def build(self, context_name: str) -> None:
        if not self.llm:
            self._create_llm()
        self._create_retriever(context_name)
        history_aware_retriever = self._create_question_contextualizer()
        qa_chain = self._create_qa_chain(context_name)
        self.rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

    async def chat(self, session_id: UUID, question: str) -> AsyncGenerator[str, None]:
        if not self.rag_chain:
            raise ValueError("RAG chain not built. Call build() method first.")

        runnable = RunnableWithMessageHistory(
            self.rag_chain,
            self.session_service.get,
            input_messages_key="input",
            history_messages_key="history",
            output_messages_key="answer",
        )

        async for token in runnable.astream(
            {"input": question}, 
            {"configurable": {"session_id": session_id}}
        ):
            if 'answer' in token:
                yield token['answer']
