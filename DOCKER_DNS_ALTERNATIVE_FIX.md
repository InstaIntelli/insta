# Alternative Docker DNS Fix (When Settings Not Available)

## 🚨 Problem
Can't find DNS settings in Docker Desktop, but still getting network errors.

## ✅ Alternative Solutions

### **Solution 1: Restart Docker Desktop Completely**

1. **Right-click Docker icon** in system tray (bottom-right)
2. **Click "Quit Docker Desktop"**
3. **Wait 30 seconds**
4. **Start Docker Desktop again** (from Start Menu)
5. **Wait 2-3 minutes** for full startup
6. **Try again:**
   ```powershell
   docker-compose up -d
   ```

### **Solution 2: Pull Images Manually First**

Pull images one by one to identify which one fails:

```powershell
# Test basic connectivity
docker pull hello-world

# Pull each image manually
docker pull postgres:15-alpine
docker pull mongo:7
docker pull redis:7-alpine
docker pull minio/minio:latest
docker pull chromadb/chroma:latest
docker pull neo4j:5.19.0-community

# If all pull successfully, then:
docker-compose up -d
```

### **Solution 3: Use Different Neo4j Image Tag**

The specific version might be unavailable. Try these alternatives:

**Option A: Use latest stable**
```yaml
# In docker-compose.yml, change:
image: neo4j:5.19.0-community
# To:
image: neo4j:latest
```

**Option B: Use older stable version**
```yaml
image: neo4j:5.15.0-community
```

**Option C: Use community edition without version**
```yaml
image: neo4j:community
```

### **Solution 4: Configure DNS at System Level (Windows)**

1. **Open Network Settings:**
   - Press `Windows Key + I`
   - Go to **Network & Internet** → **Advanced network settings** → **More network adapter options**

2. **Right-click your active network adapter** (Wi-Fi or Ethernet)
3. **Click "Properties"**
4. **Select "Internet Protocol Version 4 (TCP/IPv4)"**
5. **Click "Properties"**
6. **Select "Use the following DNS server addresses"**
7. **Add:**
   - Preferred: `8.8.8.8`
   - Alternate: `1.1.1.1`
8. **Click OK**
9. **Restart Docker Desktop**
10. **Try again**

### **Solution 5: Use Docker Daemon JSON (Advanced)**

Create/edit Docker daemon configuration:

1. **Open Docker Desktop**
2. **Go to Settings** → **Docker Engine** (or look for JSON configuration)
3. **Add DNS configuration:**
   ```json
   {
     "dns": ["8.8.8.8", "1.1.1.1", "1.0.0.1"]
   }
   ```
4. **Click "Apply & Restart"**

**If Docker Engine settings not available**, manually edit:

1. **Close Docker Desktop**
2. **Navigate to:** `C:\Users\YourUsername\.docker\`
3. **Create/edit `daemon.json`** (if it doesn't exist):
   ```json
   {
     "dns": ["8.8.8.8", "1.1.1.1"]
   }
   ```
4. **Start Docker Desktop**

### **Solution 6: Temporarily Skip Neo4j**

If Neo4j keeps failing, start without it:

**Edit `docker-compose.yml`:**

1. **Comment out Neo4j service** (add `#` before each line):
   ```yaml
   # neo4j:
   #   image: neo4j:5.19.0-community
   #   ...
   ```

2. **Comment out Neo4j dependency in backend:**
   ```yaml
   #   neo4j:
   #     condition: service_healthy
   ```

3. **Comment out Neo4j volumes:**
   ```yaml
   #   neo4j_data:
   #     driver: local
   ```

4. **Save and run:**
   ```powershell
   docker-compose up -d
   ```

**Note:** Social features (follow, like, comment) won't work, but everything else will.

### **Solution 7: Check Windows Network Adapter**

Sometimes Windows network adapter needs reset:

```powershell
# Run PowerShell as Administrator
# Reset network adapter
ipconfig /flushdns
ipconfig /release
ipconfig /renew

# Restart Docker Desktop
# Try again
```

### **Solution 8: Use VPN or Different Network**

If you're on a restricted network:

1. **Try a different network** (mobile hotspot, different WiFi)
2. **Use VPN** if available
3. **Check if corporate firewall** is blocking Docker

### **Solution 9: Update Docker Desktop**

Old versions might have network issues:

1. **Check Docker Desktop version:**
   - Docker Desktop → Settings → About
2. **Download latest from:** https://www.docker.com/products/docker-desktop
3. **Update Docker Desktop**
4. **Restart computer**
5. **Try again**

## 🎯 Recommended Order to Try

1. ✅ **Restart Docker Desktop** (easiest)
2. ✅ **Pull images manually** (identifies problem)
3. ✅ **Change Neo4j image tag** (quick fix)
4. ✅ **Configure system DNS** (Windows level)
5. ✅ **Skip Neo4j temporarily** (if urgent)

## 📝 Quick Commands

```powershell
# 1. Restart Docker Desktop
# (Right-click system tray → Quit, then restart)

# 2. Test connectivity
docker pull hello-world

# 3. Try different Neo4j version
docker pull neo4j:latest

# 4. If that works, update docker-compose.yml to use neo4j:latest
# Then:
docker-compose up -d
```

## ✅ Most Likely Quick Fix

**Try this first:**

1. **Change Neo4j image in docker-compose.yml to `neo4j:latest`**
2. **Restart Docker Desktop completely**
3. **Wait 2 minutes**
4. **Run: `docker-compose up -d`**

This usually works because `latest` tag is more reliably available.

