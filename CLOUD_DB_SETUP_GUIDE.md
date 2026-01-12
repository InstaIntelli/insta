# Cloud Database Setup Guide for InstaIntelli

## 🎯 Overview

This guide shows you how to set up cloud databases (Supabase, MongoDB Atlas, Upstash) as primary storage with local Docker databases as automatic fallback.

## 📋 Setup Checklist

- [ ] Supabase (PostgreSQL) - Primary
- [ ] MongoDB Atlas - Primary  
- [ ] Upstash (Redis) - Primary
- [ ] Local Docker - Fallback (already configured)

---

## 1. 🐘 Supabase Setup (PostgreSQL)

### Step 1: Create Supabase Account

1. Go to https://supabase.com
2. Click **"Start your project"**
3. Sign up with GitHub (recommended) or email
4. Verify your email

### Step 2: Create New Project

1. Click **"New Project"**
2. Fill in:
   - **Name:** `instaintelli` (or your project name)
   - **Database Password:** Create a strong password (save it!)
   - **Region:** Choose closest to you
   - **Pricing Plan:** Free
3. Click **"Create new project"**
4. Wait 2-3 minutes for project to initialize

### Step 3: Get Connection String

1. Go to **Project Settings** (gear icon)
2. Click **"Database"** in sidebar
3. Scroll to **"Connection string"**
4. Select **"URI"** tab
5. Copy the connection string (looks like):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   ```
6. Replace `[YOUR-PASSWORD]` with your actual database password

### Step 4: Add to .env

Add to your `.env` file:

```bash
# Supabase (Primary PostgreSQL)
SUPABASE_DB_URL=postgresql://postgres:YOUR_PASSWORD@db.xxxxx.supabase.co:5432/postgres
SUPABASE_PROJECT_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_KEY=your-service-key-here
```

**Where to find keys:**
- Go to **Project Settings** → **API**
- Copy **"anon public"** key → `SUPABASE_ANON_KEY`
- Copy **"service_role"** key → `SUPABASE_SERVICE_KEY`

### Step 5: Test Connection

```powershell
# Test from your backend
docker-compose exec backend python -c "from app.db.postgres.failover import postgres_failover; print(postgres_failover.get_status())"
```

---

## 2. 🍃 MongoDB Atlas Setup

### Step 1: Create MongoDB Atlas Account

1. Go to https://www.mongodb.com/cloud/atlas
2. Click **"Try Free"**
3. Sign up with email or Google
4. Verify your email

### Step 2: Create Cluster

1. Click **"Build a Database"**
2. Choose **"M0 FREE"** (Free tier)
3. Select **Cloud Provider:** AWS (or your preference)
4. Select **Region:** Closest to you
5. Click **"Create"**
6. Wait 2-3 minutes for cluster to deploy

### Step 3: Create Database User

1. Go to **"Database Access"** (left sidebar)
2. Click **"Add New Database User"**
3. Choose **"Password"** authentication
4. Username: `instaintelli_user`
5. Password: Create strong password (save it!)
6. Database User Privileges: **"Atlas admin"**
7. Click **"Add User"**

### Step 4: Whitelist IP Address

1. Go to **"Network Access"** (left sidebar)
2. Click **"Add IP Address"**
3. Click **"Allow Access from Anywhere"** (for development)
   - Or add your specific IP for production
4. Click **"Confirm"**

### Step 5: Get Connection String

1. Go to **"Database"** (left sidebar)
2. Click **"Connect"** on your cluster
3. Choose **"Connect your application"**
4. Select **Driver:** Python, Version: 3.6 or later
5. Copy the connection string (looks like):
   ```
   mongodb+srv://instaintelli_user:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
6. Replace `<password>` with your actual password

### Step 6: Add to .env

Add to your `.env` file:

```bash
# MongoDB Atlas (Primary MongoDB)
MONGODB_ATLAS_URL=mongodb+srv://instaintelli_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGODB_ATLAS_DATABASE=instaintelli
```

### Step 7: Test Connection

```powershell
# Test from your backend
docker-compose exec backend python -c "from app.db.mongodb.failover import mongo_failover; print(mongo_failover.get_status())"
```

---

## 3. ⚡ Upstash Setup (Redis)

### Step 1: Create Upstash Account

1. Go to https://upstash.com
2. Click **"Sign Up"**
3. Sign up with GitHub (recommended) or email
4. Verify your email

### Step 2: Create Redis Database

1. Click **"Create Database"**
2. Fill in:
   - **Name:** `instaintelli-redis`
   - **Type:** Regional (or Global for better performance)
   - **Region:** Choose closest to you
   - **Tier:** Free
3. Click **"Create"**

### Step 3: Get Connection Details

1. Click on your database
2. Go to **"Details"** tab
3. Copy:
   - **UPSTASH_REDIS_URL:** `redis://default:xxxxx@xxxxx.upstash.io:6379`
   - **UPSTASH_REDIS_REST_URL:** `https://xxxxx.upstash.io`
   - **UPSTASH_REDIS_REST_TOKEN:** `xxxxx`

