@echo off
setlocal
cd /d "%~dp0"
echo =============================================
echo       CognifyX Advanced - Local Launcher
echo =============================================
echo.
where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install Python 3 and enable Add Python to PATH.
  pause
  exit /b 1
)
start "CognifyX Browser" cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:8765"
python server.py
pause
