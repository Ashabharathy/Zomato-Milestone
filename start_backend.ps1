# Start Backend Server
Write-Host "Starting Backend Server..." -ForegroundColor Green
Write-Host "URL: http://localhost:8000" -ForegroundColor Yellow
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host ""
Set-Location "a:\NEXTLEAP\zomato ai recommender\backend"
python main.py
