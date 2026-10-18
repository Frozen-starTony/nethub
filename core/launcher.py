import os
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
from core.config import AppConfig

def launch_application(app_id: str, config: AppConfig) -> Dict[str, Any]:
    """
    Безопасный запуск преднастроенных приложений, ярлыков (.lnk) или скриптов.
    Запуск разрешен ТОЛЬКО для программ, зарегистрированных в config.json.
    """
    # Поиск приложения в белом списке конфигурации
    target_app = next((app for app in config.apps if app.id == app_id), None)
    
    if not target_app:
        return {
            "success": False,
            "error": f"Приложение с ID '{app_id}' не найдено в конфигурации!"
        }

    raw_path = target_app.path.strip()
    
    try:
        # Для ярлыков .lnk или зарегистрированных системных утилит (calc, notepad)
        # Используем встроенный механизм Windows os.startfile
        if hasattr(os, "startfile"):
            os.startfile(raw_path)
            return {
                "success": True,
                "app_id": app_id,
                "name": target_app.name,
                "path": raw_path,
                "message": f"Приложение '{target_app.name}' успешно запущено в Windows."
            }
        else:
            # Fallback для запуска через subprocess
            proc = subprocess.Popen(
                raw_path,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return {
                "success": True,
                "app_id": app_id,
                "name": target_app.name,
                "pid": proc.pid,
                "message": f"Процесс '{target_app.name}' запущен (PID {proc.pid})."
            }
    except Exception as e:
        return {
            "success": False,
            "app_id": app_id,
            "name": target_app.name,
            "error": f"Ошибка при запуске '{raw_path}': {str(e)}"
        }
