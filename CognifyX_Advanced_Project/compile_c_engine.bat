@echo off
setlocal
cd /d "%~dp0"
if not exist build mkdir build
where gcc >nul 2>nul
if errorlevel 1 (
  echo GCC was not found. Install MinGW-w64 and add its bin folder to PATH.
  pause
  exit /b 1
)
gcc -std=c11 -O2 -Wall -Wextra c_engine\cognifyx_engine.c -o build\cognifyx_engine.exe
if errorlevel 1 (
  echo Build failed. Check the error messages above.
  pause
  exit /b 1
)
echo C engine compiled successfully.
echo.
build\cognifyx_engine.exe
pause
