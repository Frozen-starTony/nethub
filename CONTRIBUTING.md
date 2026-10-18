# Contributing to NetHub

[English](#english) | [Русский](#русский)

---

<a name="english"></a>
## English

First off, thank you for considering contributing to **NetHub**! Every contribution — whether it's reporting a bug, proposing a new game UPnP preset, improving documentation, or adding major new features — makes a difference.

### Code of Conduct
We are committed to providing a friendly, welcoming, and harassment-free environment for everyone, regardless of experience level. Be respectful and constructive.

### How Can You Contribute?

#### 1. Quick & Easy Contributions (Good First Issues)
If you're looking for an entry point:
- **Add New UPnP Game Presets**: Add common ports for popular games (e.g., Rust, ARK, Satisfactory, Project Zomboid) in `core/upnp.py`.
- **Localization**: Help translate the CLI and Web UI into new languages (Spanish, German, French, Chinese) in `core/i18n.py`.
- **Documentation**: Spot a typo or unclear step? PRs improving docs are always appreciated!

#### 2. Intermediate & Advanced Features
- System Tray integration (`pystray` / minimize to tray instead of closing).
- Dynamic DNS (DDNS) auto-updater (DuckDNS, Cloudflare DNS API).
- Discord / Telegram webhook notifications when a game server launches or stops.
- Cross-platform support for Linux and macOS.

Check out our [ROADMAP.md](ROADMAP.md) for the full list of planned enhancements!

### Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/nethub.git
   cd nethub
   ```

2. **Create a virtual environment (Python 3.10+ recommended):**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/macOS
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the test suite:**
   Ensure everything passes before making changes:
   ```bash
   python tests/test_core.py
   python tests/test_web.py
   ```

### Branching & Commits

1. Create a dedicated branch for your work:
   ```bash
   git checkout -b feat/add-rust-preset
   # or
   git checkout -b fix/upnp-timeout-handling
   ```

2. NetHub follows **Conventional Commits**:
   - `feat: add Project Zomboid UPnP preset (ports 16261-16262)`
   - `fix: handle edge case where router SSDP response lacks location header`
   - `docs: update troubleshooting guide for CGNAT users`
   - `test: add unit test for subnet mask parsing`

3. Run tests and make sure your code passes cleanly.

4. Push your branch and open a **Pull Request** against `main` on GitHub!

---

<a name="русский"></a>
## Русский

Спасибо, что решили помочь развитию **NetHub**! Любой вклад — будь то отчёт об ошибке, добавление нового пресета для любимой игры, улучшение документации или написание нового функционала — важен и ценен.

### Как можно помочь проекту?

#### 1. Простые задачи для старта (Good First Issues)
- **Добавление пресетов для игр**: В файле `core/upnp.py` можно добавить порты для популярных игр (Rust, ARK, Satisfactory, DayZ, Project Zomboid).
- **Переводы интерфейса**: Помогите добавить поддержку новых языков (испанский, немецкий, китайский) в `core/i18n.py`.
- **Улучшение документации**: Исправление неточностей, дополнение инструкций для разных моделей роутеров.

#### 2. Средние и крупные фичи
- Сворачивание утилиты в системный трей Windows (`pystray`).
- Автоматическое обновление Dynamic DNS (интеграция с DuckDNS / Cloudflare API).
- Уведомления в Discord / Telegram при запуске сервера или открытии порта.
- Поддержка Linux и macOS для UPnP-клиента.

Полный список идей доступен в [ROADMAP.md](ROADMAP.md).

### Настройка окружения для разработки

1. Сделайте форк репозитория и склонируйте его:
   ```bash
   git clone https://github.com/<ваш-логин>/nethub.git
   cd nethub
   ```

2. Создайте и активируйте виртуальное окружение (Python 3.10+):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Запустите тесты:
   ```bash
   python tests/test_core.py
   python tests/test_web.py
   ```

### Соглашения по коммитам

Мы придерживаемся стандарта **Conventional Commits**:
- `feat: описание новой фичи`
- `fix: исправление бага`
- `docs: изменения в документации`
- `test: добавление или обновление тестов`

Сделайте Pull Request в ветку `main` — мы обязательно посмотрим и примем ваши изменения!
