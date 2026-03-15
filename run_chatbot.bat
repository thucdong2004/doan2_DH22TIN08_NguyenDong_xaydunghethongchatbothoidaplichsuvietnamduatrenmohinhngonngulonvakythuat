@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Initializing database...
python init_db.py

echo.
echo Starting Chatbot...
streamlit run app.py

pause
