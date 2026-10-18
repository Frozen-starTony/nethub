import os
import sys
import asyncio
import webbrowser
import uvicorn

# Добавляем корневую директорию проекта в sys.path
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from core.config import load_config
from core.network import get_external_ip
from cli.terminal import start_cli_loop
from web.server import create_app

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

ASCII_ART = r"""
  _   _      _   _   _       _     
 | \ | | ___| |_| | | |_   _| |__  
 |  \| |/ _ \ __| |_| | | | | '_ \ 
 | |\  |  __/ |_|  _  | |_| | |_) |
 |_| \_|\___|\__|_| |_|\__,_|_.__/ 
"""

BANNER = f"{CYAN}{ASCII_ART}{RESET}{BOLD}   Windows 11 Hybrid Network Toolkit (CLI + Web UI)\n   Версия: 1.0.0\n{RESET}"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def run_web_server(config):
    port = config.server.port
    host = config.server.host
    display_url = f"http://localhost:{port}"

    print(f"\n{GREEN}{'='*60}{RESET}")
    print(f"{BOLD}{GREEN}  [✓] Веб-панель запущена на {display_url}{RESET}")
    print(f"{YELLOW}  [i] Нажмите Ctrl+C в этом окне для остановки сервера.{RESET}")
    print(f"{GREEN}{'='*60}{RESET}\n")

    # Автоматическое открытие в браузере Windows
    try:
        webbrowser.open(display_url)
    except Exception:
        pass

    app = create_app(config)
    uvicorn.run(app, host=host, port=port, log_level="info")

def main():
    # Включение поддержки ANSI цветов в Windows консоли
    if os.name == "nt":
        os.system("")

    clear_screen()
    print(BANNER)

    # 1. Загрузка конфигурации
    config = load_config()

    # 2. Сбор первичных данных: определение внешнего IP
    print(f"{YELLOW}[*] Сбор первичных сетевых данных... Пожалуйста, подождите.{RESET}")
    try:
        external_ip = asyncio.run(get_external_ip())
    except Exception as e:
        external_ip = f"Ошибка ({e})"

    print(f"{BOLD}Текущий внешний IP-адрес:{RESET} {GREEN}{BOLD}{external_ip}{RESET}\n")
    print(f"{CYAN}{'-'*60}{RESET}")

    # 3. Интерактивный выбор режима работы
    while True:
        print(f"{BOLD}Выберите режим работы программы:{RESET}")
        print(f"  [{BOLD}1{RESET}] Продолжить работу в терминале ({CYAN}CLI режим{RESET})")
        print(f"  [{BOLD}2{RESET}] Запустить веб-панель управления ({GREEN}Web UI режим{RESET})")
        print(f"  [{BOLD}0{RESET}] Выход")

        mode = input(f"\n{BOLD}Ваш выбор [1/2/0]: {RESET}").strip()

        if mode == "1":
            action = start_cli_loop(config)
            if action == "SWITCH_TO_WEB":
                run_web_server(config)
            break
        elif mode == "2":
            run_web_server(config)
            break
        elif mode == "0":
            print(f"\n{CYAN}До встречи! Завершение NetHub.{RESET}")
            sys.exit(0)
        else:
            print(f"{RED}[!] Неверная команда. Введите 1, 2 или 0.{RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}[!] Принудительное завершение пользователем.{RESET}")
        sys.exit(0)
