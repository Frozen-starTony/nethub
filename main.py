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

BANNER = f"""{CYAN}{ASCII_ART}{RESET}{BOLD}   Windows 11 White IP Inspector, UPnP Port Forwarder & Host Controller
   Release: 1.0.0
{RESET}"""



def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def run_web_server(config):
    port = config.server.port
    host = config.server.host
    display_url = f"http://localhost:{port}"

    print(f"\n{GREEN}{'='*60}{RESET}")
    print(f"{BOLD}{GREEN}  [OK] Web control panel running on {display_url}{RESET}")
    print(f"{YELLOW}  [INFO] Press Ctrl+C in this console to terminate server.{RESET}")
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
    print(BANNER)

    config = load_config()

    print(f"{YELLOW}[INFO] Probing public network gateway...{RESET}")
    try:
        external_ip = asyncio.run(get_external_ip())
    except Exception as e:
        external_ip = f"Unreachable ({e})"

    print(f"{BOLD}Public IP Address:{RESET} {GREEN}{BOLD}{external_ip}{RESET}\n")
    print(f"{CYAN}{'-'*60}{RESET}")

    while True:
        print(f"{BOLD}Select Execution Mode:{RESET}")
        print(f"  [{BOLD}1{RESET}] Interactive Terminal ({CYAN}CLI Mode{RESET})")
        print(f"  [{BOLD}2{RESET}] Self-Hosted Web UI ({GREEN}Web UI Mode{RESET})")
        print(f"  [{BOLD}0{RESET}] Exit")

        mode = input(f"\n{BOLD}Action [1/2/0]: {RESET}").strip()

        if mode == "1":
            action = start_cli_loop(config)
            if action == "SWITCH_TO_WEB":
                run_web_server(config)
            break
        elif mode == "2":
            run_web_server(config)
            break
        elif mode == "0":
            print(f"\n{CYAN}NetHub process terminated.{RESET}")
            sys.exit(0)
        else:
            print(f"{RED}[ERR] Invalid command selection. Expected 1, 2 or 0.{RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}[INFO] Shutdown signal received.{RESET}")
        sys.exit(0)
