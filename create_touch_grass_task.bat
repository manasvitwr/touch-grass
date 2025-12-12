@echo off
REM create_touch_grass_task.bat
REM Creates a scheduled task to run Touch Grass continuous tracking at logon.

REM Default Python path - CHANGE THIS if Python is not in your PATH or you want a specific venv
SET PYTHON_PATH=python.exe
REM Example: SET PYTHON_PATH=C:\Users\YourName\AppData\Local\Programs\Python\Python39\python.exe

REM Set script path relative to this batch file
SET SCRIPT_PATH=%~dp0touch_grass.py

ECHO Creating scheduled task...
schtasks /CREATE /SC ONLOGON /TN "TouchGrass\ContinuousLogger" /TR "\"%PYTHON_PATH%\" \"%SCRIPT_PATH%\" --continuous" /RU "%USERNAME%"

IF %ERRORLEVEL% EQU 0 (
    ECHO Task created successfully! Tracking will start on next logon.
) ELSE (
    ECHO Error creating task. Please check permissions or syntax.
)
PAUSE
