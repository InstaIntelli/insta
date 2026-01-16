# Setup Instructions

## Quick Start

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Configure environment variables**:
```bash
# Copy the example file
cp .env_example .env

# Edit .env and set your actual values:
# - OPENAI_API_KEY: Your OpenAI API key
# - MONGODB_URI: Your MongoDB connection string
# - CHROMA_PERSIST_PATH: Path where ChromaDB will store data
```

3. **Run the service**:
```bash
python main.py
```

## Environment Variables

Required variables (must be set):
- `OPENAI_API_KEY`: Your OpenAI API key
- `MONGODB_URI`: MongoDB connection string (e.g., `mongodb://localhost:27017`)
- `CHROMA_PERSIST_PATH`: Directory path for ChromaDB persistence (e.g., `./chroma_db`)

Optional variables (have defaults):
- `OPENAI_MODEL`: OpenAI model for text generation (default: `gpt-4o-mini`)
- `OPENAI_EMBEDDING_MODEL`: OpenAI model for embeddings (default: `text-embedding-3-small`)
- `MONGODB_DATABASE`: MongoDB database name (default: `instaintelli`)
- `MONGODB_POSTS_COLLECTION`: MongoDB collection name (default: `posts`)
- `CHROMA_COLLECTION_NAME`: ChromaDB collection name (default: `post_embeddings`)

