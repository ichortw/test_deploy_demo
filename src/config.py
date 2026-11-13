import os
import sys
from dataclasses import dataclass

# 專案目錄判定
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
for path in (CURRENT_DIR, PROJECT_ROOT):
    if path not in sys.path:
        sys.path.insert(0, path)

# 嘗試載入 python-dotenv
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(PROJECT_ROOT, ".env"))
except ImportError:
    env_path = os.path.join(PROJECT_ROOT, ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, val = line.split("=", 1)
                        os.environ.setdefault(key.strip(), val.strip())
        except Exception as exc:
            print(f"[WARN] 讀取 .env 檔案失敗: {exc}", file=sys.stderr)


def get_env_int(key: str, default: int) -> int:
    val = os.getenv(key)
    if val is None:
        return default
    try:
        return int(val)
    except ValueError:
        print(f"[WARN] 環境變數 {key} 格式無效，使用預設值 {default}", file=sys.stderr)
        return default


@dataclass(frozen=True)
class AppConfig:
    app_version: str = "v1.5.0"
    model_name: str = os.getenv("MODEL_NAME", "gemini-2.5-flash")
    thinking_budget: str = os.getenv("THINKING_BUDGET", "0.05")
    ip_api_url: str = os.getenv("IP_API_URL", "https://api.ipify.org?format=json")
    request_timeout: int = get_env_int("REQUEST_TIMEOUT", 10)
    datetime_format: str = os.getenv("DATETIME_FORMAT", "%Y-%m-%d %H:%M:%S")


config = AppConfig()
