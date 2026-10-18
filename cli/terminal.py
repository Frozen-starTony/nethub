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
    print(f"{BOLD}{CYAN}             NETHUB // INTERACTIVE TERMINAL (CLI){RESET}")
    print(f"{CYAN}{'='*60}{RESET}\n")

def run_port_scanner():
    print(f"\n{BOLD}[+] TCP PORT INSPECTOR{RESET}")
    host = input("-> Target Host (IP / Domain, default 127.0.0.1): ").strip() or "127.0.0.1"

    ports_input = input("-> Port Range or Comma List (e.g. 1-1024 or 80,443): ").strip()
    if not ports_input:
        ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 1433, 3306, 3389, 5432, 8000, 8080]
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
        print("  [1] TCP Port Inspector")
        print("  [2] Host Ping Diagnostic")
        print("  [3] Network Adapters & IP Status")
        print("  [4] Launch Web UI Control Plane")
        print("  [0] Exit")
        
        choice = input(f"\n{BOLD}Select action [0-4]: {RESET}").strip()
        
        if choice == "1":
            run_port_scanner()
        elif choice == "2":
            run_host_check()
        elif choice == "3":
            run_network_status()
        elif choice == "4":
            print(f"\n{YELLOW}[*] Initializing Web UI Server...{RESET}")
            return "SWITCH_TO_WEB"
        elif choice == "0":
            print(f"\n{CYAN}NetHub shutdown complete.{RESET}")
            sys.exit(0)
        else:
            print(f"{RED}[ERR] Invalid input selection.{RESET}")

        input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")
