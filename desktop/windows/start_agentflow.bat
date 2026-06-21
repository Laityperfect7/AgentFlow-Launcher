@echo off
:: =============================================================================
:: AgentFlow-Launcher — Windows Desktop Launcher
:: =============================================================================
:: Double-click this file to start the AgentFlow-Launcher server and open
:: the web console in your default browser.
::
:: Prerequisites:
::   1. Run scripts\setup_windows.ps1 first to set up the environment
::   2. Copy .env.example to .env and configure your API keys (optional)
:: =============================================================================

title AgentFlow-Launcher

:: Navigate to the project directory (adjust if you moved the project)
cd /d "%~dp0..\.."

:: Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found.
    echo Please run: powershell -ExecutionPolicy Bypass -File scripts\setup_windows.ps1
    pause
    exit /b 1
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Print banner
echo ============================================================
echo   AgentFlow-Launcher
echo   Agent / Workflow / Skill 一体化构建与部署平台
echo ============================================================
echo.
echo   Local API:     http://127.0.0.1:8000
echo   Swagger Docs:  http://127.0.0.1:8000/docs
echo   Web Console:   http://127.0.0.1:8000/console
echo ============================================================
echo.

:: Open browser
start "" http://127.0.0.1:8000/console

:: Start the server
python scripts/run_server.py

pause
