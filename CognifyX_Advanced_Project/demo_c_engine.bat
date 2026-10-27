@echo off
setlocal
cd /d "%~dp0"
if not exist build\cognifyx_engine.exe (
  call compile_c_engine.bat
  if errorlevel 1 exit /b 1
)
echo =============================================
echo           CognifyX C Engine Demo
echo =============================================
echo.
echo [1] Example score: 7 correct, 2 wrong, 1 skipped
build\cognifyx_engine.exe score 7 2 1 402 10
echo.
echo [2] Adaptive response after a correct answer (level 2)
build\cognifyx_engine.exe adapt 2 1
echo.
echo [3] Weakest topic recommendation
build\cognifyx_engine.exe recommend 62 82 74 78
echo.
pause
