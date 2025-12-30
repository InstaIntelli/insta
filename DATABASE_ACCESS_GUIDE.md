# Database Access Guide

This guide shows you how to access and view data in all databases used by InstaIntelli.

## 📊 Databases Overview

| Database | Purpose | Port | Status |
|----------|---------|------|--------|
| **PostgreSQL** | User authentication & profiles | 5432 | ✅ Running |
| **MongoDB** | Post metadata & content | 27017 | ✅ Running |
| **Redis** | Caching layer | 6379 | ✅ Running |
| **MinIO** | Image storage (S3-compatible) | 9000 (API), 9001 (Console) | ✅ Running |
| **ChromaDB** | Vector embeddings for search | 8001 | ✅ Running |

---

## 1. PostgreSQL (User Authentication)

**Purpose:** Stores user accounts, authentication data, and profiles

### Access via Docker CLI:
```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U postgres -d instaintelli

# List all tables
\dt

# View users table
SELECT * FROM users LIMIT 10;

# Count users
SELECT COUNT(*) FROM users;

# View user details
SELECT id, username, email, created_at FROM users;

# Exit
\q
```

### Access via GUI Tools:
- **pgAdmin**: Connect to `localhost:5432`
- **DBeaver**: PostgreSQL connection
- **TablePlus**: PostgreSQL connection

**Connection Details:**
- Host: `localhost`
- Port: `5432` (or `5433` if configured)
- Database: `instaintelli`
- Username: `postgres`
- Password: `postgres123` (check `.env` file)

### Quick Commands:
```bash
# View all users
docker-compose exec postgres psql -U postgres -d instaintelli -c "SELECT id, username, email, created_at FROM users;"

# View user count
docker-compose exec postgres psql -U postgres -d instaintelli -c "SELECT COUNT(*) FROM users;"

# View table structure
docker-compose exec postgres psql -U postgres -d instaintelli -c "\d users"
```

---

## 2. MongoDB (Post Metadata)

**Purpose:** Stores post content, captions, topics, and metadata

### Access via Docker CLI:
```bash
# Connect to MongoDB
docker-compose exec mongodb mongosh -u mongodb -p mongodb123 --authenticationDatabase admin

# List databases
show dbs

# Use instaintelli database
use instaintelli

# List collections
show collections

# View posts (first 5)
db.posts.find().limit(5).pretty()

# Count posts
db.posts.countDocuments()

# Find posts by user
db.posts.find({user_id: "user_xxx"}).pretty()

# View post structure
db.posts.findOne()

# Exit
exit
```

### Access via GUI Tools:
- **MongoDB Compass**: Connect to `mongodb://mongodb:mongodb123@localhost:27017/instaintelli?authSource=admin`
- **Studio 3T**: MongoDB connection
- **NoSQLBooster**: MongoDB connection

**Connection Details:**
- Host: `localhost`
- Port: `27017` (or `27018` if configured)
- Database: `instaintelli`
- Username: `mongodb`
- Password: `mongodb123` (check `.env` file)
- Auth Database: `admin`

### Quick Commands:
```bash
# List all databases
docker-compose exec mongodb mongosh -u mongodb -p mongodb123 --authenticationDatabase admin --eval "db.getMongo().getDBNames()"

# Count posts
docker-compose exec mongodb mongosh -u mongodb -p mongodb123 --authenticationDatabase admin instaintelli --eval "db.posts.countDocuments()"

# View first post
docker-compose exec mongodb mongosh -u mongodb -p mongodb123 --authenticationDatabase admin instaintelli --eval "db.posts.findOne()"

# List all collections
docker-compose exec mongodb mongosh -u mongodb -p mongodb123 --authenticationDatabase admin instaintelli --eval "db.getCollectionNames()"
```

---

## 3. Redis (Caching)

**Purpose:** Caches search results and frequently accessed data

### Access via Docker CLI:
```bash
# Connect to Redis CLI
docker-compose exec redis redis-cli

# Check connection
PING

# List all keys
KEYS *

# Get value by key
GET cache:search:your_key_here

# View all keys with pattern
KEYS cache:*

# Get key type
TYPE cache:search:your_key_here

# Get TTL (time to live)
TTL cache:search:your_key_here

# View all keys (with values)
KEYS * | xargs redis-cli --scan

# Exit
exit
```

### Access via GUI Tools:
- **RedisInsight**: Connect to `localhost:6379`
- **Redis Desktop Manager**: Redis connection
- **Another Redis Desktop Manager**: Redis connection

**Connection Details:**
- Host: `localhost`
- Port: `6379` (or `6380` if configured)
- No password (default)
- Database: `0`

### Quick Commands:
```bash
# Check if Redis is running
docker-compose exec redis redis-cli PING

# List all keys
docker-compose exec redis redis-cli KEYS "*"

# List cache keys
docker-compose exec redis redis-cli KEYS "cache:*"

# Get key value
docker-compose exec redis redis-cli GET "cache:search:your_key"

# Clear all cache
docker-compose exec redis redis-cli FLUSHDB
```

---

## 4. MinIO (Object Storage - Images)

**Purpose:** Stores uploaded images and thumbnails

