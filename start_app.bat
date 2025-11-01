@echo off
echo ========================================
echo Starting Review Analysis System
echo ========================================
echo.

echo [1/3] Checking if config.py exists...
if not exist "config.py" (
    echo [ERROR] config.py not found!
    echo Please copy config.template.py to config.py and add your credentials
    pause
    exit /b 1
)
echo [OK] config.py found
echo.

echo [2/3] Checking if Ollama server is running...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Ollama server not detected!
    echo Please start Ollama in a separate terminal: ollama serve
    echo.
    echo Press any key to continue anyway, or Ctrl+C to cancel...
    pause >nul
)
echo [OK] Continuing...
echo.

echo [3/3] Starting Flask application...
echo The app will be available at: http://127.0.0.1:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

pause
