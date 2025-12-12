@echo off
REM delete_touch_grass_task.bat
REM Removes the Touch Grass scheduled task.

ECHO Deleting scheduled task...
schtasks /DELETE /TN "TouchGrass\ContinuousLogger" /F

IF %ERRORLEVEL% EQU 0 (
    ECHO Task deleted successfully.
) ELSE (
    ECHO Task not found or could not be deleted.
)
PAUSE
