# FastAPI RAG Application

This is a FastAPI application that implements a Retrieval-Augmented Generation (RAG) system with vector store capabilities.

## Table of Contents

1. [Installation](#installation)
2. [Environment Setup](#environment-setup)
3. [Running the Application](#running-the-application)
4. [API Documentation](#api-documentation)
5. [Project Structure](#project-structure)
6. [Contributing](#contributing)
7. [License](#license)

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
    ollama pull <EMBEDDING_MODEL_NAME>
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

## Running the Application

To run the FastAPI application:

```
uvicorn main:app --reload
```

Or you can make it available for the local network:

```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Documentation

Check [API Docs](./API.md) for details documentation.

## Project Structure

```
.
├── main.py
├── config.py
├── routers
│   ├── ChatRouter.py
│   ├── SessionRouter.py
│   └── ContextRouter.py
├── schemas
│   └── Request.py
├── services
│   ├── ChatService.py
│   ├── DocumentService.py
│   ├── SessionService.py
│   └── ContextService.py
├── dependencies.py
├── .env
├── requirements.txt
├── API.md
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.