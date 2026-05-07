# PowerShell Script to Start Backend and Frontend Services
# Run this script to start both services

$backendPath = "a:\NEXTLEAP\zomato ai recommender\backend"
$frontendPath = "a:\NEXTLEAP\zomato ai recommender\frontend"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Restaurant Recommendation System" -ForegroundColor Cyan
Write-Host "  Starting Backend + Frontend" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python availability
Write-Host "Checking Python..." -ForegroundColor Yellow
$pythonExists = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonExists) {
    Write-Host "ERROR: Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}
Write-Host "Python found" -ForegroundColor Green

# Check if backend dependencies are installed
Write-Host "Checking Backend Dependencies..." -ForegroundColor Yellow
try {
    python -c "import fastapi, uvicorn" 2>$null
    Write-Host "Backend dependencies OK" -ForegroundColor Green
} catch {
    Write-Host "Installing backend dependencies..." -ForegroundColor Yellow
    pip install -r "$backendPath\requirements.txt"
}

# Start Backend in a new window
Write-Host ""
Write-Host "Starting Backend Server (Port 8000)..." -ForegroundColor Green
$backendJob = Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$backendPath'; python main.py"
) -PassThru

# Wait a moment for backend to initialize
Start-Sleep -Seconds 3

# Check if backend started
$backendRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET -TimeoutSec 3 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        $backendRunning = $true
        Write-Host "Backend is running!" -ForegroundColor Green
    }
} catch {
    Write-Host "Backend may still be starting..." -ForegroundColor Yellow
}

# Check Node.js availability
Write-Host ""
Write-Host "Checking Node.js..." -ForegroundColor Yellow
$nodeExists = Get-Command npm -ErrorAction SilentlyContinue
if (-not $nodeExists) {
    Write-Host "WARNING: Node.js/npm not found. Frontend cannot start." -ForegroundColor Red
    Write-Host "Please install Node.js from https://nodejs.org/" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Backend is running at http://localhost:8000" -ForegroundColor Cyan
    Write-Host "Press any key to stop the backend..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    Stop-Process -Id $backendJob.Id -Force
    exit 1
}
Write-Host "Node.js found" -ForegroundColor Green

# Check if frontend dependencies are installed
Write-Host "Checking Frontend Dependencies..." -ForegroundColor Yellow
if (-not (Test-Path "$frontendPath\node_modules")) {
    Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
    Set-Location $frontendPath
    npm install
} else {
    Write-Host "Frontend dependencies OK" -ForegroundColor Green
}

# Start Frontend in a new window
Write-Host ""
Write-Host "Starting Frontend Server (Port 3000)..." -ForegroundColor Green
$frontendJob = Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$frontendPath'; npm run dev"
) -PassThru

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Services Started Successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend API:   http://localhost:8000" -ForegroundColor Yellow
Write-Host "API Docs:      http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "Frontend:      http://localhost:3000" -ForegroundColor Yellow
Write-Host "Phase6 Page:   http://localhost:3000/phase6" -ForegroundColor Magenta
Write-Host ""
Write-Host "Press any key to stop both services..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Cleanup
Write-Host ""
Write-Host "Stopping services..." -ForegroundColor Yellow
Stop-Process -Id $backendJob.Id -Force -ErrorAction SilentlyContinue
Stop-Process -Id $frontendJob.Id -Force -ErrorAction SilentlyContinue
Write-Host "Services stopped." -ForegroundColor Green
