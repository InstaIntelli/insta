# InstaIntelli Setup Script for Windows
# Run this script to set up your development environment

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  InstaIntelli Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found! Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

# Activate venv
Write-Host ""
Write-Host "Setting up Python virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate venv
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "✅ Python dependencies installed" -ForegroundColor Green

# Install Node dependencies
Write-Host ""
Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
Set-Location frontend
npm install --silent
Set-Location ..
Write-Host "✅ Node.js dependencies installed" -ForegroundColor Green

# Create .env file
Write-Host ""
Write-Host "Setting up environment variables..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item .env.example .env
        Write-Host "✅ Created .env file from .env.example" -ForegroundColor Green
        Write-Host "⚠️  IMPORTANT: Edit .env file and add your OpenAI API key!" -ForegroundColor Red
    } else {
        Write-Host "⚠️  .env.example not found. Please create .env manually" -ForegroundColor Yellow
    }
} else {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
}

# Create necessary directories
Write-Host ""
Write-Host "Creating project directories..." -ForegroundColor Yellow
$directories = @("chroma_db", "faiss_indexes", "minio_data", "analytics\parquet")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
        Write-Host "✅ Created $dir" -ForegroundColor Green
    }
}

# Check Docker (optional)
Write-Host ""
Write-Host "Checking Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>&1
    Write-Host "✅ Docker installed: $dockerVersion" -ForegroundColor Green
    Write-Host "   You can use: docker-compose up -d" -ForegroundColor Cyan
} catch {
    Write-Host "⚠️  Docker not found (optional)" -ForegroundColor Yellow
    Write-Host "   Install Docker Desktop for easier database setup" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete! ✅" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env file with your API keys" -ForegroundColor White
Write-Host "2. Start databases:" -ForegroundColor White
Write-Host "   - Docker: docker-compose up -d" -ForegroundColor Gray
Write-Host "   - OR install manually (PostgreSQL, MongoDB, Redis, MinIO)" -ForegroundColor Gray
Write-Host "3. Start backend:" -ForegroundColor White
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   uvicorn app.main:app --reload" -ForegroundColor Gray
Write-Host "4. Start frontend (in new terminal):" -ForegroundColor White
Write-Host "   cd frontend" -ForegroundColor Gray
Write-Host "   npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""



