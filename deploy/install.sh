#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "[INFO] 正在建立 Python 虛擬環境 (venv)..."
python3 -m venv venv || python -m venv venv

echo "[INFO] 啟用虛擬環境並升級 pip..."
# shellcheck disable=SC1091
source venv/bin/activate
pip install --upgrade pip

echo "[INFO] 安裝相依套件..."
pip install -r requirements.txt

echo "[SUCCESS] 虛擬環境建置與套件安裝已順利完成！"
