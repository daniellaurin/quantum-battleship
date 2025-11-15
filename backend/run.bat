@echo off
REM Quantum Battleship Backend Runner (Windows)
REM This script sets up and runs the Flask server

echo.
echo ==============================
echo Quantum Battleship Backend
echo ==============================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
)

echo.
echo Setup complete!
echo.
echo Starting Flask server...
echo Server will be available at: http://localhost:5000
echo Press Ctrl+C to stop
echo.

REM Run the Flask app
python app.py

pause