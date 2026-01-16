# InstaIntelli AI Processing Service

## Overview

The AI Processing Service is a FastAPI-based microservice that handles AI-powered processing of social media posts for the InstaIntelli platform. This service is responsible for generating captions, creating embeddings, and storing them in a vector database for future similarity searches.

## What This Service Does

This service performs three main operations:

1. **Caption Generation**: Automatically generates engaging captions for posts that don't have one, using OpenAI's GPT models.

2. **Embedding Generation**: Creates semantic embeddings (vector representations) of post content using OpenAI's embedding models. These embeddings capture the meaning and context of posts in a numerical format.

3. **Vector Storage**: Stores embeddings in ChromaDB, a vector database that enables fast similarity searches. This allows the system to find posts with similar content or themes.

## Architecture

The service follows a modular architecture:

```
backend/ai_service/
├── main.py              # FastAPI application entry point
├── api.py               # API route definitions
├── schemas.py           # Pydantic models for request/response validation
├── config.py            # Configuration management from environment variables
├── prompts.py           # AI prompt templates
├── caption_generator.py # Caption generation logic
├── embedding_generator.py # Embedding generation logic
├── vector_store.py      # ChromaDB operations
├── background_worker.py # Background task processing
├── mongodb_client.py    # MongoDB client for fetching post data
├── chroma_client.py     # ChromaDB client
└── utils.py             # Utility functions
```

## Integration with Upload Service

This service integrates with the existing InstaIntelli system:

1. **MongoDB Integration**: The service assumes that posts are already stored in MongoDB by the upload service. When processing a post, it fetches the post data from MongoDB to get complete information.

2. **API Endpoint**: Other services (like the upload service) can call the `/ai/process_post` endpoint to initiate AI processing for a newly uploaded post.

3. **Asynchronous Processing**: The service returns immediately after accepting a request, processing the post in the background. This ensures the upload service doesn't wait for AI processing to complete.

## How Embeddings Are Generated

The embedding generation process follows these steps:

1. **Content Collection**: The service collects all available content:

   - Post text (if provided)
   - Post caption (existing or newly generated)
   - Image description (generated using vision models if image URL is provided)

2. **Semantic Summary**: Instead of embedding raw text directly, the service first creates a semantic summary using GPT. This summary:

   - Extracts the main topic or theme
   - Captures key information or message
   - Includes relevant context

   This step ensures embeddings represent the meaning of the post, not just the raw words.

3. **Embedding Creation**: The semantic summary is then passed to OpenAI's embedding model (`text-embedding-3-small`) which converts it into a high-dimensional vector (typically 1536 dimensions).

4. **Metadata Extraction**: The service also extracts topics from the content, which are stored alongside the embedding for filtering and categorization.

## How Vector Database Is Used

ChromaDB is used as the vector database to store and search embeddings:

1. **Storage**: Each post's embedding is stored with metadata including:

   - `post_id`: Unique identifier
   - `user_id`: Owner of the post
   - `topics`: Extracted topics
   - `created_at`: Timestamp
   - `caption`, `text`, `image_url`: Original content references

2. **Similarity Search**: The vector database enables fast similarity searches. Given a query embedding, the database can find posts with similar semantic meaning by calculating cosine similarity between vectors.

3. **Future Use Cases**: This enables features like:
   - Content recommendation
   - Duplicate detection
   - Topic-based post discovery
   - User interest analysis

## Environment Variables

The service requires the following environment variables:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017
# Optional: MONGODB_DATABASE=instaintelli (default)
# Optional: MONGODB_POSTS_COLLECTION=posts (default)

# ChromaDB Configuration
CHROMA_PERSIST_PATH=./chroma_db
# Optional: CHROMA_COLLECTION_NAME=post_embeddings (default)
```

## How to Run Locally

### Prerequisites

1. Python 3.8 or higher
2. MongoDB running and accessible
3. OpenAI API key
4. Required Python packages (install via pip)

### Installation

1. **Install dependencies**:

```bash
pip install fastapi uvicorn pymongo chromadb openai pydantic pydantic-settings
```

2. **Set environment variables**:

Copy the example environment file and configure it:

```bash
cp .env_example .env
```

Then edit `.env` and set your actual values:
- Replace `sk-your-openai-api-key-here` with your actual OpenAI API key
- Update `MONGODB_URI` if your MongoDB is not running on localhost:27017
- Adjust `CHROMA_PERSIST_PATH` if you want a different storage location

3. **Run the service**:

```bash
cd backend/ai_service
python main.py
```

Or using uvicorn directly:

```bash
uvicorn backend.ai_service.main:app --reload --host 0.0.0.0 --port 8000
```

4. **Access the API**:

- API Base URL: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/ai/health`

### Testing the API

You can test the service using curl:

```bash
curl -X POST "http://localhost:8000/ai/process_post" \
  -H "Content-Type: application/json" \
  -d '{
    "post_id": "post_123",
    "user_id": "user_456",
    "text": "Beautiful sunset today!",
    "image_url": "https://example.com/image.jpg"
  }'
```

Expected response:

```json
{
  "status": "processing_started",
  "post_id": "post_123",
  "message": "Post processing initiated successfully"
}
```

## API Endpoints

### POST `/ai/process_post`

Initiates background processing of a post.

**Request Body**:

```json
{
  "post_id": "string (required)",
  "user_id": "string (required)",
  "text": "string (optional)",
  "image_url": "string (optional)"
}
```

**Response** (202 Accepted):

```json
{
  "status": "processing_started",
  "post_id": "string",
  "message": "Post processing initiated successfully"
}
```

### GET `/ai/health`

Health check endpoint to verify service is running.

**Response**:

```json
{
  "status": "healthy",
  "service": "AI Processing Service"
}
```

## Processing Flow

When a post is submitted for processing:

1. **Request Received**: API endpoint receives the request
2. **Validation**: Inputs are validated (post_id, user_id)
3. **Immediate Response**: Service returns 202 Accepted status
4. **Background Processing** (async):
   - Fetch post data from MongoDB
   - Generate image description (if image URL provided)
   - Generate caption (if missing)
   - Extract topics from content
   - Create semantic summary
   - Generate embedding
   - Store embedding and metadata in ChromaDB
   - Update MongoDB with generated caption

## Error Handling

The service includes comprehensive error handling:

- **Validation Errors**: Returns 400 Bad Request for invalid inputs
- **Database Errors**: Logs errors and continues gracefully
- **API Errors**: Returns 500 Internal Server Error for unexpected failures
- **Background Task Errors**: Logged but don't affect the API response

All errors are logged with appropriate context for debugging.

## Logging

The service uses Python's logging module with INFO level by default. Logs include:

- Service startup/shutdown events
- Request processing initiation
- Background task progress
- Error messages with context

## Notes for Production

1. **CORS Configuration**: Update CORS settings in `main.py` to restrict origins appropriately
2. **Error Monitoring**: Integrate with error monitoring services (e.g., Sentry)
3. **Rate Limiting**: Add rate limiting to prevent abuse
4. **Authentication**: Add authentication middleware for API endpoints
5. **Database Connection Pooling**: Configure MongoDB connection pooling for better performance
6. **Background Task Queue**: Consider using Celery or similar for production-scale background processing
7. **Environment Variables**: Use secure secret management (e.g., AWS Secrets Manager, HashiCorp Vault)

## Dependencies

- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `pymongo`: MongoDB driver
- `chromadb`: Vector database
- `openai`: OpenAI API client
- `pydantic`: Data validation
- `pydantic-settings`: Settings management
