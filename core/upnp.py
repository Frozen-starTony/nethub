import socket
import re
import urllib.parse
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional
import httpx

SSDP_ADDR = "239.255.255.250"
SSDP_PORT = 1900
SSDP_MX = 2

SSDP_MSG = (
    "M-SEARCH * HTTP/1.1\r\n"
    f"HOST: {SSDP_ADDR}:{SSDP_PORT}\r\n"
    'MAN: "ssdp:discover"\r\n'
    f"MX: {SSDP_MX}\r\n"
    "ST: urn:schemas-upnp-org:service:WANIPConnection:1\r\n\r\n"
)

SSDP_MSG_PPP = (
    "M-SEARCH * HTTP/1.1\r\n"
    f"HOST: {SSDP_ADDR}:{SSDP_PORT}\r\n"
    'MAN: "ssdp:discover"\r\n'
    f"MX: {SSDP_MX}\r\n"
    "ST: urn:schemas-upnp-org:service:WANPPPConnection:1\r\n\r\n"
)

def get_local_ip_for_target(target="8.8.8.8") -> str:
    """Получение локального IP-адреса компьютера в локальной сети."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((target, 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def discover_upnp_router(timeout=2.0) -> Optional[Dict[str, str]]:
    """Поиск домашнего роутера через протокол SSDP (UPnP)."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.settimeout(timeout)
    
    locations = []
    for msg in (SSDP_MSG, SSDP_MSG_PPP):
        try:
            sock.sendto(msg.encode("utf-8"), (SSDP_ADDR, SSDP_PORT))
            while True:
                data, _ = sock.recvfrom(2048)
                resp = data.decode("utf-8", errors="ignore")
                match = re.search(r"LOCATION:\s*(http://[^\r\n]+)", resp, re.IGNORECASE)
                if match:
                    locations.append(match.group(1).strip())
                    break
        except Exception:
            pass

    sock.close()
    if not locations:
        return None

    # Парсим XML роутера и ищем controlURL для WANIPConnection или WANPPPConnection
    for loc in locations:
        try:
            with httpx.Client(timeout=2.5) as client:
                r = client.get(loc)
                if r.status_code != 200:
                    continue
                
                # Ищем controlURL в XML
                root = ET.fromstring(r.text)
                for service in root.iter():
                    if "serviceType" in service.tag and ("WANIPConnection" in service.text or "WANPPPConnection" in service.text):
                        parent = service.find("..")
                        service_type = service.text
                        control_url_el = None
                        # Ищем controlURL в этом же блоке service
                        for sibling in parent.iter():
                            if "controlURL" in sibling.tag:
                                control_url_el = sibling.text
                                break
                        
                        if control_url_el:
                            full_control_url = urllib.parse.urljoin(loc, control_url_el)
                            return {
                                "location": loc,
                                "service_type": service_type,
                                "control_url": full_control_url
                            }
        except Exception:
            continue

    return None

def forward_port_upnp(port: int, protocol: str = "TCP", description: str = "NetHub AutoPort") -> Dict[str, Any]:
    """Автоматический проброс порта на роутере через UPnP без входа в 192.168.1.1."""
    local_ip = get_local_ip_for_target()
    router_info = discover_upnp_router()
    
    if not router_info:
        return {
            "success": False,
            "error": "Роутер не ответил на UPnP запрос (возможно, UPnP отключен в настройках роутера или сеть изолирована)."
        }

    soap_body = f"""<?xml version="1.0"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
<s:Body>
<u:AddPortMapping xmlns:u="{router_info['service_type']}">
<NewRemoteHost></NewRemoteHost>
<NewExternalPort>{port}</NewExternalPort>
<NewProtocol>{protocol.upper()}</NewProtocol>
<NewInternalPort>{port}</NewInternalPort>
<NewInternalClient>{local_ip}</NewInternalClient>
<NewEnabled>1</NewEnabled>
<NewPortMappingDescription>{description}</NewPortMappingDescription>
<NewLeaseDuration>0</NewLeaseDuration>
</u:AddPortMapping>
</s:Body>
</s:Envelope>"""

    headers = {
        "Content-Type": 'text/xml; charset="utf-8"',
        "SOAPAction": f'"{router_info["service_type"]}#AddPortMapping"'
    }

    try:
        with httpx.Client(timeout=3.5) as client:
            resp = client.post(router_info["control_url"], content=soap_body, headers=headers)
            if resp.status_code == 200:
                return {
                    "success": True,
                    "port": port,
                    "protocol": protocol,
                    "local_ip": local_ip,
                    "message": f"Порт {port} ({protocol}) успешно открыт на роутере для вашего ПК ({local_ip})!"
                }
            else:
                return {
                    "success": False,
                    "port": port,
                    "error": f"Роутер отклонил UPnP команду: HTTP {resp.status_code} ({resp.text[:150]})"
                }
    except Exception as e:
        return {
            "success": False,
            "port": port,
            "error": f"Ошибка связи с UPnP службой роутера: {str(e)}"
        }
