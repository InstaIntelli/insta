# ============================================
# INSTAINTELLI - PowerShell Docker Commands
# ============================================
# Common Docker commands for Windows development
# Usage: .\scripts\docker-commands.ps1 <command>

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "InstaIntelli - Docker Commands (PowerShell)" -ForegroundColor Cyan
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Available commands:" -ForegroundColor Yellow
    Write-Host "  build          - Build all Docker images"
    Write-Host "  up             - Start all services"
    Write-Host "  down           - Stop all services"
    Write-Host "  restart        - Restart all services"
    Write-Host "  logs           - View logs from all services"
    Write-Host "  logs-backend   - View backend logs"
    Write-Host "  logs-frontend  - View frontend logs"
    Write-Host "  clean          - Remove containers, volumes, and images"
    Write-Host "  test           - Run tests in backend container"
    Write-Host "  migrate        - Run database migrations"
    Write-Host "  shell-backend  - Open shell in backend container"
    Write-Host "  shell-postgres - Open PostgreSQL shell"
    Write-Host "  shell-mongodb  - Open MongoDB shell"
    Write-Host "  shell-redis     - Open Redis CLI"
    Write-Host "  health         - Check service health"
    Write-Host ""
}

switch ($Command.ToLower()) {
    "build" {
        Write-Host "Building Docker images..." -ForegroundColor Green
        docker-compose build
    }
    "up" {
        Write-Host "Starting all services..." -ForegroundColor Green
        docker-compose up -d
    }
    "up-logs" {
        Write-Host "Starting all services with logs..." -ForegroundColor Green
        docker-compose up
    }
    "down" {
        Write-Host "Stopping all services..." -ForegroundColor Yellow
        docker-compose down
    }
    "down-volumes" {
        Write-Host "Stopping services and removing volumes..." -ForegroundColor Yellow
        docker-compose down -v
    }
    "restart" {
        Write-Host "Restarting all services..." -ForegroundColor Green
        docker-compose restart
    }
    "logs" {
        docker-compose logs -f
    }
    "logs-backend" {
        docker-compose logs -f backend
    }
    "logs-frontend" {
        docker-compose logs -f frontend
    }
    "clean" {
        Write-Host "Cleaning Docker resources..." -ForegroundColor Yellow
        docker-compose down -v --rmi all
    }
    "test" {
        Write-Host "Running tests..." -ForegroundColor Green
        docker-compose exec backend pytest
    }
    "migrate" {
        Write-Host "Running database migrations..." -ForegroundColor Green
        docker-compose exec backend alembic upgrade head
    }
    "shell-backend" {
        docker-compose exec backend /bin/bash
    }
    "shell-postgres" {
        docker-compose exec postgres psql -U postgres -d instaintelli
    }
    "shell-mongodb" {
        docker-compose exec mongodb mongosh instaintelli
    }
    "shell-redis" {
        docker-compose exec redis redis-cli
    }
    "rebuild" {
        Write-Host "Rebuilding and restarting services..." -ForegroundColor Green
        docker-compose up -d --build
    }
    "health" {
        Write-Host "Checking service health..." -ForegroundColor Cyan
        docker-compose ps
        Write-Host "`nBackend health:" -ForegroundColor Cyan
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing
            Write-Host $response.Content -ForegroundColor Green
        } catch {
            Write-Host "Backend not responding" -ForegroundColor Red
        }
        Write-Host "`nFrontend: http://localhost:3000" -ForegroundColor Cyan
        Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
    }
    default {
        Show-Help
    }
}


