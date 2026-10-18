import asyncio
import socket
import subprocess
import re
from typing import List, Dict, Any, Optional
import httpx
import psutil

IP_SERVICES = [
    "https://api.ipify.org?format=json",
    "https://api64.ipify.org?format=json",
    "https://httpbin.org/ip"
]

async def get_external_ip() -> str:
    """Определение внешнего IP-адреса через несколько внешних сервисов с fallback."""
    async with httpx.AsyncClient(timeout=4.0) as client:
        for url in IP_SERVICES:
            try:
                resp = await client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    ip = data.get("ip") or data.get("origin", "").split(",")[0].strip()
                    if ip:
                        return ip
            except Exception:
                continue

    # Запасной вариант с обычным текстовым сервисом
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get("https://icanhazip.com")
            if resp.status_code == 200 and resp.text.strip():
                return resp.text.strip()
    except Exception:
        pass

    return "Не удалось определить (Offline / Firewall)"

def get_network_interfaces() -> List[Dict[str, Any]]:
    """Получение подробной информации о сетевых интерфейсах Windows."""
    interfaces = []
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    for iface_name, addr_list in addrs.items():
        iface_stat = stats.get(iface_name)
        is_up = iface_stat.isup if iface_stat else False
        speed = iface_stat.speed if iface_stat else 0

        ipv4 = []
        ipv6 = []
        mac = None

        for addr in addr_list:
            if addr.family == socket.AF_INET:
                ipv4.append({
                    "address": addr.address,
                    "netmask": addr.netmask,
                    "broadcast": addr.broadcast
                })
            elif addr.family == socket.AF_INET6:
                ipv6.append(addr.address)
            elif hasattr(psutil, "AF_LINK") and addr.family == psutil.AF_LINK:
                mac = addr.address

        interfaces.append({
            "name": iface_name,
            "is_up": is_up,
            "speed_mbps": speed,
            "mac": mac,
            "ipv4": ipv4,
            "ipv6": ipv6
        })

    return interfaces

async def scan_port(host: str, port: int, timeout: float = 1.0) -> bool:
    """Асинхронная проверка открытости одного TCP порта."""
    try:
        conn = asyncio.open_connection(host, port)
        reader, writer = await asyncio.wait_for(conn, timeout=timeout)
        writer.close()
        await writer.wait_closed()
        return True
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return False

async def scan_ports(host: str, ports: List[int], concurrency: int = 150, timeout: float = 1.2) -> Dict[str, Any]:
    """Быстрое асинхронное сканирование диапазона портов с ограничением параллельности."""
    sem = asyncio.Semaphore(concurrency)
    results = {}

    async def _scan_worker(p: int):
        async with sem:
            is_open = await scan_port(host, p, timeout=timeout)
            if is_open:
                results[p] = "open"

    tasks = [_scan_worker(p) for p in ports]
    await asyncio.gather(*tasks)

    # Сортируем список открытых портов
    open_ports = sorted(list(results.keys()))
    return {
        "host": host,
        "scanned_total": len(ports),
        "open_ports": open_ports,
        "open_count": len(open_ports)
    }

async def ping_host(host: str, timeout_ms: int = 2000) -> Dict[str, Any]:
    """Проверка доступности хоста средствами ОС Windows (ping.exe)."""
    # Валидация хоста во избежание command injection
    clean_host = host.strip()
    if not re.match(r"^[a-zA-Z0-9.-]+$", clean_host):
        return {"host": host, "alive": False, "error": "Недопустимый формат адреса"}

    cmd = ["ping", "-n", "2", "-w", str(timeout_ms), clean_host]
    
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate()
        output = stdout.decode("cp866", errors="replace")

        # Парсинг ответа Windows Ping
        # Проверяем наличие 'TTL=' или 'время=' / 'time='
        alive = ("TTL=" in output or "ttl=" in output)
        
        # Поиск средней задержки
        time_match = re.search(r"(?:Среднее|Average)\s*=\s*(\d+)\s*(?:мс|ms)", output)
        latency_ms = int(time_match.group(1)) if time_match else None
        
        if alive and latency_ms is None:
            single_match = re.search(r"(?:время|time)[=<](\d+)\s*(?:мс|ms)", output)
            if single_match:
                latency_ms = int(single_match.group(1))

        return {
            "host": clean_host,
            "alive": alive,
            "latency_ms": latency_ms if alive else None,
            "raw_output": output.strip()
        }
    except Exception as e:
        return {
            "host": clean_host,
            "alive": False,
            "error": str(e)
        }

async def analyze_ip_details(ip: Optional[str] = None) -> Dict[str, Any]:
    """Глубокий анализ: Белый (Public) или Серый (CGNAT) IP-адрес, провайдер и геолокация."""
    if not ip or "Не удалось" in ip or "Unreachable" in ip:
        ip = await get_external_ip()

    is_cgnat = False
    is_private = False
    ip_type = "UNKNOWN"

    # Проверка диапазонов
    if ip.startswith("100."):
        # Проверяем 100.64.0.0/10 (CGNAT)
        parts = [int(p) for p in ip.split(".") if p.isdigit()]
        if len(parts) == 4 and parts[0] == 100 and (64 <= parts[1] <= 127):
            is_cgnat = True
            ip_type = "GRAY_CGNAT"

    if (ip.startswith("10.") or 
        ip.startswith("192.168.") or 
        (ip.startswith("172.") and len(ip.split(".")) == 4 and 16 <= int(ip.split(".")[1]) <= 31)):
        is_private = True
        ip_type = "PRIVATE"

    if not is_cgnat and not is_private and "." in ip:
        ip_type = "WHITE_PUBLIC"

    # Запрос данных о провайдере
    geo_data = {}
    try:
        async with httpx.AsyncClient(timeout=3.5) as client:
            resp = await client.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,city,isp,org,as,query")
            if resp.status_code == 200:
                geo_data = resp.json()
    except Exception:
        pass

    isp = geo_data.get("isp") or geo_data.get("org") or "Не определен"
    country = geo_data.get("country") or "Не определена"
    city = geo_data.get("city") or "Не определен"
    asn = geo_data.get("as") or "N/A"

    return {
        "ip": ip,
        "ip_type": ip_type,
        "is_white": (ip_type == "WHITE_PUBLIC"),
        "is_cgnat": is_cgnat,
        "isp": isp,
        "country": country,
        "city": city,
        "asn": asn
    }

async def check_external_port(port: int) -> Dict[str, Any]:
    """Проверка доступности порта из внешней сети Интернет (открыт ли порт наружу)."""
    try:
        async with httpx.AsyncClient(timeout=4.0) as client:
            # Используем публичный сервис проверки портов
            resp = await client.get(f"https://portcheck.transmissionbt.com/{port}")
            if resp.status_code == 200:
                is_open = (resp.text.strip() == "1")
                return {
                    "port": port,
                    "is_open": is_open,
                    "status": "OPEN" if is_open else "CLOSED_OR_FILTERED",
                    "message": "Порт доступен из Интернета" if is_open else "Порт закрыт или блокируется провайдером/брандмауэром"
                }
    except Exception:
        pass

    return {
        "port": port,
        "is_open": False,
        "status": "UNKNOWN",
        "message": "Внешний сервис проверки недоступен"
    }

