@echo off
setlocal

cd /d "%~dp0"

set "PATH=C:\gtk\bin;%PATH%"
set "PYTHON=%~dp0venv314\Scripts\python.exe"

if not exist "%PYTHON%" (
    echo ERROR: venv Python not found:
    echo %PYTHON%
    pause
    exit /b 1
)

"%PYTHON%" "%~dp0oletoy\view.py"
if errorlevel 1 (
    echo.
    echo ERROR: Program crashed.
    pause
    exit /b 1
)

echo.
echo Program finished.
pause