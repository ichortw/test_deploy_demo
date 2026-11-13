import sys
from typing import Optional

try:
    import requests
except ImportError:
    requests = None
    import json
    import urllib.request
    import urllib.error

from config import config


def fetch_ip_address() -> Optional[str]:
    """
    透過外部服務取得當前公網 IP 位址並印出，成功時回傳 IP 字串。
    優先使用 requests 套件，若未安裝則自動降級為標準庫 urllib。
    """
    if requests:
        try:
            response = requests.get(config.ip_api_url, timeout=config.request_timeout)
            response.raise_for_status()
            data = response.json()
            ip = data.get("ip") or data.get("origin")
            if ip:
                print(f"目前外部 IP 位址: {ip}")
                return str(ip)
            print(f"無法解析 IP 位址，回應內容: {response.text}")
        except requests.exceptions.RequestException as exc:
            print(f"取得 IP 位址時發生錯誤 (requests): {exc}", file=sys.stderr)
        except ValueError as exc:
            print(f"解析 JSON 回應時發生錯誤: {exc}", file=sys.stderr)
    else:
        try:
            req = urllib.request.Request(config.ip_api_url, headers={"User-Agent": "Python-urllib"})
            with urllib.request.urlopen(req, timeout=config.request_timeout) as resp:
                body = resp.read().decode("utf-8")
                data = json.loads(body)
                ip = data.get("ip") or data.get("origin")
                if ip:
                    print(f"目前外部 IP 位址: {ip}")
                    return str(ip)
                print(f"無法解析 IP 位址，回應內容: {body}")
        except Exception as exc:
            print(f"取得 IP 位址時發生錯誤 (標準庫 urllib): {exc}", file=sys.stderr)
    return None
