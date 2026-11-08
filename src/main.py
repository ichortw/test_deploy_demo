import os
import sys
from datetime import datetime

# 嘗試載入 python-dotenv，若未安裝則提供降級處理並輸出警示
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("[WARN] 未安裝 'python-dotenv' 套件。請確認已啟動虛擬環境或執行 'pip install -r requirements.txt'。", file=sys.stderr)
    # 簡易讀取同專案目錄或當前目錄下的 .env 作為備用支援
    env_file_candidates = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"),
        os.path.join(os.getcwd(), ".env")
    ]
    for env_path in env_file_candidates:
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, val = line.split("=", 1)
                            os.environ.setdefault(key.strip(), val.strip())
            except Exception as e:
                print(f"[WARN] 讀取 .env 檔案失敗: {e}", file=sys.stderr)
            break

# 嘗試載入 requests
try:
    import requests
except ImportError:
    requests = None
    print("[WARN] 未安裝 'requests' 套件，將降級使用標準庫 urllib.request。", file=sys.stderr)
    import json
    import urllib.request
    import urllib.error

IP_API_URL = os.getenv("IP_API_URL", "https://api.ipify.org?format=json")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
DATETIME_FORMAT = os.getenv("DATETIME_FORMAT", "%Y-%m-%d %H:%M:%S")

def display_current_time() -> str:
    """讀取系統當前時間並依照設定格式印出，並回傳格式化字串。"""
    now = datetime.now()
    formatted_time = now.strftime(DATETIME_FORMAT)
    print(f"系統當前時間: {formatted_time}")
    return formatted_time

def fetch_ip_address():
    """透過外部服務取得當前公網 IP 位址並印出。"""
    if requests:
        try:
            response = requests.get(IP_API_URL, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            ip = data.get("ip") or data.get("origin")
            if ip:
                print(f"目前外部 IP 位址: {ip}")
            else:
                print(f"無法解析 IP 位址，回應內容: {response.text}")
        except requests.exceptions.RequestException as exc:
            print(f"取得 IP 位址時發生錯誤: {exc}", file=sys.stderr)
    else:
        try:
            req = urllib.request.Request(IP_API_URL, headers={"User-Agent": "Python-urllib"})
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                body = resp.read().decode("utf-8")
                data = json.loads(body)
                ip = data.get("ip") or data.get("origin")
                if ip:
                    print(f"目前外部 IP 位址: {ip}")
                else:
                    print(f"無法解析 IP 位址，回應內容: {body}")
        except Exception as exc:
            print(f"取得 IP 位址時發生錯誤 (標準庫): {exc}", file=sys.stderr)

def main():
    print("chortw coder 運作正常！")
    display_current_time()
    fetch_ip_address()

if __name__ == "__main__":
    main()
