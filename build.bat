@echo off
echo Building Tool...
echo.

REM Run PyInstaller
pyinstaller --onefile --name "Audio Bitrate Calculator" ^
  --hidden-import tkinterdnd2 ^
  --windowed ^
  --icon=app-icon.png ^
  "Audio Bitrate Calculator.py"

echo.
echo Build complete! Check the 'dist' folder for the executable.
pause