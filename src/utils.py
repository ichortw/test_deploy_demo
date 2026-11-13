import os
from datetime import datetime
from typing import List, Optional, Tuple
from config import PROJECT_ROOT, config

DEFAULT_EXCLUDED_DIRS: Tuple[str, ...] = ("venv", ".venv", "__pycache__", ".git")


def format_time(dt: Optional[datetime] = None, fmt: Optional[str] = None) -> str:
    """
    格式化時間並回傳字串。

    :param dt: 欲格式化的 datetime 物件，若未指定則取得目前系統時間。
    :param fmt: 格式化格式字串，未指定時套用 config.datetime_format。
    :return: 格式化後的時間字串。
    """
    target_dt = dt if dt is not None else datetime.now()
    target_fmt = fmt or config.datetime_format
    return target_dt.strftime(target_fmt)


def list_files_by_extension(
    extension: str,
    root_dir: Optional[str] = None,
    exclude_dirs: Optional[Tuple[str, ...]] = None,
) -> List[str]:
    """
    掃描指定目錄並回傳所有符合指定副檔名檔案的相對路徑清單。

    :param extension: 欲篩選的副檔名（例如 '.py'、'.bat'、'.sh'）。
    :param root_dir: 欲掃描的根目錄，未指定時預設為 PROJECT_ROOT。
    :param exclude_dirs: 欲忽略的資料夾名稱元組，未指定時使用預設排除清單。
    :return: 依字母排序後的相對路徑字串清單。
    """
    normalized_ext = extension if extension.startswith(".") else f".{extension}"
    normalized_ext = normalized_ext.lower()
    target_root = os.path.abspath(root_dir if root_dir is not None else PROJECT_ROOT)
    ignored = set(exclude_dirs if exclude_dirs is not None else DEFAULT_EXCLUDED_DIRS)
    matched_files: List[str] = []

    for dirpath, dirnames, filenames in os.walk(target_root):
        dirnames[:] = sorted(d for d in dirnames if d not in ignored)
        for filename in sorted(filenames):
            if filename.lower().endswith(normalized_ext):
                full_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(full_path, target_root)
                matched_files.append(rel_path)

    return sorted(matched_files)


def list_python_files(
    root_dir: Optional[str] = None,
    exclude_dirs: Optional[Tuple[str, ...]] = None,
) -> List[str]:
    """掃描指定目錄並回傳所有 .py 檔案的相對路徑清單。"""
    return list_files_by_extension(".py", root_dir=root_dir, exclude_dirs=exclude_dirs)


def list_bat_files(
    root_dir: Optional[str] = None,
    exclude_dirs: Optional[Tuple[str, ...]] = None,
) -> List[str]:
    """掃描指定目錄並回傳所有 .bat 檔案的相對路徑清單。"""
    return list_files_by_extension(".bat", root_dir=root_dir, exclude_dirs=exclude_dirs)


def list_sh_files(
    root_dir: Optional[str] = None,
    exclude_dirs: Optional[Tuple[str, ...]] = None,
) -> List[str]:
    """掃描指定目錄並回傳所有 .sh 檔案的相對路徑清單。"""
    return list_files_by_extension(".sh", root_dir=root_dir, exclude_dirs=exclude_dirs)
