import sys
from pathlib import Path
import json
from typing import List, Dict, Any
from pydantic import BaseModel, Field

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_PATH = BASE_DIR / "config.json"

class ServerConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080
    secret_key: str = "nethub-secret-default-key"

class GoogleOAuthConfig(BaseModel):
    client_id: str = ""
    client_secret: str = ""
    redirect_uri: str = "http://localhost:8080/auth/callback"
    allowed_emails: List[str] = Field(default_factory=list)

class AppShortcut(BaseModel):
    id: str
    name: str
    path: str
    description: str = ""

def get_default_apps() -> List[AppShortcut]:
    return [
        AppShortcut(id="notepad", name="Блокнот (Notepad)", path="notepad.exe", description="Стандартный текстовый редактор Windows"),
        AppShortcut(id="calc", name="Калькулятор", path="calc.exe", description="Системный калькулятор Windows"),
        AppShortcut(id="taskmgr", name="Диспетчер задач", path="taskmgr.exe", description="Мониторинг процессов и ресурсов Windows"),
        AppShortcut(id="cmd", name="Командная строка", path="cmd.exe", description="Терминал Windows CMD")
    ]

class AppConfig(BaseModel):
    server: ServerConfig = Field(default_factory=ServerConfig)
    google_oauth: GoogleOAuthConfig = Field(default_factory=GoogleOAuthConfig)
    apps: List[AppShortcut] = Field(default_factory=get_default_apps)

def load_config() -> AppConfig:
    """Загрузка конфигурации из config.json или создание дефолтной."""
    if not CONFIG_PATH.exists():
        default_cfg = AppConfig()
        save_config(default_cfg)
        return default_cfg
    
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return AppConfig(**data)
    except Exception as e:
        print(f"[!] Ошибка загрузки config.json: {e}. Используются дефолтные параметры.")
        return AppConfig()

def save_config(config: AppConfig) -> None:
    """Сохранение конфигурации в файл config.json."""
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config.model_dump(), f, indent=2, ensure_ascii=False)
