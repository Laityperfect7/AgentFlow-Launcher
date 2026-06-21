<#
.SYNOPSIS
    One-click setup script for AgentFlow-Launcher on Windows.

.DESCRIPTION
    Creates a Python virtual environment, installs all dependencies,
    and prompts the user to configure their .env file.

.NOTES
    Run from the project root directory:
    powershell -ExecutionPolicy Bypass -File scripts/setup_windows.ps1
#>

$ErrorActionPreference = "Stop"

# Navigate to project root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
Set-Location $ProjectRoot

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  AgentFlow-Launcher — Windows Setup" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[1/4] Checking Python..." -ForegroundColor Yellow
try {
    $pyVersion = python --version 2>&1
    Write-Host "  $pyVersion" -ForegroundColor Green
} catch {
    Write-Host "  [ERROR] Python not found. Please install Python 3.10+ from https://python.org" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "[2/4] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  Virtual environment already exists, skipping." -ForegroundColor Gray
} else {
    python -m venv venv
    Write-Host "  Virtual environment created." -ForegroundColor Green
}

# Activate and install dependencies
Write-Host "[3/4] Installing dependencies..." -ForegroundColor Yellow
& .\venv\Scripts\activate.ps1
pip install --upgrade pip -q
pip install -r requirements.txt -q
Write-Host "  Dependencies installed." -ForegroundColor Green

# Configure .env
Write-Host "[4/4] Configuring environment..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  .env file already exists, skipping." -ForegroundColor Gray
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "  .env file created from .env.example." -ForegroundColor Green
    Write-Host ""
    Write-Host "  ========================================" -ForegroundColor Yellow
    Write-Host "  IMPORTANT: Edit .env to add your API keys" -ForegroundColor Yellow
    Write-Host "  (Optional: Mock mode works without keys)" -ForegroundColor Yellow
    Write-Host "  ========================================" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Setup complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. Edit .env to add your API keys (optional)"
Write-Host "  2. Run demo:  python scripts/run_demo.py"
Write-Host "  3. Run server: python scripts/run_server.py"
Write-Host "  4. Open:       http://127.0.0.1:8000/console"
Write-Host "  5. API docs:   http://127.0.0.1:8000/docs"
Write-Host ""
Write-Host "Desktop shortcut:" -ForegroundColor White
Write-Host "  powershell -ExecutionPolicy Bypass -File desktop/windows/create_shortcut.ps1"
Write-Host ""
