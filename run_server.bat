@echo off
setlocal enabledelayedexpansion

REM ========================================
REM HackCheck API Server Launcher
REM ========================================

echo.
echo [===== HackCheck API Server Launcher =====]
echo.

REM Activate the virtual environment
echo [INFO] Activating virtual environment...
call .\.venv\Scripts\activate.bat || (
    echo [ERROR] Failed to activate virtual environment.
    echo         Make sure .venv directory exists.
    goto :error
)

REM Get the IP address
echo [INFO] Detecting network information...
set "FOUND_IP=0"
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    if !FOUND_IP!==0 (
        set IP=%%a
        set "FOUND_IP=1"
    )
)

if "%FOUND_IP%"=="0" (
    echo [WARNING] Couldn't detect IP address.
    set IP=localhost
) else (
    REM Remove leading space from IP
    set IP=%IP:~1%
)

REM Display the server information
echo.
echo [===== CONNECTION INFORMATION =====]
echo.
echo [IMPORTANT] For Frontend Configuration
echo.
echo   Configure the frontend with:
echo   API_BASE_URL = "http://%IP%:8000"
echo   in utils -> api.js
echo.
echo [SERVER URL] http://%IP%:8000
echo.
echo [===================================]
echo.
echo [INFO] Starting Django development server...
echo       Press CTRL+C to stop the server.
echo.

REM Run the Django server
python manage.py runserver 0.0.0.0:8000

REM Server was stopped
echo.
echo [INFO] Server has been stopped.

REM Deactivate the virtual environment
call deactivate
goto :end

:error
echo.
echo [ERROR] Server startup failed.
echo.

:end
endlocal