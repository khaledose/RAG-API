# API Endpoints Documentation

## Chat Endpoints

### Build Chat
- **POST** `/chat/build`
- Builds a chat session for a specific vector store.
- Request body: `{ "store_name": "string" }`
- Response: Confirmation message

### Chat
- **POST** `/chat`
- Initiates a chat session.
- Request body: `{ "store_name": "string", "session_id": "UUID", "question": "string" }`
- Response: Streaming response with chat replies

## Session Endpoints

### Get All Sessions
- **GET** `/session/`
- Retrieves all active session IDs.

### Get Session
- **GET** `/session/{session_id}`
- Retrieves chat history for a specific session.
- Path parameter: `session_id` (UUID)

### Create Session
- **POST** `/session/`
- Creates a new session.
- Response: New session ID

### Delete Session
- **DELETE** `/session/{session_id}`
- Deletes a specific session.
- Path parameter: `session_id` (UUID)

### Clear All Sessions
- **DELETE** `/session`
- Clears all active sessions.

## Vector Store Endpoints

### Get All Vector Stores
- **GET** `/vector_stores`
- Retrieves all vector stores.

### Create Vector Store
- **POST** `/vector_stores`
- Creates a new vector store.
- Request body: `{ "store_name": "string" }`

### Update Vector Store
- **POST** `/vector_stores/{store_name}`
- Updates a vector store with new file data.
- Path parameter: `store_name`
- Request body: File upload

### Delete Vector Store
- **DELETE** `/vector_stores`
- Deletes a specific vector store.
- Request body: `{ "store_name": "string" }`

Note: All endpoints may return appropriate HTTP error codes (e.g., 404, 500) with error details in case of failures.