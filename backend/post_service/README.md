# InstaIntelli Post Upload + Storage Service

## Overview

The Post Upload + Storage Service is a FastAPI-based microservice that handles the upload, storage, and metadata management of social media posts for the InstaIntelli platform. This service is responsible for receiving image uploads, storing them in object storage (MinIO), generating thumbnails, and maintaining post metadata in MongoDB.

## What This Service Does

This service performs the following operations:

1. **File Upload Handling**: Accepts image uploads (JPG, PNG) via multipart form data
2. **File Validation**: Validates file type, size, and integrity
3. **Object Storage**: Uploads original images to MinIO (S3-compatible storage)
4. **Thumbnail Generation**: Creates optimized thumbnails using Pillow
5. **Metadata Storage**: Stores post information in MongoDB for quick retrieval
6. **URL Generation**: Provides public URLs for uploaded images and thumbnails

## Upload Flow Step-by-Step

When a post is uploaded, the following steps occur:

1. **Request Reception**: API receives multipart form data with:
   - Image file (required)
   - User ID (required)
   - Text content (optional)

2. **Validation**:
   - Validates user ID format
   - Validates file type (must be JPG or PNG)
   - Validates file size (must be within configured limit)
   - Validates image integrity (ensures it's a valid, non-corrupted image)

3. **Image Processing**:
   - Opens image using Pillow
   - Generates a thumbnail while maintaining aspect ratio
   - Converts both original and thumbnail to bytes

4. **Storage**:
   - Generates unique post ID
   - Uploads original image to MinIO at `originals/{post_id}.{ext}`
   - Uploads thumbnail to MinIO at `thumbnails/{post_id}.{ext}`
   - Gets public URLs for both files

5. **Metadata Storage**:
   - Creates post metadata document with:
     - post_id
     - user_id
     - text (if provided)
     - image_url
     - thumbnail_url
     - created_at timestamp
   - Stores document in MongoDB posts collection

6. **Response**:
   - Returns JSON response with post_id, status, and URLs
   - If any step fails, appropriate error is returned

## MongoDB Schema

The service uses a `posts` collection in MongoDB with the following schema:

```javascript
{
  "_id": ObjectId,              // MongoDB auto-generated ID
  "post_id": String,            // Unique post identifier (e.g., "post_abc123")
  "user_id": String,            // User identifier
  "text": String | null,        // Optional text content
  "image_url": String,          // URL of original image in MinIO
  "thumbnail_url": String,      // URL of thumbnail image in MinIO
  "created_at": DateTime        // Post creation timestamp
}
```

### Indexes

The service automatically creates the following indexes for optimal query performance:

- **Single field indexes**:
  - `user_id`: For fast user-specific queries
  - `created_at`: For chronological sorting

- **Compound index**:
  - `(user_id, created_at)`: For efficient user timeline queries

## MinIO Storage Layout

Files are organized in the MinIO bucket with the following structure:

```
bucket-name/
├── originals/
│   ├── post_abc123.jpg
│   ├── post_def456.png
│   └── ...
└── thumbnails/
    ├── post_abc123.jpg
    ├── post_def456.png
    └── ...
```

- **originals/**: Contains full-resolution uploaded images
- **thumbnails/**: Contains generated thumbnail images (default: 300x300px, maintaining aspect ratio)

## Integration with Other Services

### Authentication Service

This service assumes authentication is handled by a separate authentication service. The `user_id` is provided in the request, and the service trusts that the user has been authenticated before reaching this endpoint.

**Integration points**:
- Receives `user_id` as a validated parameter
- No authentication logic is implemented in this service
- In production, an authentication middleware should validate tokens before requests reach this service

### AI Processing Service

After a post is uploaded and stored, the AI Processing Service can be called to:
- Generate captions
- Create embeddings
- Store embeddings in vector database

**Integration pattern**:
1. Post Upload Service stores the post and returns post_id
2. The calling service (or a webhook/event system) triggers AI processing
3. AI Processing Service fetches post data from MongoDB using post_id
4. AI Processing Service performs caption generation and embedding creation

**Example integration flow**:
```python
# After successful upload
response = upload_post(...)  # Returns post_id

# Trigger AI processing (could be done by API gateway or event system)
ai_service.process_post(
    post_id=response.post_id,
    user_id=user_id,
    image_url=response.image_url
)
```

## Environment Variables

The service requires the following environment variables:

### Required Variables

```bash
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=instaintelli

# MinIO Configuration
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=instaintelli-posts
```

### Optional Variables

```bash
# MongoDB (optional)
MONGODB_POSTS_COLLECTION=posts  # Default: posts

# MinIO (optional)
MINIO_USE_SSL=false             # Default: false
MINIO_REGION=us-east-1          # Default: us-east-1

# Upload Configuration (optional)
MAX_UPLOAD_SIZE_MB=10           # Default: 10

# API Configuration (optional)
API_TITLE=InstaIntelli Post Upload + Storage Service
API_VERSION=1.0.0
```

## How to Run Locally

### Prerequisites

1. Python 3.8 or higher
2. MongoDB running and accessible
3. MinIO server running and accessible
4. Required Python packages

### Installation

1. **Install dependencies**:

```bash
pip install fastapi uvicorn pymongo minio pillow python-multipart pydantic pydantic-settings
```

Or using requirements.txt (if created):

```bash
pip install -r requirements.txt
```

2. **Set up MinIO**:

   - Download and run MinIO server: https://min.io/download
   - Or use Docker:
     ```bash
     docker run -p 9000:9000 -p 9001:9001 \
       -e "MINIO_ROOT_USER=minioadmin" \
       -e "MINIO_ROOT_PASSWORD=minioadmin" \
       minio/minio server /data --console-address ":9001"
     ```

3. **Set environment variables**:

   Create a `.env` file in the `backend/post_service/` directory:

   ```bash
   MONGODB_URI=mongodb://localhost:27017
   MONGODB_DB_NAME=instaintelli
   MINIO_ENDPOINT=localhost:9000
   MINIO_ACCESS_KEY=minioadmin
   MINIO_SECRET_KEY=minioadmin
   MINIO_BUCKET_NAME=instaintelli-posts
   MAX_UPLOAD_SIZE_MB=10
   ```

4. **Run the service**:

```bash
cd backend/post_service
python main.py
```

Or using uvicorn directly:

```bash
uvicorn backend.post_service.main:app --reload --host 0.0.0.0 --port 8001
```

5. **Access the API**:

   - API Base URL: `http://localhost:8001`
   - API Documentation: `http://localhost:8001/docs`
   - Health Check: `http://localhost:8001/posts/health`

### Testing the API

You can test the service using curl:

```bash
curl -X POST "http://localhost:8001/posts/upload" \
  -F "file=@/path/to/image.jpg" \
  -F "user_id=user_123" \
  -F "text=Beautiful sunset today!"
```

Expected response:

```json
{
  "post_id": "post_abc123",
  "status": "uploaded",
  "image_url": "http://localhost:9000/instaintelli-posts/originals/post_abc123.jpg",
  "thumbnail_url": "http://localhost:9000/instaintelli-posts/thumbnails/post_abc123.jpg",
  "message": "Post uploaded successfully"
}
```

## API Endpoints

### POST `/posts/upload`

Upload a new post with an image.

**Request** (multipart/form-data):
- `file` (required): Image file (JPG or PNG)
- `user_id` (required): User identifier
- `text` (optional): Text content

**Response** (201 Created):
```json
{
  "post_id": "string",
  "status": "uploaded",
  "image_url": "string",
  "thumbnail_url": "string",
  "message": "Post uploaded successfully"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid file type, size, or user_id
- `500 Internal Server Error`: Upload or storage failure

### GET `/posts/health`

Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "service": "Post Upload + Storage Service"
}
```

## Error Handling

The service includes comprehensive error handling:

- **Validation Errors**: Returns 400 Bad Request for invalid inputs
- **File Errors**: Returns 400 Bad Request for invalid/corrupted images
- **Storage Errors**: Returns 500 Internal Server Error for MinIO failures
- **Database Errors**: Returns 500 Internal Server Error for MongoDB failures
- **Cleanup**: Attempts to delete uploaded files if metadata storage fails

All errors are logged with appropriate context for debugging.

## Logging

The service uses Python's logging module with INFO level by default. Logs include:

- Service startup/shutdown events
- File validation steps
- Upload progress
- Storage operations
- Error messages with context

## Notes for Production

1. **Authentication**: Add authentication middleware to validate user tokens
2. **Rate Limiting**: Implement rate limiting to prevent abuse
3. **CORS Configuration**: Update CORS settings to restrict origins appropriately
4. **Error Monitoring**: Integrate with error monitoring services (e.g., Sentry)
5. **File Size Limits**: Adjust `MAX_UPLOAD_SIZE_MB` based on requirements
6. **MinIO Security**: Use SSL/TLS in production and secure access keys
7. **Database Connection Pooling**: Configure MongoDB connection pooling
8. **CDN Integration**: Consider using a CDN for image delivery
9. **Image Optimization**: May want to add additional image optimization (WebP conversion, etc.)
10. **Environment Variables**: Use secure secret management (e.g., AWS Secrets Manager, HashiCorp Vault)

## Dependencies

- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `pymongo`: MongoDB driver
- `minio`: MinIO/S3 client
- `pillow`: Image processing
- `pydantic`: Data validation
- `pydantic-settings`: Settings management
- `python-multipart`: Multipart form data support

