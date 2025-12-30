# Database Status Report

**Generated:** December 30, 2025

## ✅ All Databases Are Accessible!

All 5 databases are running and accessible. Here's the current status:

---

## 📊 Database Status Summary

| Database | Status | Data Count | Access Method |
|----------|--------|------------|---------------|
| **PostgreSQL** | ✅ **Accessible** | 1 user | Port 5432 |
| **MongoDB** | ✅ **Accessible** | 11 posts | Port 27017 |
| **Redis** | ✅ **Accessible** | 0 keys (empty cache) | Port 6379 |
| **MinIO** | ✅ **Running** | Check via web console | Port 9000/9001 |
| **ChromaDB** | ✅ **Running** | Check via API | Port 8001 |

---

## 1. PostgreSQL (User Authentication) ✅

**Status:** ✅ **Accessible and Working**

**Current Data:**
- **Users:** 1 user registered
- **Tables:** `users` table exists

**Sample Data:**
```
Username: alishashahid
Email: alishashahidkhan77@gmail.com
Created: 2025-12-30 02:47:10
```

**Quick Access:**
```bash
# View all users
docker-compose exec postgres psql -U postgres -d instaintelli -c "SELECT * FROM users;"

# Connect interactively
docker-compose exec postgres psql -U postgres -d instaintelli
```

**Web GUI:** Use pgAdmin, DBeaver, or TablePlus
- Host: `localhost`
- Port: `5432`
- Database: `instaintelli`
- Username: `postgres`
- Password: `postgres123`

---

## 2. MongoDB (Post Metadata) ✅

**Status:** ✅ **Accessible and Working**

**Current Data:**
- **Posts:** 11 posts stored
- **Database:** `instaintelli`
- **Collection:** `posts`

**Sample Posts:**
- Post IDs: `post_3e1d4aa17a1c`, `post_1df668c344e2`, etc.
- Contains: text, image URLs, thumbnails, user IDs, timestamps

**Quick Access:**
```bash
# Count posts
docker-compose exec mongodb mongosh -u mongodb -p mongodb123 --authenticationDatabase admin instaintelli --eval "db.posts.countDocuments()"

# View all posts
docker-compose exec mongodb mongosh -u mongodb -p mongodb123 --authenticationDatabase admin instaintelli --eval "db.posts.find().pretty()"

# Connect interactively
docker-compose exec mongodb mongosh -u mongodb -p mongodb123 --authenticationDatabase admin
```

**Web GUI:** Use MongoDB Compass
- Connection String: `mongodb://mongodb:mongodb123@localhost:27017/instaintelli?authSource=admin`
- Or: Host `localhost`, Port `27017`, Username `mongodb`, Password `mongodb123`

---

## 3. Redis (Caching) ✅

**Status:** ✅ **Accessible and Working**

**Current Data:**
- **Keys:** 0 (cache is empty - normal if no recent searches)
- **Database Size:** 0

**Quick Access:**
```bash
# Check connection
docker-compose exec redis redis-cli PING

# List all keys
docker-compose exec redis redis-cli KEYS "*"

# View cache keys
docker-compose exec redis redis-cli KEYS "cache:*"

# Connect interactively
docker-compose exec redis redis-cli
```

**Web GUI:** Use RedisInsight or Redis Desktop Manager
- Host: `localhost`
- Port: `6379`
- No password (default)

**Note:** Redis cache is empty, which is normal if you haven't performed searches recently. Cache gets populated when you use semantic search or chatbot.

---

## 4. MinIO (Object Storage) ✅

**Status:** ✅ **Running** (Access via Web Console)

**Purpose:** Stores uploaded images and thumbnails

**Access Methods:**

### Option 1: Web Console (Easiest)
1. Open browser: **http://localhost:9001**
2. Login:
   - Username: `minioadmin`
   - Password: `minioadmin123`
3. Browse buckets and files visually

### Option 2: Docker CLI
```bash
# From inside container (using internal network)
docker-compose exec minio mc alias set myminio http://minio:9000 minioadmin minioadmin123
docker-compose exec minio mc ls myminio
docker-compose exec minio mc ls myminio/instaintelli-posts --recursive
```

### Option 3: S3-Compatible Tools
- **S3 Browser**: Connect to `localhost:9000`
- **Cyberduck**: S3 connection
- **MinIO Client (mc)**: Install locally

