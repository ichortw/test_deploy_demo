@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0.."

echo [INFO] 正在建立 Python 虛擬環境 (venv)...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] 虛擬環境建立失敗，請確認已安裝 Python 且已加入 PATH。
    pause
    exit /b 1
)

echo [INFO] 啟用虛擬環境並升級 pip...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip

echo [INFO] 安裝相依套件...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] 套件安裝失敗。
    pause
    exit /b 1
)

echo [SUCCESS] 虛擬環境建置與套件安裝已順利完成！
pause
