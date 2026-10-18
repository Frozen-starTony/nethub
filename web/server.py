from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
from typing import Optional, List
import urllib.parse
import httpx

from core.config import AppConfig, load_config
from core.network import get_external_ip, get_network_interfaces, scan_ports, ping_host
from core.launcher import launch_application
from web.templates import INDEX_HTML

LOGIN_PAGE_HTML = """<!DOCTYPE html>
<html lang="ru" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NetHub // Авторизация</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-200 min-h-screen flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-2xl text-center space-y-6">
        <div class="w-16 h-16 mx-auto rounded-2xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-3xl">
            ⚡
        </div>
        <div>
            <h2 class="text-2xl font-bold text-white tracking-tight">Net<span class="text-cyan-400">Hub</span></h2>
            <p class="text-sm text-slate-400 mt-1">Панель управления сетевой утилитой Windows 11</p>
        </div>
        <div class="p-4 rounded-xl bg-slate-800/60 border border-slate-700/50 text-xs text-slate-300">
            Доступ защищен авторизацией Google OAuth 2.0. Вход разрешен только доверенным аккаунтам из белого списка.
        </div>
        <a href="/auth/login" class="w-full py-3 px-4 bg-white hover:bg-slate-100 text-slate-900 font-semibold rounded-xl transition shadow-lg flex items-center justify-center space-x-3">
            <svg class="w-5 h-5" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.8-2.4 3.66v3.05h3.88c2.27-2.09 3.665-5.17 3.665-9.15z"/>
                <path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.25v3.15C3.26 21.36 7.34 24 12 24z"/>
                <path fill="#FBBC05" d="M5.28 14.27c-.25-.72-.38-1.49-.38-2.27s.13-1.55.38-2.27V6.58H1.25C.45 8.18 0 9.99 0 12s.45 3.82 1.25 5.42l4.03-3.15z"/>
                <path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.34 0 3.26 2.64 1.25 6.58l4.03 3.15c.95-2.83 3.6-4.98 6.72-4.98z"/>
            </svg>
            <span>Войти с помощью Google</span>
        </a>
    </div>
</body>
</html>
"""

