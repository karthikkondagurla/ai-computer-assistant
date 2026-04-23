@echo off
REM Windows Build Script for AI Computer Assistant
REM Run this script on Windows to build the executable

echo ========================================
echo Building AI Computer Assistant for Windows
echo ========================================

REM Install PyInstaller if not present
pip install pyinstaller

REM Build the executable
pyinstaller --onefile --console --name "AI-Assistant" ^
  --add-data "src;src" ^
  --hidden-import langchain_groq ^
  --hidden-import langchain ^
  --hidden-import langchain_core ^
  --hidden-import langgraph ^
  --hidden-import groq ^
  --hidden-import pyautogui ^
  --hidden-import psutil ^
  --hidden-import pyperclip ^
  --hidden-import pillow ^
  --hidden-import keyring ^
  --hidden-import secretstorage ^
  --hidden-import jeepney ^
  --hidden-import pyscreeze ^
  --hidden-import pygetwindow ^
  --hidden-import pymsgbox ^
  --hidden-import pytweening ^
  --hidden-import mouseinfo ^
  --hidden-import python3_Xlib ^
  --collect-all langchain ^
  --collect-all langchain_groq ^
  --collect-all langgraph ^
  --collect-all keyring ^
  ai_computer_assistant.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Build successful!
    echo Executable location: dist\AI-Assistant.exe
    echo ========================================
) else (
    echo.
    echo ========================================
    echo Build failed!
    echo ========================================
    exit /b 1
)

REM Optional: Build installer with Inno Setup
echo.
echo To create installer, run: iscc installer.iss
pause