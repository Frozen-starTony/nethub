import asyncio
import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import load_config
from core.network import get_network_interfaces, scan_port, ping_host
from core.launcher import launch_application

def test_config():
    cfg = load_config()
    assert cfg.server.port == 8080, "Default port should be 8080"
    assert len(cfg.apps) > 0, "Default apps should be registered"
    print("[PASS] test_config")

def test_interfaces():
    ifaces = get_network_interfaces()
    assert isinstance(ifaces, list), "Interfaces should be a list"
    assert len(ifaces) > 0, "At least one interface should exist"
    print(f"[PASS] test_interfaces: found {len(ifaces)} interfaces")

def test_network():
    # Test localhost ping
    ping_res = asyncio.run(ping_host("127.0.0.1"))
    assert ping_res["alive"] is True, "Localhost ping should succeed"
    print(f"[PASS] test_network_ping: {ping_res['latency_ms']} ms")

    # Test port scan on an unlikely port
    open_status = asyncio.run(scan_port("127.0.0.1", 65432, timeout=0.2))
    assert open_status is False, "Port 65432 should be closed"
    print("[PASS] test_network_port_scan")

def test_launcher():
    cfg = load_config()
    # Test non-existing app
    res = launch_application("non_existent_app_xyz", cfg)
    assert res["success"] is False, "Unknown app should fail safely"
    print("[PASS] test_launcher_safety_validation")

if __name__ == "__main__":
    test_config()
    test_interfaces()
    test_network()
    test_launcher()
    print("\n[OK] All core test suites passed successfully.")

