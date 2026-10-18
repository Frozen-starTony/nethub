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
from core.i18n import t, get_system_lang
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

def get_banner():
    subtitle = t("banner_subtitle")
    return f"""{CYAN}{ASCII_ART}{RESET}{BOLD}   {subtitle}
   Release: 1.0.0 | Language: {get_system_lang().upper()}
{RESET}"""

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def run_web_server(config):
    port = config.server.port
    host = config.server.host
    display_url = f"http://localhost:{port}"

    print(f"\n{GREEN}{'='*60}{RESET}")
    print(f"{BOLD}{GREEN}  [OK] {t('web_running')} {display_url}{RESET}")
    print(f"{YELLOW}  [INFO] {t('web_ctrl_c')}{RESET}")
    print(f"{GREEN}{'='*60}{RESET}\n")

    # Автоматическое открытие в браузере Windows
    try:
        webbrowser.open(display_url)
    except Exception:
        pass

    app = create_app(config)
    uvicorn.run(app, host=host, port=port, log_level="info")

def main():
    if os.name == "nt":
        os.system("")

    clear_screen()
    print(get_banner())

    config = load_config()

    print(f"{YELLOW}[INFO] {t('probing_gateway')}{RESET}")
    try:
        external_ip = asyncio.run(get_external_ip())
    except Exception as e:
        external_ip = f"Unreachable ({e})"

    print(f"{BOLD}{t('public_ip_label')}{RESET} {GREEN}{BOLD}{external_ip}{RESET}\n")
    print(f"{CYAN}{'-'*60}{RESET}")

    while True:
        print(f"{BOLD}{t('select_mode')}{RESET}")
        print(f"  [{BOLD}1{RESET}] {t('mode_cli')}")
        print(f"  [{BOLD}2{RESET}] {t('mode_web')}")
        print(f"  [{BOLD}0{RESET}] {t('mode_exit')}")

        mode = input(f"\n{BOLD}{t('action_prompt')}{RESET}").strip()

        if mode == "1":
            action = start_cli_loop(config)
            if action == "SWITCH_TO_WEB":
                run_web_server(config)
            break
        elif mode == "2":
            run_web_server(config)
            break
        elif mode == "0":
            print(f"\n{CYAN}{t('shutdown')}{RESET}")
            sys.exit(0)
        else:
            print(f"{RED}[ERR] {t('invalid_choice')}{RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}[INFO] Shutdown signal received.{RESET}")
        sys.exit(0)
