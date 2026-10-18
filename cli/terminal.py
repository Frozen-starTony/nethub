import asyncio
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from core.network import scan_ports, ping_host, get_network_interfaces, get_external_ip, analyze_ip_details, check_external_port
from core.upnp import forward_port_upnp
from core.config import AppConfig

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

def print_cli_header():
    print(f"\n{CYAN}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}      NETHUB // WHITE IP & NETWORK OPERATIONS (CLI){RESET}")
    print(f"{CYAN}{'='*60}{RESET}\n")

def run_ip_analysis():
    print(f"\n{BOLD}[+] АНАЛИЗАТОР: БЕЛЫЙ ИЛИ СЕРЫЙ IP{RESET}")
    print("[*] Опрос глобальных маршрутизаторов и провайдера...")
    data = asyncio.run(analyze_ip_details())

    print(f"\n{GREEN}{'—'*45}{RESET}")
    print(f"Публичный IP: {BOLD}{data['ip']}{RESET}")
    print(f"Провайдер:    {data['isp']}")
    print(f"Локация:      {data['city']}, {data['country']}")
    print(f"AS:           {data['asn']}")
    print(f"{GREEN}{'—'*45}{RESET}")

    if data["is_white"]:
        print(f"\n  {GREEN}[ВЕРДИКТ] БЕЛЫЙ (ПУБЛИЧНЫЙ) IP!{RESET}")
        print("  Ваш ПК напрямую доступен из Интернета. Вы можете хостить серверы")
        print("  (Minecraft, CS2, Palworld) и использовать RDP. Достаточно открыть порт через UPnP.")
    elif data["is_cgnat"]:
        print(f"\n  {YELLOW}[ВЕРДИКТ] СЕРЫЙ IP (CGNAT / NAT ПРОВАЙДЕРА)!{RESET}")
        print("  Провайдер заблокировал прямой входящий трафик.")
        print("  Решение: подключите услугу 'Белый/Статический IP' у провайдера")
        print("  или бесплатно используйте Playit.gg / Cloudflare Tunnels.")
    else:
        print(f"\n  {CYAN}[ВЕРДИКТ] Стандартный публичный маршрут.{RESET}")

def run_upnp_forward():
    print(f"\n{BOLD}[+] UPNP АВТО-ПРОБРОС ПОРТОВ (БЕЗ ВХОДА В РОУТЕР){RESET}")
    port_input = input("-> Укажите порт для открытия (например, 25565 для Minecraft, 8080 для Web): ").strip()
    if not port_input.isdigit():
        print(f"{RED}[ERR] Неверный номер порта!{RESET}")
        return

    port = int(port_input)
    proto = input("-> Протокол [TCP/UDP, по умолчанию TCP]: ").strip().upper() or "TCP"

    print(f"[*] Отправка UPnP команды на роутер для порта {port} ({proto})...")
    res = forward_port_upnp(port, proto, f"NetHub CLI {port}")

    if res["success"]:
        print(f"\n  {GREEN}[OK] {res['message']}{RESET}")
    else:
        print(f"\n  {RED}[FAIL] {res['error']}{RESET}")