### Access via Web Console:
1. Open browser: `http://localhost:9001`
2. Login:
   - Username: `minioadmin`
   - Password: `minioadmin123` (check `.env` file)

### Access via Docker CLI:
```bash
# Setup MinIO client alias
docker-compose exec minio mc alias set myminio http://localhost:9000 minioadmin minioadmin123

# List all buckets
docker-compose exec minio mc ls myminio

# List objects in a bucket
docker-compose exec minio mc ls myminio/instaintelli-posts

# View bucket info
docker-compose exec minio mc stat myminio/instaintelli-posts

# Download an object
docker-compose exec minio mc cp myminio/instaintelli-posts/path/to/image.png /tmp/

# List all objects recursively
docker-compose exec minio mc ls myminio/instaintelli-posts --recursive
```

### Access via S3-Compatible Tools:
- **MinIO Console**: `http://localhost:9001`
- **S3 Browser**: Connect to `localhost:9000`
- **Cyberduck**: S3 connection

**Connection Details:**
- Endpoint: `http://localhost:9000`
- Access Key: `minioadmin`
- Secret Key: `minioadmin123` (check `.env` file)
- Region: `us-east-1` (default)

### Quick Commands:
```bash
# List buckets
docker-compose exec minio mc alias set myminio http://localhost:9000 minioadmin minioadmin123 && docker-compose exec minio mc ls myminio

# Count objects in bucket
docker-compose exec minio mc ls myminio/instaintelli-posts --recursive | wc -l

# View bucket size
docker-compose exec minio mc du myminio/instaintelli-posts
```

---

## 5. ChromaDB (Vector Database)

**Purpose:** Stores embeddings for semantic search

### Access via API:
```bash
# Check health
curl http://localhost:8001/api/v1/heartbeat

# List collections
curl http://localhost:8001/api/v1/collections

# Get collection info
curl http://localhost:8001/api/v1/collections/instaintelli_embeddings
```

### Access via Python:
```python
import chromadb

# Connect to ChromaDB
client = chromadb.HttpClient(host="localhost", port=8001)

# List collections
collections = client.list_collections()
print(collections)

# Get collection
collection = client.get_collection("instaintelli_embeddings")

# Count embeddings
count = collection.count()
print(f"Total embeddings: {count}")

# Get first 10 items
results = collection.get(limit=10)
print(results)
```

### Access via Docker:
```bash
# Connect to ChromaDB container
docker-compose exec chromadb python

# Then run Python code above
```

**Connection Details:**
- Host: `localhost`
- Port: `8001`
- Collection: `instaintelli_embeddings`

---

## 🔍 Quick Database Status Check

Run this script to check all databases:

```bash
# PostgreSQL
echo "=== PostgreSQL ==="
docker-compose exec postgres psql -U postgres -d instaintelli -c "SELECT COUNT(*) as user_count FROM users;"

# MongoDB
echo "=== MongoDB ==="
docker-compose exec mongodb mongosh -u mongodb -p mongodb123 --authenticationDatabase admin instaintelli --eval "db.posts.countDocuments()"

# Redis
echo "=== Redis ==="
docker-compose exec redis redis-cli DBSIZE

# MinIO
echo "=== MinIO ==="
docker-compose exec minio mc alias set myminio http://localhost:9000 minioadmin minioadmin123 2>&1 | Out-Null
docker-compose exec minio mc ls myminio

# ChromaDB
echo "=== ChromaDB ==="
curl -s http://localhost:8001/api/v1/heartbeat
```

---

## 📝 Common Queries

### View All Users (PostgreSQL)
```sql
SELECT id, username, email, created_at, is_active 
FROM users 
ORDER BY created_at DESC;
```

### View All Posts (MongoDB)
```javascript
db.posts.find()
  .sort({created_at: -1})
  .limit(10)
  .pretty();
```

### View Cache Statistics (Redis)
```bash
docker-compose exec redis redis-cli INFO stats
```

### View All Images (MinIO)
```bash
docker-compose exec minio mc ls myminio/instaintelli-posts --recursive
```

### View Embeddings Count (ChromaDB)
```python
import chromadb
client = chromadb.HttpClient(host="localhost", port=8001)
collection = client.get_collection("instaintelli_embeddings")
print(f"Total embeddings: {collection.count()}")
```

---

## 🛠️ Troubleshooting

### Database Not Accessible?
1. Check if container is running: `docker-compose ps`
2. Check logs: `docker-compose logs <service_name>`
3. Verify port mapping in `docker-compose.yml`
4. Check `.env` file for credentials

### Connection Refused?
- Ensure database container is healthy: `docker-compose ps`
- Check if port is already in use: `netstat -an | findstr <port>`
- Restart service: `docker-compose restart <service_name>`

### Authentication Failed?
- Verify credentials in `.env` file
- Check if user exists in database
- For MongoDB, ensure `authSource=admin` is set

---

## 📚 Additional Resources

- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **MongoDB Docs**: https://docs.mongodb.com/
- **Redis Docs**: https://redis.io/documentation
- **MinIO Docs**: https://min.io/docs/
- **ChromaDB Docs**: https://docs.trychroma.com/

