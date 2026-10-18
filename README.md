# ⚡ NetHub — Windows 11 Hybrid Network Toolkit

**NetHub** — гибридная сетевая утилита для Windows 11, совмещающая интерактивный консольный терминал (**CLI**) и локальную веб-панель управления (**Web UI**) с поддержкой авторизации через **Google OAuth 2.0**.

---

## 📁 Структура проекта

```text
nethub/
│
├── config.json             # Файл конфигурации (порты, Google OAuth, ярлыки/программы)
├── requirements.txt        # Список зависимостей Python
├── main.py                 # Главная точка входа (баннер, IP, выбор режима CLI / Web)
│
├── core/                   # Ядро утилиты
│   ├── __init__.py
│   ├── config.py           # Загрузка и валидация настроек (Pydantic)
│   ├── network.py          # Асинхронный сканер портов, ping, сетевые интерфейсы, внешний IP
│   └── launcher.py         # Безопасный запуск ярлыков (.lnk) и программ в Windows
│
├── cli/                    # Консольный интерфейс
│   ├── __init__.py
│   └── terminal.py         # Интерактивное текстовое меню и обработка команд
│
└── web/                    # Веб-панель (Self-Hosted Web UI)
    ├── __init__.py
    ├── server.py           # FastAPI сервер, Google OAuth2, REST API эндпоинты
    └── templates.py        # Встроенный современный HTML5/Tailwind CSS интерфейс
```

---

## 🚀 Быстрый старт

### 1. Установка зависимостей
Убедитесь, что у вас установлен Python 3.10+ и выполните команду:

```powershell
pip install -r requirements.txt
```

### 2. Запуск приложения
Запустите `main.py`:

```powershell
python main.py
```

При старте программа:
1. Выведет ASCII-логотип и автоматически определит ваш текущий **внешний IP-адрес**.
2. Предложит выбор режима:
   - `[1] CLI режим` — для работы прямо в терминале Windows.
   - `[2] Web UI режим` — запустит локальный сервер на `http://localhost:8080` и откроет браузер.

---

## ⚙️ Настройка `config.json`

Файл `config.json` создается автоматически при первом запуске (или настраивается вручную):

```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 8080,
    "secret_key": "your-secret-session-key"
  },
  "google_oauth": {
    "client_id": "ВАШ_GOOGLE_CLIENT_ID.apps.googleusercontent.com",
    "client_secret": "ВАШ_GOOGLE_CLIENT_SECRET",
    "redirect_uri": "http://localhost:8080/auth/callback",
    "allowed_emails": [
      "user@gmail.com"
    ]
  },
  "apps": [
    {
      "id": "notepad",
      "name": "Блокнот",
      "path": "notepad.exe",
      "description": "Стандартный текстовый редактор"
    },
    {
      "id": "my_game",
      "name": "Моя Игра",
      "path": "C:\\Users\\Username\\Desktop\\Game.lnk",
      "description": "Ярлык запуска игры с рабочего стола"
    }
  ]
}
```

### 🛡️ Настройка Google OAuth 2.0:
1. Перейдите в [Google Cloud Console](https://console.cloud.google.com/).
2. Создайте проект и перейдите в **APIs & Services** -> **Credentials**.
3. Создайте **OAuth 2.0 Client ID** (тип: *Web application*).
4. В поле **Authorized redirect URIs** укажите: `http://localhost:8080/auth/callback`.
5. Вставьте полученные `client_id` и `client_secret` в `config.json`.
6. Добавьте ваш Google-email в массив `allowed_emails`.
> **Примечание:** Если `client_id` не заполнен, утилита автоматически запускается в **Dev Mode** (режиме отладки), чтобы вы могли протестировать весь функционал без ожидания настройки Google Cloud.

---

## 📦 Сборка в один `.exe` файл (Опционально)

Для создания автономного исполняемого файла для Windows:

```powershell
pip install pyinstaller
pyinstaller --onefile --name "NetHub" --add-data "config.json;." main.py
```
Готовый файл `NetHub.exe` появится в папке `dist/`.