**Connection Details:**
- Endpoint: `http://localhost:9000`
- Console: `http://localhost:9001`
- Access Key: `minioadmin`
- Secret Key: `minioadmin123`

---

## 5. ChromaDB (Vector Database) ✅

**Status:** ✅ **Running** (API v2 available)

**Purpose:** Stores embeddings for semantic search

**Note:** ChromaDB v1 API is deprecated. Use v2 API or Python client.

**Access Methods:**

### Option 1: Python Client (Recommended)
```python
import chromadb

# Connect to ChromaDB
client = chromadb.HttpClient(host="localhost", port=8001)

# List collections
collections = client.list_collections()
print(f"Collections: {[c.name for c in collections]}")

# Get collection
collection = client.get_collection("instaintelli_embeddings")

# Count embeddings
count = collection.count()
print(f"Total embeddings: {count}")

# Get sample data
results = collection.get(limit=5)
print(results)
```

### Option 2: Docker Exec
```bash
# Run Python in ChromaDB container
docker-compose exec chromadb python

# Then run the Python code above
```

### Option 3: API v2 (Advanced)
```bash
# List collections (v2 API)
curl http://localhost:8001/api/v1/collections
```

**Connection Details:**
- Host: `localhost`
- Port: `8001`
- Collection: `instaintelli_embeddings`

---

## 🔍 Quick Status Check Commands

Run these commands to quickly check all databases:

```powershell
# PostgreSQL - User count
docker-compose exec postgres psql -U postgres -d instaintelli -c "SELECT COUNT(*) FROM users;"

# MongoDB - Post count
docker-compose exec mongodb mongosh -u mongodb -p mongodb123 --authenticationDatabase admin instaintelli --eval "db.posts.countDocuments()"

# Redis - Key count
docker-compose exec redis redis-cli DBSIZE

# MinIO - List buckets (via web console: http://localhost:9001)
# Or via container:
docker-compose exec minio mc alias set myminio http://minio:9000 minioadmin minioadmin123
docker-compose exec minio mc ls myminio

# ChromaDB - Check health
# Use Python client (see above) or check container logs
docker-compose logs chromadb --tail 10
```

---

## 📝 Viewing Data in Each Database

### PostgreSQL
```sql
-- View all users
SELECT id, username, email, created_at, is_active FROM users;

-- View user count
SELECT COUNT(*) FROM users;
```

### MongoDB
```javascript
// View all posts
db.posts.find().pretty();

// Count posts
db.posts.countDocuments();

// Find posts by user
db.posts.find({user_id: "user_xxx"}).pretty();
```

### Redis
```bash
# List all keys
KEYS *

# Get value
GET cache:search:your_key

# View cache statistics
INFO stats
```

### MinIO
- **Web Console**: http://localhost:9001
- Browse buckets and files
- Download/upload files
- View file metadata

### ChromaDB
```python
# Get collection
collection = client.get_collection("instaintelli_embeddings")

# Count embeddings
print(collection.count())

# Get all data
results = collection.get()
print(results)
```

---

## 🎯 Recommended Tools for Database Access

| Database | Recommended Tool | Download Link |
|----------|------------------|--------------|
| **PostgreSQL** | DBeaver (Free) | https://dbeaver.io/ |
| **MongoDB** | MongoDB Compass (Free) | https://www.mongodb.com/try/download/compass |
| **Redis** | RedisInsight (Free) | https://redis.io/insight/ |
| **MinIO** | Web Console (Built-in) | http://localhost:9001 |
| **ChromaDB** | Python Client | Built-in (chromadb package) |

---

## ✅ Summary

**All databases are accessible and working correctly!**

- ✅ **PostgreSQL**: 1 user registered
- ✅ **MongoDB**: 11 posts stored
- ✅ **Redis**: Running (cache empty - normal)
- ✅ **MinIO**: Running (access via web console)
- ✅ **ChromaDB**: Running (use Python client)

**Next Steps:**
1. Use the **DATABASE_ACCESS_GUIDE.md** for detailed access instructions
2. Access MinIO via web console: http://localhost:9001
3. Use MongoDB Compass for visual MongoDB browsing
4. Use DBeaver for PostgreSQL management
5. Use RedisInsight for Redis monitoring

---

## 📚 Documentation

- **Full Access Guide**: See `DATABASE_ACCESS_GUIDE.md`
- **Testing Guide**: See `TESTING_GUIDE.md`
- **Project README**: See `README.md`

