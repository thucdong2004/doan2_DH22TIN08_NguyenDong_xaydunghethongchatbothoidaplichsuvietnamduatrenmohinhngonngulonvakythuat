@echo off
echo ========================================
echo Vietnamese History Chatbot - DEMO
echo ========================================
echo.
echo This script will:
echo 1. Check if Ollama is running
echo 2. Initialize/verify database
echo 3. Run automated tests
echo 4. Start the chatbot interface
echo.
pause

echo.
echo Step 1: Checking Ollama...
ollama list
if %errorlevel% neq 0 (
    echo ERROR: Ollama is not running!
    echo Please start Ollama first: ollama serve
    pause
    exit /b 1
)

echo.
echo Step 2: Verifying database...
if not exist "chroma_db" (
    echo Database not found. Creating...
    python init_db.py
) else (
    echo Database exists. Skipping initialization.
)

echo.
echo Step 3: Running automated tests...
echo This will test the chatbot with sample questions.
echo.
python test_chatbot.py

echo.
echo ========================================
echo Tests completed! 
echo ========================================
echo.
echo Press any key to start the chatbot interface...
pause

echo.
echo Starting chatbot...
streamlit run app.py
