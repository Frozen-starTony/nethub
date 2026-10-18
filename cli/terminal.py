import asyncio
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from core.network import scan_ports, ping_host, get_network_interfaces, get_external_ip
from core.config import AppConfig

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

def print_cli_header():
    print(f"\n{CYAN}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}             NETHUB // КОНСОЛЬНЫЙ ТЕРМИНАЛ (CLI){RESET}")
    print(f"{CYAN}{'='*60}{RESET}\n")

def run_port_scanner():
    print(f"\n{BOLD}[+] СКАНИРОВАНИЕ ПОРТОВ (PORT SCANNER){RESET}")
    host = input("-> Введите IP или домен (например, 127.0.0.1 или scanme.nmap.org): ").strip()
    if not host:
        print(f"{RED}[!] Хост не может быть пустым!{RESET}")
        return

    ports_input = input("-> Укажите порты (диапазон '1-1000' или через запятую '80,443,8080'): ").strip()
    if not ports_input:
        ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 1433, 3306, 3389, 5432, 8000, 8080]
        print(f"{YELLOW}[i] Используется стандартный список популярных портов ({len(ports)} шт.){RESET}")
    elif "-" in ports_input:
        try:
            start_p, end_p = map(int, ports_input.split("-"))
            ports = list(range(max(1, start_p), min(65535, end_p) + 1))
        except ValueError:
            print(f"{RED}[!] Неверный формат диапазона! Пример: 20-100{RESET}")
            return
    else:
        try:
            ports = [int(p.strip()) for p in ports_input.split(",") if p.strip().isdigit()]
        except ValueError:
            print(f"{RED}[!] Ошибка парсинга портов!{RESET}")
            return

    print(f"\n[*] Сканирование {len(ports)} портов на {host}...")
    result = asyncio.run(scan_ports(host, ports, concurrency=200))
    
    print(f"\n{GREEN}{'—'*45}{RESET}")
    print(f"Результат для: {BOLD}{result['host']}{RESET}")
    print(f"Всего проверено: {result['scanned_total']} | Открыто: {len(result['open_ports'])}")
    print(f"{GREEN}{'—'*45}{RESET}")

    if result["open_ports"]:
        for p in result["open_ports"]:
            print(f"  [+] Порт {BOLD}{p:<6}{RESET} {GREEN}ОТКРЫТ (OPEN){RESET}")
    else:
        print(f"  {YELLOW}[-] Открытых портов не обнаружено или хост блокирует запросы.{RESET}")

def run_host_check():
    print(f"\n{BOLD}[+] ПРОВЕРКА ДОСТУПНОСТИ ХОСТА (PING / HOST CHECK){RESET}")
    host = input("-> Введите IP или домен для проверки: ").strip()
    if not host:
        print(f"{RED}[!] Хост не может быть пустым!{RESET}")
        return

    print(f"[*] Отправка ICMP пакетов к {host}...")
    res = asyncio.run(ping_host(host))

    if res["alive"]:
        lat = f"{res['latency_ms']} ms" if res["latency_ms"] is not None else "<1 ms"
        print(f"\n  {GREEN}[✓] Хост ДОСТУПЕН! Задержка: {BOLD}{lat}{RESET}")
    else:
        err = res.get("error", "Хост не отвечает (таймаут)")
        print(f"\n  {RED}[✗] Хост НЕДОСТУПЕН! ({err}){RESET}")

def run_network_status():
    print(f"\n{BOLD}[+] СЕТЕВЫЕ ИНТЕРФЕЙСЫ WINDOWS{RESET}")
    ext_ip = asyncio.run(get_external_ip())
    print(f"Внешний (Public) IP: {GREEN}{BOLD}{ext_ip}{RESET}\n")

    ifaces = get_network_interfaces()
    for iface in ifaces:
        status_color = GREEN if iface["is_up"] else RED
        status_text = "АКТИВЕН" if iface["is_up"] else "ОТКЛЮЧЕН"
        print(f"• Интерфейс: {BOLD}{iface['name']}{RESET} [{status_color}{status_text}{RESET}] (Скорость: {iface['speed_mbps']} Mbps)")
        if iface["mac"]:
            print(f"  MAC: {iface['mac']}")
        for v4 in iface["ipv4"]:
            print(f"  IPv4: {CYAN}{v4['address']}{RESET} (Маска: {v4['netmask']})")
        print()

def start_cli_loop(config: AppConfig):
    """Главный интерактивный цикл консоли."""
    while True:
        print_cli_header()
        print("  [1] Сканирование портов (Port Scanner)")
        print("  [2] Проверка доступности хоста (Ping)")
        print("  [3] Сетевой статус и адаптеры (Network Status)")
        print("  [4] Переключиться в режим Web UI")
        print("  [0] Выход из программы")
        
        choice = input(f"\n{BOLD}Выберите действие [0-4]: {RESET}").strip()
        
        if choice == "1":
            run_port_scanner()
        elif choice == "2":
            run_host_check()
        elif choice == "3":
            run_network_status()
        elif choice == "4":
            print(f"\n{YELLOW}[*] Переключение на веб-сервер...{RESET}")
            return "SWITCH_TO_WEB"
        elif choice == "0":
            print(f"\n{CYAN}Завершение работы NetHub. Пока!{RESET}")
            sys.exit(0)
        else:
            print(f"{RED}[!] Неверный выбор. Повторите ввод.{RESET}")

        input(f"\n{YELLOW}Нажмите Enter для возврата в меню...{RESET}")