def run_port_scanner():
    print(f"\n{BOLD}[+] TCP PORT INSPECTOR{RESET}")
    host = input("-> Target Host (IP / Domain, default 127.0.0.1): ").strip() or "127.0.0.1"

    ports_input = input("-> Port Range or Comma List (e.g. 1-1024 or 80,443): ").strip()
    if not ports_input:
        ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 1433, 3306, 3389, 5432, 8000, 8080, 25565]
        print(f"{YELLOW}[INFO] Using top standard service ports ({len(ports)} targets){RESET}")
    elif "-" in ports_input:
        try:
            start_p, end_p = map(int, ports_input.split("-"))
            ports = list(range(max(1, start_p), min(65535, end_p) + 1))
        except ValueError:
            print(f"{RED}[ERR] Invalid range specification. Expected start-end (e.g. 20-100){RESET}")
            return
    else:
        try:
            ports = [int(p.strip()) for p in ports_input.split(",") if p.strip().isdigit()]
        except ValueError:
            print(f"{RED}[ERR] Port parsing failed{RESET}")
            return

    print(f"\n[*] Probing {len(ports)} ports on {host}...")
    result = asyncio.run(scan_ports(host, ports, concurrency=200))
    
    print(f"\n{GREEN}{'—'*45}{RESET}")
    print(f"Target: {BOLD}{result['host']}{RESET}")
    print(f"Scanned: {result['scanned_total']} | Open: {len(result['open_ports'])}")
    print(f"{GREEN}{'—'*45}{RESET}")

    if result["open_ports"]:
        for p in result["open_ports"]:
            print(f"  [+] Port {BOLD}{p:<6}{RESET} {GREEN}OPEN{RESET}")
    else:
        print(f"  {YELLOW}[-] No responsive TCP ports detected.{RESET}")

def run_host_check():
    print(f"\n{BOLD}[+] HOST ICMP PING DIAGNOSTIC{RESET}")
    host = input("-> Target Host / IP (default 8.8.8.8): ").strip() or "8.8.8.8"

    print(f"[*] Dispatching ICMP packets to {host}...")
    res = asyncio.run(ping_host(host))

    if res["alive"]:
        lat = f"{res['latency_ms']} ms" if res["latency_ms"] is not None else "<1 ms"
        print(f"\n  {GREEN}[OK] Host {host} is REACHABLE | RTT: {BOLD}{lat}{RESET}")
    else:
        err = res.get("error", "Request timed out")
        print(f"\n  {RED}[FAIL] Host {host} is UNREACHABLE ({err}){RESET}")

def run_network_status():
    print(f"\n{BOLD}[+] NETWORK INTERFACES & ADAPTERS{RESET}")
    ext_ip = asyncio.run(get_external_ip())
    print(f"Public Gateway IP: {GREEN}{BOLD}{ext_ip}{RESET}\n")

    ifaces = get_network_interfaces()
    for iface in ifaces:
        status_color = GREEN if iface["is_up"] else RED
        status_text = "UP" if iface["is_up"] else "DOWN"
        print(f"  [+] Adapter: {BOLD}{iface['name']}{RESET} [{status_color}{status_text}{RESET}] ({iface['speed_mbps']} Mbps)")
        if iface["mac"]:
            print(f"      MAC:  {iface['mac']}")
        for v4 in iface["ipv4"]:
            print(f"      IPv4: {CYAN}{v4['address']}{RESET} (Netmask: {v4['netmask']})")
        print()

def start_cli_loop(config: AppConfig):
    while True:
        print_cli_header()
        print("  [1] Анализ: Белый или Серый IP (White vs CGNAT)")
        print("  [2] UPnP: Авто-проброс портов (Minecraft, RDP, Web)")
        print("  [3] Сканирование портов (Port Scanner)")
        print("  [4] Проверка доступности хоста (Ping)")
        print("  [5] Сетевые интерфейсы и адаптеры")
        print("  [6] Запустить Веб-панель управления")
        print("  [0] Выход")
        
        choice = input(f"\n{BOLD}Выберите действие [0-6]: {RESET}").strip()
        
        if choice == "1":
            run_ip_analysis()
        elif choice == "2":
            run_upnp_forward()
        elif choice == "3":
            run_port_scanner()
        elif choice == "4":
            run_host_check()
        elif choice == "5":
            run_network_status()
        elif choice == "6":
            print(f"\n{YELLOW}[*] Запуск веб-сервера NetHub...{RESET}")
            return "SWITCH_TO_WEB"
        elif choice == "0":
            print(f"\n{CYAN}Завершение работы NetHub.{RESET}")
            sys.exit(0)
        else:
            print(f"{RED}[ERR] Неверный выбор.{RESET}")

        input(f"\n{YELLOW}Нажмите Enter для возврата в главное меню...{RESET}")
