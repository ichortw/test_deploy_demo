#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -f "venv/bin/python" ]; then
    echo "[WARN] 偵測到尚未建立虛擬環境，正在自動執行安裝步驟..."
    bash deploy/install.sh
fi

echo "[INFO] 正在虛擬環境中啟動主程式..."
venv/bin/python src/main.py
