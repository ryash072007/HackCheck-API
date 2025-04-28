@echo off
setlocal

REM 1. Set up virtual environment and install requirements
echo [*] Setting up the virtual environment...
python -m venv .venv
call .venv\Scripts\activate.bat

echo [*] Installing dependencies from requirements.txt...
pip install --upgrade pip
pip install -r requirements.txt

echo [*] Setup complete. Press any key to exit this window.
pause

endlocal