### Step 4: Add to .env

Add to your `.env` file:

```bash
# Upstash (Primary Redis)
UPSTASH_REDIS_URL=redis://default:YOUR_TOKEN@xxxxx.upstash.io:6379
UPSTASH_REDIS_REST_URL=https://xxxxx.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-token-here
```

### Step 5: Test Connection

```powershell
# Test from your backend
docker-compose exec backend python -c "from app.db.redis.failover import redis_failover; print(redis_failover.get_status())"
```

---

## 4. ✅ Verify Setup

### Check Database Status

Visit: http://localhost:8000/api/v1/health/databases

You should see:
```json
{
  "postgres": {
    "using_primary": true,
    "primary_available": true,
    "current_db": "Supabase"
  },
  "mongodb": {
    "using_primary": true,
    "primary_available": true,
    "current_db": "MongoDB Atlas"
  },
  "redis": {
    "using_primary": true,
    "primary_available": true,
    "current_db": "Upstash"
  },
  "overall_status": "healthy"
}
```

### Test Failover

1. **Temporarily break Supabase connection** (wrong password in .env)
2. **Restart backend:** `docker-compose restart backend`
3. **Check status again:** Should show `"using_primary": false, "current_db": "Local PostgreSQL"`
4. **Fix connection:** Restore correct password
5. **Wait 30 seconds:** Should automatically switch back to Supabase

---

## 5. 📝 Complete .env Example

```bash
# ============================================
# CLOUD DATABASES (Primary)
# ============================================

# Supabase (PostgreSQL)
SUPABASE_DB_URL=postgresql://postgres:YOUR_PASSWORD@db.xxxxx.supabase.co:5432/postgres
SUPABASE_PROJECT_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key

# MongoDB Atlas
MONGODB_ATLAS_URL=mongodb+srv://user:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGODB_ATLAS_DATABASE=instaintelli

# Upstash (Redis)
UPSTASH_REDIS_URL=redis://default:token@xxxxx.upstash.io:6379
UPSTASH_REDIS_REST_URL=https://xxxxx.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-token

# ============================================
# LOCAL DATABASES (Fallback)
# ============================================

# Local PostgreSQL (Fallback)
POSTGRES_URL=postgresql://postgres:postgres123@postgres:5432/instaintelli

# Local MongoDB (Fallback)
MONGODB_URL=mongodb://mongodb:mongodb123@mongodb:27017/instaintelli?authSource=admin
MONGODB_DATABASE=instaintelli

# Local Redis (Fallback)
REDIS_URL=redis://redis:6379/0
REDIS_HOST=redis
REDIS_PORT=6379
```

---

## 6. 🚀 Benefits

✅ **Automatic Failover:** If cloud is down, automatically uses local  
✅ **High Availability:** Always have a backup database  
✅ **Zero Downtime:** Seamless switching between primary and fallback  
✅ **Health Monitoring:** Check status at `/api/v1/health/databases`  
✅ **Free Tier:** All cloud services have generous free tiers  

---

## 7. 🔧 Troubleshooting

### Issue: Can't connect to Supabase

**Solutions:**
- Check password is correct (no spaces)
- Verify IP is whitelisted (if required)
- Check connection string format
- Try connecting with psql: `psql "your-connection-string"`

### Issue: MongoDB Atlas connection fails

**Solutions:**
- Verify IP is whitelisted (allow from anywhere for dev)
- Check username/password are correct
- Verify connection string format
- Check cluster is running (not paused)

### Issue: Upstash connection fails

**Solutions:**
- Verify token is correct
- Check database is not paused
- Verify URL format
- Check region matches

### Issue: Failover not working

**Solutions:**
- Check both primary and fallback URLs are set
- Verify local databases are running
- Check logs: `docker-compose logs backend`
- Wait 30 seconds for health check interval

---

## 8. 📊 Monitoring

### View Database Status

```powershell
# Via API
curl http://localhost:8000/api/v1/health/databases

# Via Python
docker-compose exec backend python -c "
from app.db.postgres.failover import postgres_failover
from app.db.mongodb.failover import mongo_failover
from app.db.redis.failover import redis_failover
print('PostgreSQL:', postgres_failover.get_status())
print('MongoDB:', mongo_failover.get_status())
print('Redis:', redis_failover.get_status())
"
```

### View Logs

```powershell
# Watch for failover messages
docker-compose logs -f backend | grep -i "failover\|switching\|primary\|fallback"
```

---

## 🎉 You're Done!

Your InstaIntelli app now has:
- ✅ Cloud databases as primary (Supabase, MongoDB Atlas, Upstash)
- ✅ Local databases as automatic fallback
- ✅ Zero-downtime failover
- ✅ Health monitoring
- ✅ Robust persistence

**Next Steps:**
1. Test the setup
2. Monitor database status
3. Enjoy high availability! 🚀

