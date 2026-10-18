import locale
import sys
from typing import Dict, Any, Optional

def get_system_lang() -> str:
    """Определение языка операционной системы (ru или en)."""
    try:
        if sys.platform == "win32":
            import ctypes
            lang_id = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            # 0x19 is LANG_RUSSIAN (0x0419 = Russian, 0x0819 = Russian Moldavia, etc.)
            if (lang_id & 0xFF) == 0x19:
                return "ru"
            # 0x22 is Ukrainian, 0x23 is Belarusian - treat as CIS/ru or fallback to ru if desired
            if (lang_id & 0xFF) in (0x22, 0x23):
                return "ru"
        
        loc = locale.getdefaultlocale()[0]
        if loc and (loc.lower().startswith("ru") or loc.lower().startswith("be") or loc.lower().startswith("uk")):
            return "ru"
    except Exception:
        pass
    return "en"

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "ru": {
        "banner_subtitle": "Анализ Белого IP, UPnP авто-проброс портов и селф-хостинг",
        "probing_gateway": "Опрос глобального сетевого шлюза...",
        "public_ip_label": "Публичный IP-адрес:",
        "select_mode": "Выберите режим работы программы:",
        "mode_cli": "Интерактивный терминал (CLI режим)",
        "mode_web": "Локальная веб-панель управления (Web UI режим)",
        "mode_exit": "Выход",
        "action_prompt": "Ваш выбор [1/2/0]: ",
        "invalid_choice": "Неверная команда. Введите 1, 2 или 0.",
        "web_running": "Веб-панель запущена на",
        "web_ctrl_c": "Нажмите Ctrl+C в этом окне для остановки сервера.",
        "cli_header": "NETHUB // АНАЛИЗАТОР БЕЛОГО IP И СЕТЕВЫЕ ОПЕРАЦИИ (CLI)",
        "menu_1": "Анализ: Белый или Серый IP (White vs CGNAT)",
        "menu_2": "UPnP: Авто-проброс портов (Minecraft, RDP, Web)",
        "menu_3": "Сканирование портов (Port Scanner)",
        "menu_4": "Проверка доступности хоста (Ping)",
        "menu_5": "Сетевые интерфейсы и адаптеры",
        "menu_6": "Запустить Веб-панель управления",
        "menu_0": "Выход",
        "select_action": "Выберите действие [0-6]: ",
        "press_enter": "Нажмите Enter для возврата в главное меню...",
        "shutdown": "Завершение работы NetHub. Пока!",
        "ip_analysis_title": "АНАЛИЗАТОР: БЕЛЫЙ ИЛИ СЕРЫЙ IP",
        "ip_probing": "Опрос глобальных маршрутизаторов и провайдера...",
        "verdict_white": "[ВЕРДИКТ] БЕЛЫЙ (ПУБЛИЧНЫЙ) IP!",
        "verdict_white_desc": "Ваш ПК напрямую доступен из Интернета. Вы можете хостить серверы\n(Minecraft, CS2, Palworld) и использовать RDP. Достаточно открыть порт через UPnP.",
        "verdict_cgnat": "[ВЕРДИКТ] СЕРЫЙ IP (CGNAT / NAT ПРОВАЙДЕРА)!",
        "verdict_cgnat_desc": "Провайдер заблокировал прямой входящий трафик.\nРешение: подключите услугу 'Белый/Статический IP' у провайдера\nили бесплатно используйте Playit.gg / Cloudflare Tunnels.",
        "verdict_standard": "[ВЕРДИКТ] Стандартный публичный маршрут.",
        "upnp_title": "UPNP АВТО-ПРОБРОС ПОРТОВ (БЕЗ ВХОДА В РОУТЕР)",
        "upnp_port_prompt": "-> Укажите порт для открытия (например, 25565 для Minecraft, 8080 для Web): ",
        "upnp_proto_prompt": "-> Протокол [TCP/UDP, по умолчанию TCP]: ",
        "upnp_sending": "Отправка UPnP команды на роутер для порта",
        "ping_title": "ПРОВЕРКА ДОСТУПНОСТИ ХОСТА (ICMP PING)",
        "ping_host_prompt": "-> Введите целевой хост / IP (по умолчанию 8.8.8.8): ",
        "port_scan_title": "СКАНИРОВАНИЕ TCP ПОРТОВ",
        "port_scan_host_prompt": "-> Целевой хост (IP / домен, по умолчанию 127.0.0.1): ",
        "port_scan_ports_prompt": "-> Диапазон портов или список (например, 1-1024 или 80,443): ",
        "adapters_title": "СЕТЕВЫЕ ИНТЕРФЕЙСЫ И АДАПТЕРЫ WINDOWS"
    },
    "en": {
        "banner_subtitle": "White IP Inspector, UPnP Port Forwarder & Self-Hosting Hub",
        "probing_gateway": "Probing global network gateway...",
        "public_ip_label": "Public IP Address:",
        "select_mode": "Select Execution Mode:",
        "mode_cli": "Interactive Terminal (CLI Mode)",
        "mode_web": "Self-Hosted Control Plane (Web UI Mode)",
        "mode_exit": "Exit",
        "action_prompt": "Action [1/2/0]: ",
        "invalid_choice": "Invalid selection. Expected 1, 2 or 0.",
        "web_running": "Web control panel running on",
        "web_ctrl_c": "Press Ctrl+C in this console to terminate server.",
        "cli_header": "NETHUB // WHITE IP & NETWORK OPERATIONS (CLI)",
        "menu_1": "Analyze: White vs Gray IP (Public vs CGNAT)",
        "menu_2": "UPnP: Automatic Port Forwarding (Minecraft, RDP, Web)",
        "menu_3": "TCP Port Inspector",
        "menu_4": "Host Ping Diagnostic",
        "menu_5": "Network Adapters & IP Status",
        "menu_6": "Launch Web UI Control Plane",
        "menu_0": "Exit",
        "select_action": "Select action [0-6]: ",
        "press_enter": "Press Enter to return to main menu...",
        "shutdown": "NetHub shutdown complete.",
        "ip_analysis_title": "WHITE VS GRAY IP INSPECTOR",
        "ip_probing": "Probing global routing tables and ISP data...",
        "verdict_white": "[VERDICT] WHITE (PUBLIC) IP DETECTED!",
        "verdict_white_desc": "Your PC is directly routable from the Internet. You can host servers\n(Minecraft, CS2, Palworld) and RDP. Forward ports using UPnP.",
        "verdict_cgnat": "[VERDICT] GRAY IP (CGNAT / CARRIER-GRADE NAT) DETECTED!",
        "verdict_cgnat_desc": "Your ISP blocks direct inbound traffic.\nSolution: Request a Static/Public IP from your ISP or use Playit.gg / Cloudflare Tunnels.",
        "verdict_standard": "[VERDICT] Standard routable public path.",
        "upnp_title": "UPNP AUTOMATIC PORT FORWARDING (NO ROUTER LOGIN REQUIRED)",
        "upnp_port_prompt": "-> Specify port to forward (e.g. 25565 for Minecraft, 8080 for Web): ",
        "upnp_proto_prompt": "-> Protocol [TCP/UDP, default TCP]: ",
        "upnp_sending": "Sending UPnP request to home gateway for port",
        "ping_title": "HOST REACHABILITY CHECK (ICMP PING)",
        "ping_host_prompt": "-> Target host / IP (default 8.8.8.8): ",
        "port_scan_title": "TCP PORT INSPECTOR",
        "port_scan_host_prompt": "-> Target host (IP / domain, default 127.0.0.1): ",
        "port_scan_ports_prompt": "-> Port range or list (e.g. 1-1024 or 80,443): ",
        "adapters_title": "WINDOWS NETWORK ADAPTERS & INTERFACES"
    }
}

def t(key: str, lang: Optional[str] = None) -> str:
    """Получение локализованной строки."""
    if not lang:
        lang = get_system_lang()
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
