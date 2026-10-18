INDEX_HTML = """<!DOCTYPE html>
<html lang="ru" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NetHub | White IP Analyzer, UPnP & Self-Hosting Hub</title>
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2338bdf8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='10'/%3E%3Cpath d='M12 2a14.5 14.5 0 0 0 0 20M2 12h20'/%3E%3C/svg%3E">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        surface: '#09090b',
                        card: '#121215',
                        border: '#27272a',
                        muted: '#71717a'
                    },
                    fontFamily: {
                        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
                        mono: ['JetBrains Mono', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'monospace']
                    }
                }
            }
        }
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
        body {
            background-color: #09090b;
            color: #f4f4f5;
        }
    </style>
</head>
<body class="min-h-screen flex flex-col font-sans antialiased text-sm">

    <!-- Top Navigation Bar -->
    <header class="border-b border-border bg-[#09090b]/90 backdrop-blur sticky top-0 z-40">
        <div class="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="w-7 h-7 rounded border border-zinc-700 bg-zinc-900 flex items-center justify-center text-zinc-300">
                    <svg class="w-4 h-4 text-sky-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/>
                        <path d="M12 2a14.5 14.5 0 0 0 0 20M2 12h20"/>
                    </svg>
                </div>
                <div class="flex items-center space-x-2">
                    <span class="font-semibold tracking-tight text-white">NetHub</span>
                    <span class="text-[10px] uppercase tracking-wider px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-400 font-mono border border-zinc-700">White IP Hub</span>
                </div>
            </div>

            <div class="flex items-center space-x-3">
                <div id="ipStatusPill" class="flex items-center space-x-2 px-2.5 py-1 rounded bg-zinc-900/80 border border-zinc-800 text-xs font-mono">
                    <span class="w-2 h-2 rounded-full bg-zinc-600 animate-pulse" id="ipStatusDot"></span>
                    <span id="externalIpBadge" class="text-zinc-400">Анализ сети...</span>
                </div>

                <div id="authStatusContainer" class="flex items-center space-x-2">
                    <!-- Dynamic Auth State -->
                </div>
            </div>
        </div>
    </header>

    <!-- Dev Mode Notice -->
    <div id="devModeNotice" class="hidden bg-amber-950/30 border-b border-amber-800/40 px-4 py-2 text-xs text-amber-200/90 text-center font-mono">
        Режим отладки: Google OAuth не настроен в config.json. Доступ к панели открыт локально.
    </div>

    <!-- Main Container -->
    <main class="flex-1 max-w-6xl mx-auto px-4 py-6 w-full space-y-6">
        <!-- Navigation Tabs -->
        <nav class="flex space-x-1 border-b border-border pb-2 overflow-x-auto">
            <button onclick="switchTab('ip-analysis')" id="tabBtn-ip-analysis" class="tab-btn px-3 py-1.5 rounded text-xs font-medium transition flex items-center space-x-2 bg-zinc-800 text-zinc-100 border border-zinc-700">
                <svg class="w-3.5 h-3.5 text-zinc-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/><path d="m4.93 4.93 4.24 4.24M14.83 9.17l4.24-4.24M14.83 14.83l4.24 4.24M9.17 14.83l-4.24 4.24"/>
                </svg>
                <span>Анализ: Белый или Серый IP</span>
            </button>
            <button onclick="switchTab('upnp')" id="tabBtn-upnp" class="tab-btn px-3 py-1.5 rounded text-xs font-medium transition flex items-center space-x-2 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/50">
                <svg class="w-3.5 h-3.5 text-zinc-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
                <span>UPnP: Авто-проброс портов</span>
            </button>
            <button onclick="switchTab('guide')" id="tabBtn-guide" class="tab-btn px-3 py-1.5 rounded text-xs font-medium transition flex items-center space-x-2 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/50">
                <svg class="w-3.5 h-3.5 text-zinc-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><path d="M6 6h10M6 10h10"/>
                </svg>
                <span>Как получить Белый IP / Обход</span>
            </button>
            <button onclick="switchTab('apps')" id="tabBtn-apps" class="tab-btn px-3 py-1.5 rounded text-xs font-medium transition flex items-center space-x-2 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/50">
                <svg class="w-3.5 h-3.5 text-zinc-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/>
                </svg>
                <span>Запуск серверов и программ</span>
            </button>
            <button onclick="switchTab('settings')" id="tabBtn-settings" class="tab-btn px-3 py-1.5 rounded text-xs font-medium transition flex items-center space-x-2 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/50">
                <svg class="w-3.5 h-3.5 text-zinc-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
                </svg>
                <span>Настройки и OAuth</span>
            </button>
        </nav>

        <!-- TAB 1: БЕЛЫЙ ИЛИ СЕРЫЙ IP (АНАЛИЗАТОР) -->
        <section id="tabContent-ip-analysis" class="space-y-6">
            <!-- Главная статусная карточка IP -->
            <div class="border border-border bg-[#121215] rounded-lg p-5 space-y-4">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-border pb-4">
                    <div>
                        <div class="text-[11px] font-mono text-zinc-400 uppercase tracking-wider">Ваш публичный адрес</div>
                        <div class="text-2xl font-bold font-mono text-white tracking-tight flex items-center space-x-3 mt-0.5">
                            <span id="analysisIpText">Определение...</span>
                        </div>
                    </div>
                    <div id="ipTypeBadgeContainer">
                        <span class="inline-flex items-center px-3 py-1 rounded text-xs font-mono font-medium bg-zinc-800 text-zinc-400 border border-zinc-700">
                            Выполняется диагностика...
                        </span>
                    </div>
                </div>

                <!-- Метаданные провайдера -->
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono">
                    <div class="p-3 rounded bg-zinc-900/60 border border-zinc-800">
                        <div class="text-zinc-500 text-[10px] uppercase">Провайдер (ISP)</div>
                        <div id="analysisIsp" class="text-zinc-200 font-medium truncate mt-0.5">...</div>
                    </div>
                    <div class="p-3 rounded bg-zinc-900/60 border border-zinc-800">
                        <div class="text-zinc-500 text-[10px] uppercase">Автономная система (AS)</div>
                        <div id="analysisAsn" class="text-zinc-200 font-medium truncate mt-0.5">...</div>
                    </div>
                    <div class="p-3 rounded bg-zinc-900/60 border border-zinc-800">
                        <div class="text-zinc-500 text-[10px] uppercase">Локация</div>
                        <div id="analysisLocation" class="text-zinc-200 font-medium truncate mt-0.5">...</div>
                    </div>
                    <div class="p-3 rounded bg-zinc-900/60 border border-zinc-800">
                        <div class="text-zinc-500 text-[10px] uppercase">Маршрутизация</div>
                        <div id="analysisRoute" class="text-zinc-200 font-medium truncate mt-0.5">...</div>
                    </div>
                </div>

                <!-- Вердикт и понятное объяснение для пользователя -->
                <div id="ipVerdictBox" class="p-4 rounded border text-xs space-y-2">
                    <div class="font-semibold text-sm" id="ipVerdictTitle">Проверка статуса IP-адреса...</div>
                    <div class="text-zinc-400 text-xs leading-relaxed" id="ipVerdictDesc">
                        Система анализирует диапазоны подсетей и структуру маршрутизации вашего провайдера.
                    </div>
                </div>
            </div>

            <!-- Внешняя проверка порта из интернета -->
            <div class="border border-border bg-[#121215] rounded-lg p-5 space-y-4">
                <div>
                    <h2 class="text-sm font-semibold text-white tracking-tight">Проверка доступности порта из внешней сети (WAN Reachability)</h2>
                    <p class="text-xs text-muted mt-0.5">
                        Проверяет, могут ли игроки, друзья или внешние устройства подключиться к вашему порту из Интернета.
                    </p>
                </div>

                <div class="flex flex-col sm:flex-row gap-3">
                    <div class="flex-1">
                        <label class="block text-[11px] font-mono text-zinc-400 uppercase tracking-wider mb-1">Номер порта</label>
                        <input type="number" id="checkPortInput" value="25565" placeholder="например, 25565 (Minecraft) или 8080" 
                               class="w-full bg-zinc-900 border border-zinc-700/80 rounded px-3 py-1.5 text-xs text-zinc-100 font-mono focus:outline-none focus:border-zinc-500">
                    </div>
                    <div class="flex items-end space-x-2">
                        <button onclick="setCheckPortPreset(25565)" class="px-2.5 py-1.5 bg-zinc-800 text-zinc-300 rounded text-xs font-mono border border-zinc-700">MC (25565)</button>
                        <button onclick="setCheckPortPreset(8080)" class="px-2.5 py-1.5 bg-zinc-800 text-zinc-300 rounded text-xs font-mono border border-zinc-700">Web (8080)</button>
                        <button onclick="setCheckPortPreset(3389)" class="px-2.5 py-1.5 bg-zinc-800 text-zinc-300 rounded text-xs font-mono border border-zinc-700">RDP (3389)</button>
                        <button onclick="runExternalPortCheck()" id="checkPortBtn" 
                                class="px-4 py-1.5 bg-zinc-100 hover:bg-white text-zinc-950 text-xs font-medium rounded transition">
                            Проверить из Интернета
                        </button>
                    </div>
                </div>

                <div id="checkPortResult" class="hidden p-3 rounded border text-xs font-mono">
                    <!-- Заполняется JS -->
                </div>
            </div>
        </section>

        <!-- TAB 2: АВТО-ПРОБРОС ПОРТОВ (UPNP) -->
        <section id="tabContent-upnp" class="hidden space-y-6">
            <div class="border border-border bg-[#121215] rounded-lg p-5 space-y-4">
                <div>
                    <h2 class="text-sm font-semibold text-white tracking-tight">UPnP: Автоматическое открытие портов на роутере</h2>
                    <p class="text-xs text-muted mt-0.5">
                        Открывайте порты для игр и серверов в 1 клик прямо с компьютера, без необходимости заходить в панель управления роутером (192.168.1.1).
                    </p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3" id="upnpPresetsContainer">
                    <!-- Заполняется JS из /api/presets -->
                </div>
            </div>

            <!-- Ручной проброс кастомного порта -->
            <div class="border border-border bg-[#121215] rounded-lg p-5 space-y-3">
                <h3 class="text-xs font-semibold uppercase tracking-wider text-zinc-300 font-mono">Кастомный проброс порта</h3>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    <div>
                        <label class="block text-[11px] font-mono text-zinc-400 mb-1">Порт</label>
                        <input type="number" id="customUpnpPort" value="8080" 
                               class="w-full bg-zinc-900 border border-zinc-700/80 rounded px-3 py-1.5 text-xs text-zinc-100 font-mono focus:outline-none focus:border-zinc-500">
                    </div>
                    <div>
                        <label class="block text-[11px] font-mono text-zinc-400 mb-1">Протокол</label>
                        <select id="customUpnpProto" class="w-full bg-zinc-900 border border-zinc-700/80 rounded px-3 py-1.5 text-xs text-zinc-100 font-mono focus:outline-none focus:border-zinc-500">
                            <option value="TCP">TCP</option>
                            <option value="UDP">UDP</option>
                        </select>
                    </div>
                    <div class="flex items-end">
                        <button onclick="triggerCustomUpnp()" class="w-full py-1.5 bg-zinc-100 hover:bg-white text-zinc-950 text-xs font-medium rounded transition">
                            Открыть порт через UPnP
                        </button>
                    </div>
                </div>

                <div id="upnpStatusBox" class="hidden p-3 rounded border text-xs font-mono">
                    <!-- Результат UPnP -->
                </div>
            </div>
        </section>

        <!-- TAB 3: БАЗА ЗНАНИЙ: КАК ПОЛУЧИТЬ БЕЛЫЙ IP / ОБХОД -->
        <section id="tabContent-guide" class="hidden space-y-6">
            <!-- Способ 1: Получение у провайдера -->
            <div class="border border-border bg-[#121215] rounded-lg p-5 space-y-3">
                <div class="flex items-center justify-between">
                    <h3 class="text-sm font-semibold text-white">1. Как заказать Белый (Статический) IP у вашего провайдера</h3>
                    <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Лучший вариант</span>
                </div>
                <p class="text-xs text-zinc-400 leading-relaxed">
                    Белый IP позволяет подключаться к вашему ПК напрямую по IP-адресу без задержек и сторонних посредников. Стоимость у большинства провайдеров РФ составляет от 100 до 150 рублей в месяц.
                </p>
                <div class="p-3.5 rounded bg-zinc-900 border border-zinc-800 space-y-2 text-xs font-mono text-zinc-300">
                    <div class="text-zinc-200 font-semibold">Готовый шаблон для техподдержки вашего провайдера:</div>
                    <div class="bg-black/50 p-2.5 rounded border border-zinc-800 text-sky-300 select-all">
                        «Здравствуйте! Мне необходимо подключить услугу "Статический белый IP-адрес" (публичный IPv4) на моём договоре для хостинга игрового сервера и удаленного доступа. Подключите, пожалуйста.»
                    </div>
                    <div class="text-[11px] text-zinc-400 pt-1">
                        • <b>Ростелеком:</b> опция «Статический IP» в личном кабинете или через чат поддержки.<br/>
                        • <b>МТС / Дом.ру / Билайн:</b> подключается в мобильном приложении в разделе «Услуги».
                    </div>
                </div>
            </div>

            <!-- Способ 2: Бесплатный обход Серого IP (CGNAT) без звонков провайдеру -->
            <div class="border border-border bg-[#121215] rounded-lg p-5 space-y-3">
                <div class="flex items-center justify-between">
                    <h3 class="text-sm font-semibold text-white">2. Бесплатные способы открыть доступ, если у вас Серый IP</h3>
                    <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-sky-500/10 text-sky-400 border border-sky-500/20">Без доплат</span>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-1 text-xs">
                    <div class="p-3.5 rounded bg-zinc-900 border border-zinc-800 space-y-2">
                        <div class="font-semibold text-white font-mono flex items-center justify-between">
                            <span>Playit.gg</span>
                            <span class="text-[10px] text-emerald-400">Для игр</span>
                        </div>
                        <p class="text-[11px] text-zinc-400 leading-relaxed">
                            Идеально для Minecraft, CS2, Palworld. Дает постоянный публичный адрес (например, <code class="text-zinc-300">mine.joinmc.link</code>), через который друзья подключаются без белого IP и без роутера.
                        </p>
                        <a href="https://playit.gg/" target="_blank" class="inline-block text-[11px] text-sky-400 hover:underline font-mono">Скачать playit.gg &rarr;</a>
                    </div>

                    <div class="p-3.5 rounded bg-zinc-900 border border-zinc-800 space-y-2">
                        <div class="font-semibold text-white font-mono flex items-center justify-between">
                            <span>Cloudflare Tunnels</span>
                            <span class="text-[10px] text-sky-400">Для сайтов / API</span>
                        </div>
                        <p class="text-[11px] text-zinc-400 leading-relaxed">
                            Бесплатный инструмент Cloudflare. Пробрасывает локальный порт (например, 8080) на ваш личный домен без белого IP и с бесплатной защитой от DDoS-атак.
                        </p>
                        <a href="https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/" target="_blank" class="inline-block text-[11px] text-sky-400 hover:underline font-mono">Инструкция Cloudflare &rarr;</a>
                    </div>

                    <div class="p-3.5 rounded bg-zinc-900 border border-zinc-800 space-y-2">
                        <div class="font-semibold text-white font-mono flex items-center justify-between">
                            <span>Tailscale</span>
                            <span class="text-[10px] text-indigo-400">Для друзей и RDP</span>
                        </div>
                        <p class="text-[11px] text-zinc-400 leading-relaxed">
                            Создает защищенную виртуальную локальную сеть на базе WireGuard между вашими устройствами. Позволяет подключаться к удаленному рабочему столу (RDP) откуда угодно.
                        </p>
                        <a href="https://tailscale.com/" target="_blank" class="inline-block text-[11px] text-sky-400 hover:underline font-mono">Перейти в Tailscale &rarr;</a>
                    </div>
                </div>
            </div>

            <!-- Способ 3: Как выжать максимум из Белого IP (DDNS) -->
            <div class="border border-border bg-[#121215] rounded-lg p-5 space-y-3">
                <h3 class="text-sm font-semibold text-white">3. Если у вас Динамический Белый IP: Настройка бесплатного DDNS</h3>
                <p class="text-xs text-zinc-400 leading-relaxed">
                    Если провайдер выдает белый адрес, но он периодически меняется при перезагрузке роутера, привяжите к нему бесплатное постоянное доменное имя (Dynamic DNS).
                </p>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                    <div class="p-3 rounded bg-zinc-900 border border-zinc-800 space-y-1">
                        <div class="font-medium text-white font-mono">DuckDNS (duckdns.org)</div>
                        <div class="text-[11px] text-zinc-400">Бесплатный поддомен вида <code class="text-sky-300">yourname.duckdns.org</code>, который автоматически обновляется при смене вашего IP.</div>
                    </div>
                    <div class="p-3 rounded bg-zinc-900 border border-zinc-800 space-y-1">
                        <div class="font-medium text-white font-mono">Роутерный DDNS (Keenetic / ASUS)</div>
                        <div class="text-[11px] text-zinc-400">Встроенные бесплатные сервисы KeenDNS или ASUS DDNS прямо в веб-интерфейсе вашего роутера.</div>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 4: ЗАПУСК ПРИЛОЖЕНИЙ И СЕРВЕРОВ -->
        <section id="tabContent-apps" class="hidden space-y-4">
            <div>
                <h2 class="text-sm font-semibold text-white tracking-tight">Диспетчер процессов и серверов</h2>
                <p class="text-xs text-muted mt-0.5">Быстрый запуск зарегистрированных серверов, ярлыков и утилит на компьютере.</p>
            </div>

            <div id="appsGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                <!-- Карточки процессов -->
            </div>

            <div id="launchToast" class="fixed bottom-6 right-6 hidden bg-zinc-900 border border-zinc-700 p-3 rounded-md shadow-xl z-50 text-xs flex items-center space-x-2.5 font-mono">
                <span class="w-2 h-2 rounded-full bg-sky-400 animate-pulse"></span>
                <span id="launchToastMsg" class="text-zinc-200">Запуск...</span>
            </div>
        </section>

        <!-- TAB 5: НАСТРОЙКИ И OAUTH -->
        <section id="tabContent-settings" class="hidden space-y-4">
            <div class="border border-border bg-[#121215] rounded-lg p-5 space-y-4">
                <div>
                    <h2 class="text-sm font-semibold text-white tracking-tight">Авторизация Google OAuth 2.0</h2>
                    <p class="text-xs text-muted mt-0.5">Безопасный доступ к панели управления по вашей учетной записи Google.</p>
                </div>

                <div class="space-y-4 text-xs">
                    <div class="p-3.5 rounded bg-zinc-900/60 border border-zinc-800 space-y-2 text-zinc-300">
                        <div class="font-medium text-white">Инструкция по привязке:</div>
                        <ol class="list-decimal list-inside space-y-1 text-zinc-400 font-mono text-[11px]">
                            <li>Создайте проект на <a href="https://console.cloud.google.com/" target="_blank" class="text-sky-400 hover:underline">Google Cloud Console</a>.</li>
                            <li>В разделе <b>APIs & Services</b> &rarr; <b>Credentials</b> создайте <b>OAuth 2.0 Client ID</b> (Web application).</li>
                            <li>Укажите redirect URI: <code class="bg-black/60 text-zinc-200 px-1.5 py-0.5 rounded border border-zinc-800">http://localhost:8080/auth/callback</code></li>
                            <li>Вставьте <code>client_id</code> и <code>client_secret</code> в файл <code>config.json</code>.</li>
                            <li>Добавьте ваш Gmail в <code>allowed_emails</code>.</li>
                        </ol>
                    </div>

                    <div>
                        <div class="text-[11px] font-mono uppercase tracking-wider text-zinc-400 mb-2">Разрешенные адреса:</div>
                        <div id="allowedEmailsList" class="flex flex-wrap gap-1.5">
                            <!-- Заполняется JS -->
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="border-t border-border py-4 mt-8 bg-[#09090b] text-center text-[11px] text-zinc-500 font-mono">
        NetHub Windows 11 Network Toolkit &bull; White IP Diagnostics &bull; UPnP Controller
    </footer>

    <!-- Client Script -->
    <script>
        let currentAnalysisData = null;

        function switchTab(tabId) {
            document.querySelectorAll('[id^="tabContent-"]').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.className = "tab-btn px-3 py-1.5 rounded text-xs font-medium transition flex items-center space-x-2 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/50";
            });

            const content = document.getElementById(`tabContent-${tabId}`);
            const btn = document.getElementById(`tabBtn-${tabId}`);
            if (content) content.classList.remove('hidden');
            if (btn) btn.className = "tab-btn px-3 py-1.5 rounded text-xs font-medium transition flex items-center space-x-2 bg-zinc-800 text-zinc-100 border border-zinc-700";

            if (tabId === 'upnp') loadUpnpPresets();
            if (tabId === 'apps') loadApps();
        }

        async function initData() {
            try {
                // 1. Auth Status
                const authRes = await fetch('/auth/status');
                const authData = await authRes.json();
                
                const container = document.getElementById('authStatusContainer');
                if (authData.dev_mode) {
                    document.getElementById('devModeNotice').classList.remove('hidden');
                    container.innerHTML = `
                        <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-mono font-medium bg-zinc-800 text-zinc-300 border border-zinc-700">
                            <span class="w-1.5 h-1.5 rounded-full bg-amber-400 mr-1.5"></span>
                            Dev Mode
                        </span>
                    `;
                } else if (authData.authenticated) {
                    container.innerHTML = `
                        <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-mono font-medium bg-zinc-800 text-zinc-300 border border-zinc-700">
                            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-1.5"></span>
                            ${authData.user}
                        </span>
                        <a href="/auth/logout" class="text-xs text-zinc-400 hover:text-zinc-200 transition font-mono ml-2">Выход</a>
                    `;
                } else {
                    container.innerHTML = `
                        <a href="/auth/login" class="px-2.5 py-1 bg-zinc-100 hover:bg-white text-zinc-950 text-xs font-medium rounded transition">
                            Вход через Google
                        </a>
                    `;
                }

                // Whitelisted emails
                const emailContainer = document.getElementById('allowedEmailsList');
                if (authData.allowed_emails && authData.allowed_emails.length > 0) {
                    emailContainer.innerHTML = authData.allowed_emails.map(e => `
                        <span class="px-2 py-0.5 bg-zinc-900 text-zinc-300 rounded font-mono text-[11px] border border-zinc-800">${e}</span>
                    `).join('');
                } else {
                    emailContainer.innerHTML = '<span class="text-xs text-zinc-500 font-mono">Список пуст</span>';
                }

                // 2. White IP Analysis
                loadIpAnalysis();

            } catch (err) {
                console.error("Init failed:", err);
            }
        }

        async function loadIpAnalysis() {
            try {
                const res = await fetch('/api/ip-analysis');
                const data = await res.json();
                currentAnalysisData = data;

                document.getElementById('analysisIpText').textContent = data.ip;
                document.getElementById('externalIpBadge').textContent = data.ip;
                document.getElementById('analysisIsp').textContent = data.isp;
                document.getElementById('analysisAsn').textContent = data.asn;
                document.getElementById('analysisLocation').textContent = `${data.city}, ${data.country}`;
                document.getElementById('analysisRoute').textContent = data.is_white ? 'Прямой маршрут' : 'Через CGNAT';

                const badgeContainer = document.getElementById('ipTypeBadgeContainer');
                const verdictBox = document.getElementById('ipVerdictBox');
                const verdictTitle = document.getElementById('ipVerdictTitle');
                const verdictDesc = document.getElementById('ipVerdictDesc');
                const dot = document.getElementById('ipStatusDot');

                if (data.is_white) {
                    dot.className = "w-2 h-2 rounded-full bg-emerald-400";
                    badgeContainer.innerHTML = `
                        <span class="inline-flex items-center px-3 py-1 rounded text-xs font-mono font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                            БЕЛЫЙ (ПУБЛИЧНЫЙ) IP
                        </span>
                    `;
                    verdictBox.className = "p-4 rounded bg-emerald-950/20 border border-emerald-500/30 text-xs space-y-2";
                    verdictTitle.className = "font-bold text-sm text-emerald-300";
                    verdictTitle.textContent = "Отличные новости: У вас Белый (Публичный) IP-адрес!";
                    verdictDesc.className = "text-zinc-300 leading-relaxed";
                    verdictDesc.innerHTML = `
                        Ваш компьютер доступен напрямую из глобальной сети Интернет. Вы можете открывать порты через вкладку <b>UPnP</b>, хостить игровые серверы (Minecraft, CS2, Palworld), поднимать домашнее облако или использовать Удаленный рабочий стол (RDP) без сторонних прокси.
                    `;
                } else if (data.is_cgnat) {
                    dot.className = "w-2 h-2 rounded-full bg-amber-400";
                    badgeContainer.innerHTML = `
                        <span class="inline-flex items-center px-3 py-1 rounded text-xs font-mono font-bold bg-amber-500/10 text-amber-400 border border-amber-500/30">
                            СЕРЫЙ IP (CGNAT / NAT ПРОВАЙДЕРА)
                        </span>
                    `;
                    verdictBox.className = "p-4 rounded bg-amber-950/20 border border-amber-500/30 text-xs space-y-2";
                    verdictTitle.className = "font-bold text-sm text-amber-300";
                    verdictTitle.textContent = "Внимание: Ваш IP находится за CGNAT провайдера (Серый IP)";
                    verdictDesc.className = "text-zinc-300 leading-relaxed";
                    verdictDesc.innerHTML = `
                        Провайдер поместил вас за общий пул адресов. Прямой проброс портов работать не будет. Перейдите во вкладку <b>«Как получить Белый IP / Обход»</b> — там описано, как бесплатно открыть доступ через Playit.gg / Cloudflare Tunnels или заказать статический белый IP.
                    `;
                } else {
                    dot.className = "w-2 h-2 rounded-full bg-sky-400";
                    badgeContainer.innerHTML = `
                        <span class="inline-flex items-center px-3 py-1 rounded text-xs font-mono font-bold bg-sky-500/10 text-sky-400 border border-sky-500/30">
                            СТАНДАРТНЫЙ ПУБЛИЧНЫЙ МАРШРУТ
                        </span>
                    `;
                    verdictBox.className = "p-4 rounded bg-zinc-900 border border-zinc-800 text-xs space-y-2";
                    verdictTitle.className = "font-bold text-sm text-zinc-200";
                    verdictTitle.textContent = "IP-адрес успешно зарегистрирован в глобальной сети";
                    verdictDesc.textContent = "Выполните проверку порта ниже, чтобы узнать доступность из Интернета.";
                }

            } catch (err) {
                console.error("IP analysis error:", err);
            }
        }

        function setCheckPortPreset(port) {
            document.getElementById('checkPortInput').value = port;
            runExternalPortCheck();
        }

        async function runExternalPortCheck() {
            const port = parseInt(document.getElementById('checkPortInput').value);
            const btn = document.getElementById('checkPortBtn');
            const card = document.getElementById('checkPortResult');

            if (!port) return;

            btn.disabled = true;
            btn.textContent = "Проверка...";
            card.classList.remove('hidden');
            card.className = "p-3 rounded bg-zinc-900 border border-zinc-800 text-zinc-400 text-xs font-mono";
            card.textContent = `Запрос к внешнему сетевому сканеру для порта ${port}...`;

            try {
                const res = await fetch('/api/check-port', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({port: port})
                });
                const data = await res.json();

                if (data.is_open) {
                    card.className = "p-3 rounded bg-zinc-900 border border-emerald-500/40 text-emerald-400 text-xs font-mono";
                    card.innerHTML = `<b>УСПЕХ:</b> Порт ${data.port} ОТКРЫТ и доступен из Интернета! Друзья могут подключаться по адресу: <code>${currentAnalysisData?.ip || ''}:${data.port}</code>`;
                } else {
                    card.className = "p-3 rounded bg-zinc-900 border border-amber-500/40 text-amber-300 text-xs font-mono";
                    card.innerHTML = `<b>ЗАКРЫТ:</b> Порт ${data.port} не отвечает из внешней сети. Если сервер уже запущен на ПК, откройте его во вкладке <b>UPnP</b>.`;
                }
            } catch (err) {
                card.className = "p-3 rounded bg-zinc-900 border border-red-500/40 text-red-400 text-xs font-mono";
                card.textContent = "Ошибка внешней проверки: " + err;
            } finally {
                btn.disabled = false;
                btn.textContent = "Проверить из Интернета";
            }
        }

        async function loadUpnpPresets() {
            const container = document.getElementById('upnpPresetsContainer');
            if (container.children.length > 0) return;

            try {
                const res = await fetch('/api/presets');
                const presets = await res.json();

                container.innerHTML = presets.map(p => `
                    <div class="border border-border bg-zinc-900/60 rounded-md p-3.5 flex flex-col justify-between space-y-3">
                        <div>
                            <div class="flex items-center justify-between">
                                <span class="font-semibold text-white text-xs">${p.name}</span>
                                <span class="text-[10px] font-mono px-1 rounded bg-zinc-800 text-sky-400 border border-zinc-700">${p.protocol} ${p.port}</span>
                            </div>
                            <p class="text-[11px] text-zinc-400 mt-1">${p.desc}</p>
                        </div>
                        <button onclick="forwardPreset(${p.port}, '${p.protocol}', '${p.name}')" 
                                class="w-full py-1.5 px-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-xs font-mono rounded border border-zinc-700 transition">
                            Открыть порт ${p.port}
                        </button>
                    </div>
                `).join('');
            } catch (err) {
                console.error("Presets error:", err);
            }
        }

        async function forwardPreset(port, protocol, name) {
            const box = document.getElementById('upnpStatusBox');
            box.classList.remove('hidden');
            box.className = "p-3 rounded bg-zinc-900 border border-zinc-800 text-zinc-300 text-xs font-mono";
            box.textContent = `Отправка UPnP команды роутеру для ${name} (порт ${port} ${protocol})...`;

            try {
                const res = await fetch('/api/upnp-forward', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({port: port, protocol: protocol, description: name})
                });
                const data = await res.json();

                if (data.success) {
                    box.className = "p-3 rounded bg-zinc-900 border border-emerald-500/40 text-emerald-400 text-xs font-mono";
                    box.innerHTML = `<b>УСПЕХ:</b> ${data.message}`;
                } else {
                    box.className = "p-3 rounded bg-zinc-900 border border-red-500/40 text-red-400 text-xs font-mono";
                    box.innerHTML = `<b>ОШИБКА:</b> ${data.error}`;
                }
            } catch (err) {
                box.className = "p-3 rounded bg-zinc-900 border border-red-500/40 text-red-400 text-xs font-mono";
                box.textContent = "Сбой запроса: " + err;
            }
        }

        async function triggerCustomUpnp() {
            const port = parseInt(document.getElementById('customUpnpPort').value);
            const proto = document.getElementById('customUpnpProto').value;
            if (!port) return;
            forwardPreset(port, proto, `Custom Port ${port}`);
        }

        async function loadApps() {
            const grid = document.getElementById('appsGrid');
            grid.innerHTML = '<div class="col-span-full text-center text-zinc-500 text-xs py-6 font-mono">Загрузка списка программ...</div>';

            try {
                const res = await fetch('/api/apps');
                const apps = await res.json();

                if (apps.length === 0) {
                    grid.innerHTML = '<div class="col-span-full text-center text-zinc-500 text-xs py-6 font-mono">Нет настроенных программ в config.json</div>';
                    return;
                }

                grid.innerHTML = apps.map(app => `
                    <div class="border border-border bg-[#121215] rounded-md p-4 flex flex-col justify-between space-y-3 hover:border-zinc-700 transition">
                        <div>
                            <div class="flex items-center justify-between mb-1.5">
                                <h3 class="font-medium text-white text-xs">${app.name}</h3>
                                <span class="text-[10px] font-mono uppercase px-1 rounded bg-zinc-900 border border-zinc-800 text-zinc-400">Process</span>
                            </div>
                            <p class="text-[11px] text-zinc-400 mb-2">${app.description || 'Локальный запуск'}</p>
                            <div class="text-[10px] font-mono text-zinc-500 truncate" title="${app.path}">Путь: ${app.path}</div>
                        </div>

                        <button onclick="launchApp('${app.id}')" 
                                class="w-full py-1.5 px-3 bg-zinc-900 hover:bg-zinc-800 text-zinc-200 text-xs font-mono font-medium rounded border border-zinc-700 transition flex items-center justify-center space-x-1.5">
                            <span>Запустить сейчас</span>
                            <span class="text-zinc-500">&rarr;</span>
                        </button>
                    </div>
                `).join('');

            } catch (err) {
                grid.innerHTML = `<div class="col-span-full text-center text-red-400 text-xs py-6 font-mono">Ошибка загрузки: ${err}</div>`;
            }
        }

        async function launchApp(appId) {
            const toast = document.getElementById('launchToast');
            const msg = document.getElementById('launchToastMsg');

            toast.classList.remove('hidden');
            msg.textContent = `Отправка сигнала запуска для ${appId}...`;

            try {
                const res = await fetch(`/api/launch/${appId}`, { method: 'POST' });
                const data = await res.json();

                if (data.success) {
                    msg.textContent = `Успех: ${data.message}`;
                } else {
                    msg.textContent = `Ошибка: ${data.error}`;
                }
            } catch (err) {
                msg.textContent = `Сбой: ${err}`;
            }

            setTimeout(() => {
                toast.classList.add('hidden');
            }, 4000);
        }

        window.addEventListener('DOMContentLoaded', () => {
            initData();
        });
    </script>
</body>
</html>
"""
