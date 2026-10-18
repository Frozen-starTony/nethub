# NetHub Development Roadmap

[English](#english) | [Русский](#русский)

---

<a name="english"></a>
## English

Here is the strategic feature roadmap for **NetHub**. Features marked with **`[Good First Issue]`** or **`[Help Wanted]`** are ideal entry points for new contributors!

### Short-Term Milestones (v1.1.0)
- [ ] **`[Good First Issue]` Expand UPnP Service Presets:**
  - Rust Dedicated Server (`UDP 28015-28016`)
  - ARK: Survival Evolved (`UDP 7777-7778, 27015`)
  - Project Zomboid (`UDP 16261, TCP 16262`)
  - Factorio Multiplayer (`UDP 34197`)
  - 7 Days to Die (`TCP/UDP 26900-26902`)
- [ ] **`[Good First Issue]` Additional Translations:**
  - Spanish (`es`)
  - German (`de`)
  - Chinese Simplified (`zh-CN`)
- [ ] **`[Help Wanted]` Windows System Tray Minimization:**
  - Add optional minimize-to-tray capability via `pystray` so NetHub runs silently in the background while servers are active.
- [ ] **`[Help Wanted]` Dynamic DNS (DDNS) Sync Engine:**
  - Auto-update DuckDNS or Cloudflare DNS record when dynamic Public IP changes.

### Mid-Term Milestones (v1.2.0)
- [ ] **`[Help Wanted]` Webhook Notification Alerts:**
  - Send instant alerts to Discord or Telegram when game servers launch, stop, or ports are mapped.
- [ ] **Direct CGNAT Tunnel Integrations:**
  - Built-in one-click tunnel launch for users behind CGNAT (Playit.gg agent and Cloudflare `cloudflared` wrapper).
- [ ] **Automated Port Lease Renewal Daemon:**
  - Keep UPnP lease alive with background refresh for routers that expire leases after 3600 seconds.

### Long-Term Vision (v2.0.0)
- [ ] **Cross-Platform Compatibility:**
  - Bring core UPnP & network classification to Linux and macOS.
- [ ] **Embedded Web Terminal:**
  - Interactive web console (`xterm.js`) inside the Web UI for direct live output of running game server terminals.

---

<a name="русский"></a>
## Русский

Стратегический план развития **NetHub**. Задачи с метками **`[Good First Issue]`** и **`[Help Wanted]`** открыты для любого желающего внести свой вклад!

### Ближайшие планы (v1.1.0)
- [ ] **`[Good First Issue]` Новые пресеты для игр:**
  - Rust Dedicated Server (`UDP 28015-28016`)
  - ARK: Survival Evolved (`UDP 7777-7778, 27015`)
  - Project Zomboid (`UDP 16261, TCP 16262`)
  - Factorio Multiplayer (`UDP 34197`)
  - 7 Days to Die (`TCP/UDP 26900-26902`)
- [ ] **`[Good First Issue]` Локализация на новые языки:**
  - Испанский (`es`)
  - Немецкий (`de`)
  - Китайский (`zh-CN`)
- [ ] **`[Help Wanted]` Сворачивание в системный трей Windows:**
  - Интеграция с `pystray`, чтобы программа работала в фоне, не занимая место в панели задач.
- [ ] **`[Help Wanted]` Синхронизация с Dynamic DNS (DDNS):**
  - Автоматическое обновление записей в DuckDNS или Cloudflare при смене динамического IP.

### Среднесрочные планы (v1.2.0)
- [ ] **`[Help Wanted]` Оповещения в Discord / Telegram:**
  - Отправка вебхуков при старте/падении сервера или успешном пробросе порта.
- [ ] **Встроенный обход CGNAT:**
  - Запуск туннелей Playit.gg и Cloudflare `cloudflared` в один клик прямо из веб-панели для пользователей без белого IP.
- [ ] **Фоновый демон продления аренды UPnP:**
  - Автоматическое продление аренды портов на капризных роутерах, сбрасывающих UPnP раз в час.

### Долгосрочные планы (v2.0.0)
- [ ] **Кроссплатформенность:**
  - Поддержка Linux и macOS для сетевого ядра и UPnP.
- [ ] **Веб-терминал в панели управления:**
  - Просмотр логов игрового сервера в реальном времени через веб-интерфейс (`xterm.js`).
