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
from core.i18n import t

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

def print_cli_header():
    print(f"\n{CYAN}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}      {t('cli_header')}{RESET}")
    print(f"{CYAN}{'='*60}{RESET}\n")

def run_ip_analysis():
    print(f"\n{BOLD}[+] {t('ip_analysis_title')}{RESET}")
    print(f"[*] {t('ip_probing')}")
    data = asyncio.run(analyze_ip_details())

    print(f"\n{GREEN}{'—'*45}{RESET}")
    print(f"{t('public_ip_label')} {BOLD}{data['ip']}{RESET}")
    print(f"ISP:          {data['isp']}")
    print(f"Location:     {data['city']}, {data['country']}")
    print(f"ASN:          {data['asn']}")
    print(f"{GREEN}{'—'*45}{RESET}")

    if data["is_white"]:
        print(f"\n  {GREEN}{t('verdict_white')}{RESET}")
        print(f"  {t('verdict_white_desc')}")
    elif data["is_cgnat"]:
        print(f"\n  {YELLOW}{t('verdict_cgnat')}{RESET}")
        print(f"  {t('verdict_cgnat_desc')}")
    else:
        print(f"\n  {CYAN}{t('verdict_standard')}{RESET}")

def run_upnp_forward():
    print(f"\n{BOLD}[+] {t('upnp_title')}{RESET}")
    port_input = input(t("upnp_port_prompt")).strip()
    if not port_input.isdigit():
        print(f"{RED}[ERR] Invalid port number!{RESET}")
        return

    port = int(port_input)
    proto = input(t("upnp_proto_prompt")).strip().upper() or "TCP"

    print(f"[*] {t('upnp_sending')} {port} ({proto})...")
    res = forward_port_upnp(port, proto, f"NetHub CLI {port}")

    if res["success"]:
        print(f"\n  {GREEN}[OK] {res['message']}{RESET}")
    else:
        print(f"\n  {RED}[FAIL] {res['error']}{RESET}")

def run_port_scanner():
    print(f"\n{BOLD}[+] {t('port_scan_title')}{RESET}")
    host = input(t("port_scan_host_prompt")).strip() or "127.0.0.1"

    ports_input = input(t("port_scan_ports_prompt")).strip()
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
    print(f"\n{BOLD}[+] {t('ping_title')}{RESET}")
    host = input(t("ping_host_prompt")).strip() or "8.8.8.8"

    print(f"[*] Dispatching ICMP packets to {host}...")
    res = asyncio.run(ping_host(host))

    if res["alive"]:
        lat = f"{res['latency_ms']} ms" if res["latency_ms"] is not None else "<1 ms"
        print(f"\n  {GREEN}[OK] Host {host} is REACHABLE | RTT: {BOLD}{lat}{RESET}")
    else:
        err = res.get("error", "Request timed out")
        print(f"\n  {RED}[FAIL] Host {host} is UNREACHABLE ({err}){RESET}")

def run_network_status():
    print(f"\n{BOLD}[+] {t('adapters_title')}{RESET}")
    ext_ip = asyncio.run(get_external_ip())
    print(f"{t('public_ip_label')} {GREEN}{BOLD}{ext_ip}{RESET}\n")

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
        print(f"  [1] {t('menu_1')}")
        print(f"  [2] {t('menu_2')}")
        print(f"  [3] {t('menu_3')}")
        print(f"  [4] {t('menu_4')}")
        print(f"  [5] {t('menu_5')}")
        print(f"  [6] {t('menu_6')}")
        print(f"  [0] {t('menu_0')}")
        
        choice = input(f"\n{BOLD}{t('select_action')}{RESET}").strip()
        
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
            print(f"\n{YELLOW}[*] Initializing Web UI Server...{RESET}")
            return "SWITCH_TO_WEB"
        elif choice == "0":
            print(f"\n{CYAN}{t('shutdown')}{RESET}")
            sys.exit(0)
        else:
            print(f"{RED}[ERR] Invalid selection.{RESET}")

        input(f"\n{YELLOW}{t('press_enter')}{RESET}")
