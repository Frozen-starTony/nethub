import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from web.server import create_app
from core.config import load_config

def test_web_routes():
    cfg = load_config()
    app = create_app(cfg)
    client = TestClient(app)

    # 1. Main UI
    resp = client.get("/")
    assert resp.status_code == 200, "Dashboard should be served"
    assert "NetHub" in resp.text

    # 2. Auth status
    auth_resp = client.get("/auth/status")
    assert auth_resp.status_code == 200
    data = auth_resp.json()
    assert "authenticated" in data
    print(f"[PASS] auth_status_endpoint: {data['user']}")

    # 3. Interfaces API
    ifaces_resp = client.get("/api/interfaces")
    assert ifaces_resp.status_code == 200
    ifaces = ifaces_resp.json()
    assert isinstance(ifaces, list)
    print(f"[PASS] interfaces_endpoint: {len(ifaces)} interfaces found")

    # 4. Apps API
    apps_resp = client.get("/api/apps")
    assert apps_resp.status_code == 200
    apps = apps_resp.json()
    assert len(apps) > 0
    print(f"[PASS] apps_endpoint: {len(apps)} apps registered")

    # 5. Ping API
    ping_resp = client.post("/api/ping", json={"host": "127.0.0.1"})
    assert ping_resp.status_code == 200
    ping_data = ping_resp.json()
    assert ping_data["alive"] is True
    print(f"[PASS] ping_endpoint: latency {ping_data['latency_ms']} ms")

    print("\n[OK] All Web API test suites passed successfully.")


if __name__ == "__main__":
    test_web_routes()