def create_app(config: Optional[AppConfig] = None) -> FastAPI:
    if config is None:
        config = load_config()

    app = FastAPI(title="NetHub Web UI", version="1.0.0")

    # Сессии для хранения токенов/пользователя
    app.add_middleware(
        SessionMiddleware,
        secret_key=config.server.secret_key,
        max_age=86400 * 7 # 7 дней
    )

    # Проверка настроен ли Google OAuth
    is_oauth_configured = bool(
        config.google_oauth.client_id 
        and not config.google_oauth.client_id.startswith("YOUR_GOOGLE")
        and config.google_oauth.client_secret
        and not config.google_oauth.client_secret.startswith("YOUR_GOOGLE")
    )

    def check_auth(request: Request):
        """Проверка авторизации: если OAuth не настроен - работает в dev_mode."""
        if not is_oauth_configured:
            return "developer_admin"
        
        user = request.session.get("user")
        if not user:
            raise HTTPException(status_code=401, detail="Требуется авторизация через Google")
        return user

    # --- МАРШРУТЫ АВТОРИЗАЦИИ (GOOGLE OAUTH) ---

    @app.get("/auth/status")
    async def auth_status(request: Request):
        user = request.session.get("user")
        return {
            "authenticated": bool(user) or not is_oauth_configured,
            "user": user or ("admin (dev_mode)" if not is_oauth_configured else None),
            "dev_mode": not is_oauth_configured,
            "allowed_emails": config.google_oauth.allowed_emails
        }

    @app.get("/auth/login")
    async def auth_login():
        if not is_oauth_configured:
            return RedirectResponse(url="/")

        # Формирование URL для авторизации Google OAuth 2.0
        params = {
            "client_id": config.google_oauth.client_id,
            "redirect_uri": config.google_oauth.redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "online",
            "prompt": "select_account"
        }
        google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
        return RedirectResponse(url=google_auth_url)

    @app.get("/auth/callback")
    async def auth_callback(request: Request, code: Optional[str] = None, error: Optional[str] = None):
        if error or not code:
            return HTMLResponse(f"<h3>Ошибка авторизации Google: {error or 'Код не получен'}</h3><a href='/'>Назад</a>", status_code=400)

        # Обмен code на access_token через httpx
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "code": code,
            "client_id": config.google_oauth.client_id,
            "client_secret": config.google_oauth.client_secret,
            "redirect_uri": config.google_oauth.redirect_uri,
            "grant_type": "authorization_code"
        }

        async with httpx.AsyncClient() as client:
            token_resp = await client.post(token_url, data=token_data)
            if token_resp.status_code != 200:
                return HTMLResponse(f"<h3>Ошибка получения токена Google: {token_resp.text}</h3>", status_code=400)
            
            tokens = token_resp.json()
            access_token = tokens.get("access_token")

            # Запрос профиля пользователя
            userinfo_resp = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            if userinfo_resp.status_code != 200:
                return HTMLResponse("<h3>Не удалось получить профиль пользователя Google</h3>", status_code=400)
            
            profile = userinfo_resp.json()
            email = profile.get("email", "").lower().strip()

        # Проверка белого списка (allowed_emails)
        allowed = [e.lower().strip() for e in config.google_oauth.allowed_emails]
        if allowed and email not in allowed:
            return HTMLResponse(
                f"""<div style='font-family: sans-serif; padding: 40px; text-align: center;'>
                    <h2 style='color: #ef4444;'>[403] Доступ запрещен</h2>
                    <p>Email <b>{email}</b> отсутствует в списке доверенных адресов (config.json).</p>
                    <a href='/auth/login'>Попробовать другой аккаунт</a>
                </div>""",
                status_code=403
            )

        # Сохранение в сессию
        request.session["user"] = email
        return RedirectResponse(url="/")

    @app.get("/auth/logout")
    async def auth_logout(request: Request):
        request.session.clear()
        return RedirectResponse(url="/")

    # --- СТРАНИЦЫ ИНТЕРФЕЙСА ---

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        if is_oauth_configured and not request.session.get("user"):
            return HTMLResponse(LOGIN_PAGE_HTML)
        return HTMLResponse(INDEX_HTML)

    # --- API ЭНДПОИНТЫ ---

    @app.get("/api/ip")
    async def api_ip(_=Depends(check_auth)):
        ip = await get_external_ip()
        return {"ip": ip}

    @app.get("/api/interfaces")
    async def api_interfaces(_=Depends(check_auth)):
        return get_network_interfaces()

    class PingRequest(BaseModel):
        host: str

    @app.post("/api/ping")
    async def api_ping(req: PingRequest, _=Depends(check_auth)):
        return await ping_host(req.host)

    class ScanRequest(BaseModel):
        host: str
        ports_str: str

    @app.post("/api/scan")
    async def api_scan(req: ScanRequest, _=Depends(check_auth)):
        host = req.host.strip()
        ports_input = req.ports_str.strip()

        ports = []
        if "-" in ports_input:
            try:
                s, e = map(int, ports_input.split("-"))
                ports = list(range(max(1, s), min(65535, e) + 1))
            except Exception:
                return {"error": "Неверный диапазон портов (например, 20-100)"}
        else:
            try:
                ports = [int(p.strip()) for p in ports_input.split(",") if p.strip().isdigit()]
            except Exception:
                return {"error": "Неверный список портов (например, 80,443,8080)"}

        if not ports:
            return {"error": "Не указаны порты для сканирования"}

        # Ограничиваем срез за раз во избежание перегрузки
        ports = ports[:5000]
        return await scan_ports(host, ports, concurrency=200)

    @app.get("/api/apps")
    async def api_apps(_=Depends(check_auth)):
        return config.apps

    @app.post("/api/launch/{app_id}")
    async def api_launch(app_id: str, _=Depends(check_auth)):
        res = launch_application(app_id, config)
        return res

    return app
