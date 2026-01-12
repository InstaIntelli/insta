# Docker Desktop Startup Guide for Windows

## 🚨 Problem
The error `failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine` means Docker Desktop is not running.

## ✅ Solution: Start Docker Desktop

### **Method 1: Start from Start Menu (Easiest)**

1. **Press `Windows Key`** on your keyboard
2. **Type "Docker Desktop"**
3. **Click on "Docker Desktop"** application
4. **Wait for Docker to start** (30-60 seconds)
   - You'll see a Docker icon in the system tray (bottom-right)
   - The icon will stop animating when ready

### **Method 2: Start from Desktop/Shortcut**

1. **Look for Docker Desktop icon** on your desktop
2. **Double-click** to launch
3. **Wait for startup** (30-60 seconds)

### **Method 3: Start from Command Line**

```powershell
# Start Docker Desktop
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

# Or if installed in different location:
Start-Process "$env:ProgramFiles\Docker\Docker\Docker Desktop.exe"
```

## 🔍 Verify Docker is Running

### **Check 1: System Tray Icon**
- Look at the **bottom-right corner** of your screen
- You should see a **Docker whale icon** 🐳
- If it's **animated/spinning** → Docker is starting
- If it's **static** → Docker is running

### **Check 2: Command Line Test**

Open PowerShell or Command Prompt and run:

```powershell
docker ps
```

**If Docker is running**, you'll see:
```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

**If Docker is NOT running**, you'll see:
```
error during connect: ... The system cannot find the file specified.
```

### **Check 3: Docker Desktop Window**

- Docker Desktop window should be open
- Status should show **"Docker Desktop is running"**
- No error messages visible

## 🚀 Start Your Project

Once Docker Desktop is running:

### **Step 1: Navigate to Project Directory**

```powershell
cd C:\Alisha\Projects\university\big_data_project
```

### **Step 2: Start All Services**

```powershell
docker-compose up -d
```

This will:
- Pull images if needed
- Start all containers (postgres, mongodb, redis, minio, chromadb, neo4j, backend, frontend)
- Run them in background (`-d` flag)

### **Step 3: Check Status**

```powershell
docker-compose ps
```

You should see all services with status "Up":
```
NAME                    STATUS
instaintelli_backend    Up
instaintelli_frontend   Up
instaintelli_postgres   Up
instaintelli_mongodb    Up
instaintelli_redis      Up
instaintelli_minio      Up
instaintelli_chromadb   Up
instaintelli_neo4j    Up
```

### **Step 4: View Logs (Optional)**

```powershell
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 🛠️ Troubleshooting

### **Issue 1: Docker Desktop Won't Start**

**Symptoms:**
- Docker Desktop window doesn't open
- Error messages appear

**Solutions:**

1. **Restart Docker Desktop:**
   - Right-click Docker icon in system tray
   - Click "Quit Docker Desktop"
   - Wait 10 seconds
   - Start Docker Desktop again

2. **Check Windows Services:**
   ```powershell
   # Open Services
   services.msc
   # Look for "Docker Desktop Service" - should be "Running"
   ```

3. **Restart Your Computer:**
   - Sometimes Docker needs a fresh start

4. **Reinstall Docker Desktop** (last resort):
   - Download from: https://www.docker.com/products/docker-desktop
   - Uninstall current version
   - Install fresh copy

### **Issue 2: Docker Desktop Starts But Commands Fail**

**Symptoms:**
- Docker Desktop is running
- But `docker ps` still fails

**Solutions:**

1. **Wait longer** (Docker needs 1-2 minutes to fully initialize)

2. **Restart Docker Desktop:**
   - Right-click system tray icon
   - "Restart Docker Desktop"

3. **Check WSL 2** (if using WSL 2 backend):
   ```powershell
   wsl --status
   # Should show WSL version 2
   ```

### **Issue 3: "WSL 2 installation is incomplete"**

**Solution:**
1. Open Docker Desktop
2. Go to **Settings** → **General**
3. Check **"Use the WSL 2 based engine"**
4. If error appears, click the link to install WSL 2
5. Follow the installation instructions
6. Restart Docker Desktop

### **Issue 4: Port Already in Use**

**Symptoms:**
```
Error: bind: address already in use
```

**Solutions:**

1. **Find what's using the port:**
   ```powershell
   # Check port 8000 (backend)
   netstat -ano | findstr :8000
   
   # Check port 3000 (frontend)
   netstat -ano | findstr :3000
   ```

2. **Stop the conflicting service** or **change ports in docker-compose.yml**

## 📋 Quick Reference Commands

```powershell
# Start Docker Desktop (if not running)
# → Use Start Menu or Desktop shortcut

# Check if Docker is running
docker ps

# Navigate to project
cd C:\Alisha\Projects\university\big_data_project

# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Restart all services
docker-compose restart

# View logs
docker-compose logs -f

# Check service status
docker-compose ps

# Rebuild and start
docker-compose up -d --build
```

## ✅ Success Checklist

- [ ] Docker Desktop is running (icon in system tray)
- [ ] `docker ps` command works
- [ ] Navigated to project directory
- [ ] Ran `docker-compose up -d`
- [ ] All services show "Up" status
- [ ] Can access http://localhost:3000 (frontend)
- [ ] Can access http://localhost:8000/docs (backend API)

## 🎯 Next Steps After Docker is Running

1. **Start Docker Desktop** (if not already running)
2. **Navigate to project:**
   ```powershell
   cd C:\Alisha\Projects\university\big_data_project
   ```
3. **Start services:**
   ```powershell
   docker-compose up -d
   ```
4. **Wait 30-60 seconds** for services to initialize
5. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/docs

## 💡 Pro Tips

1. **Auto-start Docker Desktop:**
   - Docker Desktop → Settings → General
   - Check "Start Docker Desktop when you log in"

2. **Keep Docker Desktop running:**
   - Don't close Docker Desktop window
   - Minimize it instead

3. **Monitor resource usage:**
   - Docker Desktop → Settings → Resources
   - Adjust CPU/Memory if needed

4. **Use Docker Desktop dashboard:**
   - Click Docker icon in system tray
   - View containers, images, volumes

