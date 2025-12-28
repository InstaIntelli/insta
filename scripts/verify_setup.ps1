# InstaIntelli - Setup Verification Script
# Verifies all services are running and accessible

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "InstaIntelli - Setup Verification" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allHealthy = $true

# Check Docker services
Write-Host "Checking Docker services..." -ForegroundColor Yellow
$services = docker-compose ps --format json | ConvertFrom-Json

foreach ($service in $services) {
    $name = $service.Name
    $status = $service.State
    $health = $service.Health
    
    if ($status -eq "running") {
        if ($health -eq "healthy" -or $health -eq "") {
            Write-Host "  ✓ $name - Running" -ForegroundColor Green
        } else {
            Write-Host "  ⚠ $name - Running (Health: $health)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  ✗ $name - $status" -ForegroundColor Red
        $allHealthy = $false
    }
}

Write-Host ""

# Check service endpoints
Write-Host "Checking service endpoints..." -ForegroundColor Yellow

# PostgreSQL
try {
    $pgTest = docker exec instaintelli_postgres pg_isready -U postgres 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ PostgreSQL (port 5433) - Accessible" -ForegroundColor Green
    } else {
        Write-Host "  ✗ PostgreSQL - Not ready" -ForegroundColor Red
        $allHealthy = $false
    }
} catch {
    Write-Host "  ✗ PostgreSQL - Connection failed" -ForegroundColor Red
    $allHealthy = $false
}

# MongoDB
try {
    $mongoTest = docker exec instaintelli_mongodb mongosh --eval "db.adminCommand('ping')" --quiet 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ MongoDB (port 27018) - Accessible" -ForegroundColor Green
    } else {
        Write-Host "  ✗ MongoDB - Not ready" -ForegroundColor Red
        $allHealthy = $false
    }
} catch {
    Write-Host "  ✗ MongoDB - Connection failed" -ForegroundColor Red
    $allHealthy = $false
}

# Redis
try {
    $redisTest = docker exec instaintelli_redis redis-cli ping 2>&1
    if ($redisTest -eq "PONG") {
        Write-Host "  ✓ Redis (port 6379) - Accessible" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Redis - Not responding" -ForegroundColor Red
        $allHealthy = $false
    }
} catch {
    Write-Host "  ✗ Redis - Connection failed" -ForegroundColor Red
    $allHealthy = $false
}

# MinIO
try {
    $minioTest = Invoke-WebRequest -Uri "http://localhost:9000/minio/health/live" -Method GET -TimeoutSec 2 -UseBasicParsing 2>&1
    if ($minioTest.StatusCode -eq 200) {
        Write-Host "  ✓ MinIO (port 9000) - Accessible" -ForegroundColor Green
        Write-Host "    Console: http://localhost:9001" -ForegroundColor Gray
    } else {
        Write-Host "  ⚠ MinIO - Responding but status unclear" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ✗ MinIO - Not accessible" -ForegroundColor Red
    $allHealthy = $false
}

# ChromaDB
try {
    $chromaTest = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/heartbeat" -Method GET -TimeoutSec 2 -UseBasicParsing 2>&1
    if ($chromaTest.StatusCode -eq 200) {
        Write-Host "  ✓ ChromaDB (port 8000) - Accessible" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ ChromaDB - Responding but status unclear" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ⚠ ChromaDB - Not accessible yet (may still be starting)" -ForegroundColor Yellow
}

# Backend API
try {
    $backendTest = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET -TimeoutSec 2 -UseBasicParsing 2>&1
    if ($backendTest.StatusCode -eq 200) {
        Write-Host "  ✓ Backend API (port 8000) - Accessible" -ForegroundColor Green
        Write-Host "    API Docs: http://localhost:8000/docs" -ForegroundColor Gray
    } else {
        Write-Host "  ⚠ Backend API - Responding but status unclear" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ⚠ Backend API - Not running yet" -ForegroundColor Yellow
}

# Frontend
try {
    $frontendTest = Invoke-WebRequest -Uri "http://localhost:3000" -Method GET -TimeoutSec 2 -UseBasicParsing 2>&1
    if ($frontendTest.StatusCode -eq 200) {
        Write-Host "  ✓ Frontend (port 3000) - Accessible" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Frontend - Responding but status unclear" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ⚠ Frontend - Not running yet" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
if ($allHealthy) {
    Write-Host "✓ All core services are healthy!" -ForegroundColor Green
} else {
    Write-Host "⚠ Some services need attention" -ForegroundColor Yellow
}
Write-Host "========================================" -ForegroundColor Cyan

