@echo off
set PYTHONSCRIPTPATH=C:\Users\Utilizador\Desktop\CODE\Lib\site-packages
set PYTHONPATH=%PYTHONSCRIPTPATH%

REM Ensure the paths are correct
echo PYTHONSCRIPTPATH: %PYTHONSCRIPTPATH%
echo PYTHONPATH: %PYTHONPATH%

REM Check if Python script exists
if exist C:\Users\Utilizador\Desktop\codePY\KeyListenerAndBlocker\FinalShutdownVer.py (
    echo Python script found.
) else (
    echo Python script not found. > C:\Users\Utilizador\Desktop\codePY\KeyListenerAndBlocker\logfile.txt
    pause
    exit /b
)

REM Start the Python script and log errors
:START
python C:\Users\Utilizador\Desktop\codePY\KeyListenerAndBlocker\FinalShutdownVer.py > C:\Users\Utilizador\Desktop\codePY\KeyListenerAndBlocker\logfile.txt 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo %DATE% %TIME% - Script crashed with exit code %ERRORLEVEL%. >> C:\Users\Utilizador\Desktop\codePY\KeyListenerAndBlocker\logfile.txt
    echo Restarting... >> C:\Users\Utilizador\Desktop\codePY\KeyListenerAndBlocker\logfile.txt
    goto START
)

pause

