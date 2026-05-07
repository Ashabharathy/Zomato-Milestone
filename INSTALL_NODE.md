# Node.js Installation Instructions

## Current Status
- ✅ Backend is running on http://localhost:8000
- ❌ Node.js/npm not installed - Frontend cannot start

## Install Node.js

### Option 1: Download from Official Website
1. Go to https://nodejs.org/
2. Download the LTS version (recommended)
3. Run the installer
4. Follow the installation wizard

### Option 2: Using Chocolatey (if installed)
```powershell
choco install nodejs
```

### Option 3: Using Winget (Windows 10+)
```powershell
winget install OpenJS.NodeJS
```

## Verify Installation
After installation, open a NEW PowerShell window and run:
```powershell
node --version
npm --version
```

## Start Frontend
Once Node.js is installed:
```powershell
cd "a:\NEXTLEAP\zomato ai recommender\frontend"
npm install
npm run dev
```

## Access the Application
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:3000
- Phase 6 Dashboard: http://localhost:3000/phase6

## Backend Status
✅ Backend is currently running on port 8000
- Database: SQLite (recs_dev.db)
- API endpoints available
- Ready for frontend connections
