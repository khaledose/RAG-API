# FastAPI RAG Application

This is a FastAPI application that implements a Retrieval-Augmented Generation (RAG) system with vector store capabilities.

## Table of Contents

1. [Installation](#installation)
2. [Environment Setup](#environment-setup)
3. [Running the Application](#running-the-application)
4. [API Documentation](#api-documentation)
5. [Project Structure](#project-structure)
6. [Configuration](#configuration)
7. [Contributing](#contributing)
8. [License](#license)

## Installation

Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Environment Setup

Create a `.env` file in the root directory with the following structure:

```
API_URL=<LM_STUDIO_SERVER_URL>
API_KEY=<CAN_BE_ANYTHING>
MODEL_TEMPERATURE=<TEMPERATURE>
DB_DIR=<PATH_TO_CHROMA_DB>
EMBEDDING_MODEL=<EMBEDDING_MODEL_NAME>
```

Make sure to replace `your_api_key_here` with your actual API key.

## Running the Application

To run the FastAPI application:

```
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`.

## API Documentation

### Vector Store Endpoints

- `GET /vector_stores`: Retrieve all vector stores
- `POST /vector_stores`: Create a new vector store
  - Body: `{"store_name": "your_store_name"}`
- `POST /vector_stores/{store_name}/{file_type}`: Update a vector store with a file
  - Path parameters: `store_name`, `file_type`
  - Body: File upload
- `DELETE /vector_stores`: Delete a vector store
  - Body: `{"store_name": "your_store_name"}`

### RAG Endpoints

- `POST /rag/build`: Build a RAG chain for a vector store
  - Body: `{"store_name": "your_store_name"}`
- `POST /rag/chat`: Chat with the RAG system
  - Body: `{"store_name": "your_store_name", "session_id": "unique_session_id", "question": "Your question here"}`

For detailed API documentation, visit `http://localhost:8000/docs` after starting the application.

## Project Structure

```
.
├── main.py
├── config.py
├── routers
│   ├── rag.py
│   └── vector_store.py
├── schemas
│   └── chat.py
├── services
│   ├── rag.py
│   └── vector_store.py
├── utils
│   └── files.py
├── dependencies.py
├── .env
├── requirements.txt
└── README.md
```

## Configuration

The `config.py` file contains important system prompts for the RAG system:

- `SYSTEM_PROMPT`: This is used to instruct the AI model on how to answer questions based on the retrieved context. It must contain `{context}` which is the placeholder for embeddings to be added to the prompt.
- `HISTORY_PROMPT`: This is used to reformulate user questions in the context of the chat history, ensuring that the questions are standalone and can be understood without additional context.

You can modify these prompts in the `config.py` file to adjust the behavior of your RAG system as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.