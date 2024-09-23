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

1. Install the required packages:

    ```
    pip install -r requirements.txt
    ```
2. Pull the model from Ollama:
    ```
    ollama pull <MODEL_NAME>
    ```
3. Pull the embedding model from Ollama:
    ```
    ollama pull <MODEL_NAME>
    ```

You can get available models from [Ollama Models Library](https://ollama.com/library)

## Environment Setup

Create a `.env` file in the root directory with the following structure:

```
MODEL_NAME=<MODEL_NAME>
EMBEDDING_MODEL_NAME=<EMBEDDING_MODEL_NAME>
MODEL_TEMPERATURE=<TEMPERATURE>
DB_DIR=<PATH_TO_CHROMA_DB>
```

Make sure to replace `your_api_key_here` with your actual API key.

## Running the Application

To run the FastAPI application:

```
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`.

## API Documentation

Check [API Docs](./API.md) for details documentation.

## Project Structure

```
.
├── main.py
├── config.py
├── routers
│   ├── chat.py
│   ├── session.py
│   └── vector_store.py
├── schemas
│   └── chat.py
├── services
│   ├── chat.py
│   ├── file.py
│   ├── session.py
│   └── vector_store.py
├── dependencies.py
├── .env
├── requirements.txt
├── API.md
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