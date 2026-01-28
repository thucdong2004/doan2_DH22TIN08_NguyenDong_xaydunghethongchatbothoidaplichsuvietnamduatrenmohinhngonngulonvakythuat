@echo off
echo ========================================
echo Vietnamese History Chatbot - Fix Database
echo ========================================
echo.
echo This will force recreate the database.
echo Make sure app.py is NOT running!
echo.
pause

echo.
echo Step 1: Killing any running Python processes...
taskkill /F /IM python.exe /T 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Step 2: Clearing and recreating database...
python init_db.py --clear

echo.
echo Done! Press any key to exit.
pause
