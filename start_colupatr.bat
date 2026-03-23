@echo off
setlocal

set "ROOT=%~dp0"
set "PATH=C:\gtk\bin;%PATH%"
set "PYTHON=%ROOT%venv314\Scripts\python.exe"

if not exist "%PYTHON%" (
    echo ERROR: venv Python not found:
    echo %PYTHON%
    pause
    exit /b 1
)

cd /d "%ROOT%colupatr"

"%PYTHON%" colupatr.py

if errorlevel 1 (
    echo.
    echo ERROR: Program crashed.
    pause
    exit /b 1
)

echo.
echo Program finished.
pause