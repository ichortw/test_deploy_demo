@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0.."

if not exist "venv\Scripts\python.exe" (
    echo [WARN] 偵測到尚未建立虛擬環境，正在自動執行安裝步驟...
    call deploy\install.bat
)

echo [INFO] 正在虛擬環境中啟動主程式...
"venv\Scripts\python.exe" src\main.py
if errorlevel 1 (
    echo [ERROR] 程式執行時發生錯誤。
    pause
    exit /b %errorlevel%
)
pause
