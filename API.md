# API Endpoints Documentation

## Chat Endpoints

### Build Chat
- **POST** `/chat/build`
- Builds a chat session for a specific context.
- Request body: `{ "context_name": "string" }`
- Response: Confirmation message

### Chat
- **POST** `/chat`
- Initiates a chat session.
- Request body: `{ "context_name": "string", "session_id": "UUID", "question": "string" }`
- Response: Streaming response with chat replies

## Session Endpoints

### Get All Sessions
- **GET** `/sessions`
- Retrieves all active session IDs.

### Get Session
- **GET** `/sessions/{session_id}`
- Retrieves chat history for a specific session.
- Path parameter: `session_id` (UUID)

### Create Session
- **POST** `/sessions`
- Creates a new session.
- Response: New session ID

### Delete Session
- **DELETE** `/sessions/{session_id}`
- Deletes a specific session.
- Path parameter: `session_id` (UUID)

### Clear All Sessions
- **DELETE** `/sessions`
- Clears all active sessions.

## Context Endpoints

### Get All Contexts
- **GET** `/contexts`
- Retrieves all contexts.

### Create Context
- **POST** `/contexts`
- Creates a new context.
- Request body: `{ "context_name": "string" }`

### Update Context
- **POST** `/contexts/file/{context_name}`
- Updates a context with new file data.
- Path parameter: `context_name`
- Request body: File upload

### Delete Context
- **DELETE** `/contexts/{context_name}`
- Deletes a specific context.
- Path parameter: `context_name`

Note: All endpoints may return appropriate HTTP error codes (e.g., 404, 500) with error details in case of failures.