@echo off
echo ========================================
echo Review Analysis System - Setup Checker
echo ========================================
echo.

echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [FAIL] Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    goto :end
) else (
    python --version
    echo [OK] Python is installed
)
echo.

echo [2/5] Checking Ollama installation...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [FAIL] Ollama is not installed or not in PATH
    echo Please install from https://ollama.com/
    goto :end
) else (
    ollama --version
    echo [OK] Ollama is installed
)
echo.

echo [3/5] Checking if DeepSeek model is pulled...
ollama list | findstr "deepseek-llm" >nul 2>&1
if %errorlevel% neq 0 (
    echo [FAIL] DeepSeek model not found
    echo Please run: ollama pull deepseek-llm:7b
    goto :end
) else (
    echo [OK] DeepSeek model is available
)
echo.

echo [4/5] Checking if config.py exists...
if not exist "config.py" (
    echo [FAIL] config.py not found
    echo Please copy config.template.py to config.py and fill in your credentials
    goto :end
) else (
    echo [OK] config.py exists
)
echo.

echo [5/5] Checking if Ollama server is running...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Ollama server might not be running
    echo Please run: ollama serve
    echo (in a separate terminal window)
) else (
    echo [OK] Ollama server is running
)
echo.

echo ========================================
echo Setup check complete!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure Ollama is running: ollama serve
echo 2. Update config.py with your Oxylabs credentials
echo 3. Run the app: python app.py
echo 4. Open browser: http://127.0.0.1:5000
echo.

:end
pause
