# Docker Network/DNS Fix Guide

## 🚨 Problem
Docker can't pull images due to network/DNS issues:
```
failed to copy: httpReadSeeker: failed open: ... no such host
```

## ✅ Solutions (Try in Order)

### **Solution 1: Check Internet Connection**

1. **Test internet connectivity:**
   ```powershell
   ping google.com
   ping docker.com
   ```

2. **If ping fails**, fix your internet connection first

### **Solution 2: Fix Docker DNS Settings**

1. **Open Docker Desktop**
2. **Go to Settings** (gear icon)
3. **Click "Resources" → "Network"**
4. **Change DNS settings:**
   - Uncheck "Use kernel DNS resolver"
   - Add DNS servers:
     - `8.8.8.8` (Google DNS)
     - `8.8.4.4` (Google DNS backup)
     - `1.1.1.1` (Cloudflare DNS)
5. **Click "Apply & Restart"**
6. **Wait for Docker to restart** (30-60 seconds)

### **Solution 3: Restart Docker Desktop**

1. **Right-click Docker icon** in system tray
2. **Click "Quit Docker Desktop"**
3. **Wait 10 seconds**
4. **Start Docker Desktop again** (from Start Menu)
5. **Wait for full startup** (1-2 minutes)
6. **Try again:**
   ```powershell
   docker-compose up -d
   ```

### **Solution 4: Use Alternative Neo4j Image**

If DNS issues persist, use a different Neo4j image tag:

**Edit `docker-compose.yml`:**

Find the neo4j service (around line 112) and change:

```yaml
# Change from:
neo4j:
  image: neo4j:5-community

# To (use official latest):
neo4j:
  image: neo4j:latest
```

Or try a specific stable version:

```yaml
neo4j:
  image: neo4j:5.19.0-community
```

### **Solution 5: Pull Image Manually First**

Try pulling the image separately to see detailed error:

```powershell
# Pull Neo4j image manually
docker pull neo4j:5-community

# If that fails, try:
docker pull neo4j:latest

# Or try with specific version:
docker pull neo4j:5.19.0-community
```

### **Solution 6: Check Firewall/Antivirus**

1. **Temporarily disable Windows Firewall:**
   - Windows Security → Firewall & network protection
   - Turn off for Private network (temporarily)
   - Try docker-compose again
   - Re-enable firewall after

2. **Add Docker to Firewall exceptions:**
   - Windows Security → Firewall & network protection
   - Allow an app through firewall
   - Find "Docker Desktop" and enable it

3. **Check Antivirus:**
   - Some antivirus software blocks Docker
   - Temporarily disable to test
   - Add Docker to exceptions if needed

### **Solution 7: Use Docker Hub Mirror (China/Network Issues)**

If you're in a region with Docker Hub access issues:

1. **Edit Docker Desktop settings:**
   - Settings → Docker Engine
   - Add registry mirrors:
   ```json
   {
     "registry-mirrors": [
       "https://docker.mirrors.ustc.edu.cn",
       "https://hub-mirror.c.163.com"
     ]
   }
   ```
2. **Click "Apply & Restart"**

### **Solution 8: Clear Docker Cache**

Sometimes corrupted cache causes issues:

```powershell
# Stop Docker Desktop first
# Then run:
docker system prune -a --volumes

# Restart Docker Desktop
# Try again
docker-compose up -d
```

### **Solution 9: Use VPN/Proxy (If Behind Corporate Firewall)**

If you're behind a corporate firewall:

1. **Configure Docker proxy:**
   - Docker Desktop → Settings → Resources → Proxies
   - Enter your proxy settings
   - Click "Apply & Restart"

2. **Or use VPN** to bypass firewall restrictions

## 🔧 Quick Fix Commands

```powershell
# 1. Restart Docker Desktop (do this first)
# Right-click system tray icon → Quit Docker Desktop
# Then start it again

# 2. Test Docker connectivity
docker pull hello-world

# 3. If hello-world works, try Neo4j
docker pull neo4j:5-community

# 4. If specific version fails, try latest
docker pull neo4j:latest

# 5. Then start your project
cd C:\Alisha\Projects\university\big_data_project
docker-compose up -d
```

## 📝 Alternative: Skip Neo4j Temporarily

If Neo4j keeps failing, you can temporarily comment it out:

**Edit `docker-compose.yml`:**

1. **Find the neo4j service** (lines ~112-134)
2. **Comment it out** by adding `#` at the start of each line
3. **Also comment out neo4j dependency in backend service**
4. **Save and try:**
   ```powershell
   docker-compose up -d
   ```

**Note:** This will disable social features (follow, like, comment) but other features will work.

## ✅ Most Likely Solution

**90% of the time, this fixes it:**

1. **Open Docker Desktop**
2. **Settings → Resources → Network**
3. **Add DNS: `8.8.8.8` and `1.1.1.1`**
4. **Apply & Restart**
5. **Wait 2 minutes**
6. **Try again:**
   ```powershell
   docker-compose up -d
   ```

## 🎯 After Fixing

Once images pull successfully:

```powershell
# Check all services are up
docker-compose ps

# View logs if any issues
docker-compose logs -f

# Access your app
# Frontend: http://localhost:3000
# Backend: http://localhost:8000/docs
```

