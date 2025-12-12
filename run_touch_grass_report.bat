@echo off
REM run_touch_grass_report.bat
REM Generates and opens the activity report.
REM Usage: Run without arguments for today, or provide a number for N days ago.

REM Default Python path - CHANGE THIS if needed
SET PYTHON_PATH=python.exe

SET SCRIPT_PATH=%~dp0activity_report.py

IF "%1"=="" (
    ECHO Generating report for today...
    "%PYTHON_PATH%" "%SCRIPT_PATH%"
) ELSE (
    ECHO Generating report for %1 days ago...
    "%PYTHON_PATH%" "%SCRIPT_PATH%" --daysago %1
)

PAUSE
