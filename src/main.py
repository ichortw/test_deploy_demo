import sys
from typing import Dict, List
from config import config
from network import fetch_ip_address
from utils import format_time, list_bat_files, list_python_files, list_sh_files


def display_current_time() -> str:
    """透過 utils.format_time 取得格式化時間並印出，同時回傳字串。"""
    formatted_time = format_time()
    print(f"系統當前時間: {formatted_time}")
    return formatted_time


def display_python_files() -> List[str]:
    """掃描並顯示專案內所有 .py 檔案數量與清單，同時回傳清單。"""
    py_files = list_python_files()
    print(f"專案 .py 檔案總數: {len(py_files)}")
    for idx, file_path in enumerate(py_files, start=1):
        print(f"  {idx}. {file_path}")
    return py_files


def display_deploy_scripts() -> Dict[str, List[str]]:
    """掃描並顯示專案內所有 .bat 與 .sh 檔案數量與清單，同時回傳統計字典。"""
    bat_files = list_bat_files()
    print(f"專案 .bat 檔案總數: {len(bat_files)}")
    for idx, file_path in enumerate(bat_files, start=1):
        print(f"  {idx}. {file_path}")

    sh_files = list_sh_files()
    print(f"專案 .sh 檔案總數: {len(sh_files)}")
    for idx, file_path in enumerate(sh_files, start=1):
        print(f"  {idx}. {file_path}")

    return {".bat": bat_files, ".sh": sh_files}


def run_workflow() -> bool:
    """
    執行核心業務流程：
    1. 顯示系統時間
    2. 列出專案中的 .py 檔案數量與清單
    3. 列出專案中的 .bat 與 .sh 檔案數量與清單
    4. 取得並顯示外部公網 IP
    :return: 流程是否完整成功
    """
    display_current_time()
    display_python_files()
    display_deploy_scripts()
    ip_addr = fetch_ip_address()
    return ip_addr is not None


def main() -> int:
    """
    主程式進入點：
    負責初始化系統狀態、顯示環境配置，並調用各模組功能。
    :return: 系統退出狀態碼 (Exit Code)
    """
    try:
        print(f"[INFO] 程式版本: {config.app_version}")
        print("[INFO] chortw coder 運作正常！")

        # 顯示當前配置之模型資訊與思考預算
        print(f"[INFO] 模型代號: {config.model_name} | 思考預算設定: {config.thinking_budget}")

        success = run_workflow()
        if not success:
            print("[WARN] 部分網路檢測流程未能順利取得結果，請檢查網路連線。", file=sys.stderr)
        return 0
    except KeyboardInterrupt:
        print("\n[WARN] 接收到中斷訊號，程式即將結束。", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"[ERROR] 程式執行期間發生未預期錯誤: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
