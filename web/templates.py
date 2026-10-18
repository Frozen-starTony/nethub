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
                <!-- IP Badge -->
                <div id="ipStatusPill" class="flex items-center space-x-2 px-2.5 py-1 rounded bg-zinc-900/80 border border-zinc-800 text-xs font-mono">
                    <span class="w-2 h-2 rounded-full bg-zinc-600 animate-pulse" id="ipStatusDot"></span>
                    <span id="externalIpBadge" class="text-zinc-400">...</span>
                </div>

                <!-- Language Switcher Button -->
                <button onclick="toggleLang()" id="langBtn" class="px-2 py-1 rounded bg-zinc-800 hover:bg-zinc-700 text-zinc-300 border border-zinc-700 text-xs font-mono font-medium transition">
                    RU
                </button>

                <!-- Auth Status -->
                <div id="authStatusContainer" class="flex items-center space-x-2"></div>
            </div>
        </div>
    </header>

    <!-- Dev Mode Notice -->
    <div id="devModeNotice" class="hidden bg-amber-950/30 border-b border-amber-800/40 px-4 py-2 text-xs text-amber-200/90 text-center font-mono">
        <span data-i18n="dev_notice">Режим отладки: Google OAuth не настроен в config.json. Доступ к панели открыт локально.</span>
    </div>

    <!-- Main Container -->
    <main class="flex-1 max-w-6xl mx-auto px-4 py-6 w-full space-y-6">
        <!-- Navigation Tabs -->
        <nav class="flex space-x-1 border-b border-border pb-2 overflow-x-auto">
            <button onclick="switchTab('ip-analysis')" id="tabBtn-ip-analysis" class="tab-btn px-3 py-1.5 rounded text-xs font-medium transition flex items-center space-x-2 bg-zinc-800 text-zinc-100 border border-zinc-700">
                <svg class="w-3.5 h-3.5 text-zinc-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/><path d="m4.93 4.93 4.24 4.24M14.83 9.17l4.24-4.24M14.83 14.83l4.24 4.24M9.17 14.83l-4.24 4.24"/>
                </svg>
                <span data-i18n="tab_analysis">Анализ: Белый или Серый IP</span>
            </button>
            <button onclick="switchTab('upnp')" id="tabBtn-upnp" class="tab-btn px-3 py-1.5 rounded text-xs font-medium transition flex items-center space-x-2 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/50">
                <svg class="w-3.5 h-3.5 text-zinc-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
                <span data-i18n="tab_upnp">UPnP: Авто-проброс портов</span>
            </button>
            <button onclick="switchTab('guide')" id="tabBtn-guide" class="tab-btn px-3 py-1.5 rounded text-xs font-medium transition flex items-center space-x-2 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/50">
                <svg class="w-3.5 h-3.5 text-zinc-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><path d="M6 6h10M6 10h10"/>
                </svg>
                <span data-i18n="tab_guide">Как получить Белый IP / Обход</span>
            </button>
            <button onclick="switchTab('apps')" id="tabBtn-apps" class="tab-btn px-3 py-1.5 rounded text-xs font-medium transition flex items-center space-x-2 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/50">
                <svg class="w-3.5 h-3.5 text-zinc-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/>
                </svg>
                <span data-i18n="tab_apps">Запуск серверов и программ</span>
            </button>
            <button onclick="switchTab('settings')" id="tabBtn-settings" class="tab-btn px-3 py-1.5 rounded text-xs font-medium transition flex items-center space-x-2 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/50">
                <svg class="w-3.5 h-3.5 text-zinc-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
                </svg>
                <span data-i18n="tab_settings">Настройки и OAuth</span>
            </button>
        </nav>

        <!-- TAB 1: БЕЛЫЙ ИЛИ СЕРЫЙ IP -->
        <section id="tabContent-ip-analysis" class="space-y-6">
            <div class="border border-border bg-[#121215] rounded-lg p-5 space-y-4">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-border pb-4">
                    <div>
                        <div class="text-[11px] font-mono text-zinc-400 uppercase tracking-wider" data-i18n="your_public_ip">Ваш публичный адрес</div>
                        <div class="text-2xl font-bold font-mono text-white tracking-tight flex items-center space-x-3 mt-0.5">
                            <span id="analysisIpText">...</span>
                        </div>
                    </div>
                    <div id="ipTypeBadgeContainer">
                        <span class="inline-flex items-center px-3 py-1 rounded text-xs font-mono font-medium bg-zinc-800 text-zinc-400 border border-zinc-700" data-i18n="diagnosing">
                            Выполняется диагностика...
                        </span>
                    </div>
                </div>

                <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono">
                    <div class="p-3 rounded bg-zinc-900/60 border border-zinc-800">
                        <div class="text-zinc-500 text-[10px] uppercase" data-i18n="isp_label">Провайдер (ISP)</div>
                        <div id="analysisIsp" class="text-zinc-200 font-medium truncate mt-0.5">...</div>
                    </div>
                    <div class="p-3 rounded bg-zinc-900/60 border border-zinc-800">
                        <div class="text-zinc-500 text-[10px] uppercase" data-i18n="asn_label">Автономная система (AS)</div>
                        <div id="analysisAsn" class="text-zinc-200 font-medium truncate mt-0.5">...</div>
                    </div>
                    <div class="p-3 rounded bg-zinc-900/60 border border-zinc-800">
                        <div class="text-zinc-500 text-[10px] uppercase" data-i18n="loc_label">Локация</div>
                        <div id="analysisLocation" class="text-zinc-200 font-medium truncate mt-0.5">...</div>
                    </div>
                    <div class="p-3 rounded bg-zinc-900/60 border border-zinc-800">
                        <div class="text-zinc-500 text-[10px] uppercase" data-i18n="route_label">Маршрутизация</div>
                        <div id="analysisRoute" class="text-zinc-200 font-medium truncate mt-0.5">...</div>
                    </div>
                </div>

                <div id="ipVerdictBox" class="p-4 rounded border text-xs space-y-2">
                    <div class="font-semibold text-sm" id="ipVerdictTitle">...</div>
                    <div class="text-zinc-400 text-xs leading-relaxed" id="ipVerdictDesc">...</div>
                </div>
            </div>

            <!-- Внешняя проверка порта -->
            <div class="border border-border bg-[#121215] rounded-lg p-5 space-y-4">
                <div>
                    <h2 class="text-sm font-semibold text-white tracking-tight" data-i18n="wan_check_title">Проверка доступности порта из внешней сети (WAN Reachability)</h2>
                    <p class="text-xs text-muted mt-0.5" data-i18n="wan_check_desc">
                        Проверяет, могут ли игроки, друзья или внешние устройства подключиться к вашему порту из Интернета.
                    </p>
                </div>

                <div class="flex flex-col sm:flex-row gap-3">
                    <div class="flex-1">
                        <label class="block text-[11px] font-mono text-zinc-400 uppercase tracking-wider mb-1" data-i18n="port_label">Номер порта</label>
                        <input type="number" id="checkPortInput" value="25565" placeholder="e.g. 25565" 
                               class="w-full bg-zinc-900 border border-zinc-700/80 rounded px-3 py-1.5 text-xs text-zinc-100 font-mono focus:outline-none focus:border-zinc-500">
                    </div>
                    <div class="flex items-end space-x-2">
                        <button onclick="setCheckPortPreset(25565)" class="px-2.5 py-1.5 bg-zinc-800 text-zinc-300 rounded text-xs font-mono border border-zinc-700">MC (25565)</button>
                        <button onclick="setCheckPortPreset(8080)" class="px-2.5 py-1.5 bg-zinc-800 text-zinc-300 rounded text-xs font-mono border border-zinc-700">Web (8080)</button>
                        <button onclick="setCheckPortPreset(3389)" class="px-2.5 py-1.5 bg-zinc-800 text-zinc-300 rounded text-xs font-mono border border-zinc-700">RDP (3389)</button>
                        <button onclick="runExternalPortCheck()" id="checkPortBtn" 
                                class="px-4 py-1.5 bg-zinc-100 hover:bg-white text-zinc-950 text-xs font-medium rounded transition" data-i18n="btn_check_port">
                            Проверить из Интернета
                        </button>
                    </div>
                </div>

                <div id="checkPortResult" class="hidden p-3 rounded border text-xs font-mono"></div>
            </div>
        </section>

        <!-- TAB 2: АВТО-ПРОБРОС ПОРТОВ (UPNP) -->
        <section id="tabContent-upnp" class="hidden space-y-6">
            <div class="border border-border bg-[#121215] rounded-lg p-5 space-y-4">
                <div>
                    <h2 class="text-sm font-semibold text-white tracking-tight" data-i18n="upnp_title">UPnP: Автоматическое открытие портов на роутере</h2>
                    <p class="text-xs text-muted mt-0.5" data-i18n="upnp_desc">
                        Открывайте порты для игр и серверов в 1 клик прямо с компьютера, без необходимости заходить в панель управления роутером (192.168.1.1).
                    </p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3" id="upnpPresetsContainer"></div>
            </div>

            <div class="border border-border bg-[#121215] rounded-lg p-5 space-y-3">
                <h3 class="text-xs font-semibold uppercase tracking-wider text-zinc-300 font-mono" data-i18n="custom_upnp_title">Кастомный проброс порта</h3>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    <div>
                        <label class="block text-[11px] font-mono text-zinc-400 mb-1" data-i18n="port_label">Порт</label>
                        <input type="number" id="customUpnpPort" value="8080" 
                               class="w-full bg-zinc-900 border border-zinc-700/80 rounded px-3 py-1.5 text-xs text-zinc-100 font-mono focus:outline-none focus:border-zinc-500">
                    </div>
                    <div>
                        <label class="block text-[11px] font-mono text-zinc-400 mb-1" data-i18n="proto_label">Протокол</label>
                        <select id="customUpnpProto" class="w-full bg-zinc-900 border border-zinc-700/80 rounded px-3 py-1.5 text-xs text-zinc-100 font-mono focus:outline-none focus:border-zinc-500">
                            <option value="TCP">TCP</option>
                            <option value="UDP">UDP</option>
                        </select>
                    </div>
                    <div class="flex items-end">
                        <button onclick="triggerCustomUpnp()" class="w-full py-1.5 bg-zinc-100 hover:bg-white text-zinc-950 text-xs font-medium rounded transition" data-i18n="btn_forward_upnp">
                            Открыть порт через UPnP
                        </button>
                    </div>
                </div>

                <div id="upnpStatusBox" class="hidden p-3 rounded border text-xs font-mono"></div>
            </div>
        </section>

        <!-- TAB 3: БАЗА ЗНАНИЙ: КАК ПОЛУЧИТЬ БЕЛЫЙ IP / ОБХОД -->
        <section id="tabContent-guide" class="hidden space-y-6">
            <div class="border border-border bg-[#121215] rounded-lg p-5 space-y-3">
                <div class="flex items-center justify-between">
                    <h3 class="text-sm font-semibold text-white" data-i18n="guide_1_title">1. Как заказать Белый (Статический) IP у вашего провайдера</h3>
                    <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20" data-i18n="badge_best">Лучший вариант</span>
                </div>
                <p class="text-xs text-zinc-400 leading-relaxed" data-i18n="guide_1_desc">
                    Белый IP позволяет подключаться к вашему ПК напрямую по IP-адресу без задержек и сторонних посредников. Стоимость у большинства провайдеров составляет от 100 до 150 рублей в месяц.
                </p>
                <div class="p-3.5 rounded bg-zinc-900 border border-zinc-800 space-y-2 text-xs font-mono text-zinc-300">
                    <div class="text-zinc-200 font-semibold" data-i18n="guide_1_template_title">Готовый шаблон для техподдержки вашего провайдера:</div>
                    <div class="bg-black/50 p-2.5 rounded border border-zinc-800 text-sky-300 select-all" data-i18n="guide_1_template_text">
                        «Здравствуйте! Мне необходимо подключить услугу "Статический белый IP-адрес" (публичный IPv4) на моём договоре для хостинга игрового сервера и удаленного доступа. Подключите, пожалуйста.»
                    </div>
                </div>
            </div>

            <div class="border border-border bg-[#121215] rounded-lg p-5 space-y-3">
                <div class="flex items-center justify-between">
                    <h3 class="text-sm font-semibold text-white" data-i18n="guide_2_title">2. Бесплатные способы открыть доступ, если у вас Серый IP (CGNAT)</h3>
                    <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-sky-500/10 text-sky-400 border border-sky-500/20" data-i18n="badge_free">Без доплат</span>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-1 text-xs">
                    <div class="p-3.5 rounded bg-zinc-900 border border-zinc-800 space-y-2">
                        <div class="font-semibold text-white font-mono flex items-center justify-between">
                            <span>Playit.gg</span>
                            <span class="text-[10px] text-emerald-400" data-i18n="tag_gaming">Для игр</span>
                        </div>
                        <p class="text-[11px] text-zinc-400 leading-relaxed" data-i18n="playit_desc">
                            Идеально для Minecraft, CS2, Palworld. Дает постоянный публичный адрес без белого IP и без роутера.
                        </p>
                        <a href="https://playit.gg/" target="_blank" class="inline-block text-[11px] text-sky-400 hover:underline font-mono">playit.gg &rarr;</a>
                    </div>

                    <div class="p-3.5 rounded bg-zinc-900 border border-zinc-800 space-y-2">
                        <div class="font-semibold text-white font-mono flex items-center justify-between">
                            <span>Cloudflare Tunnels</span>
                            <span class="text-[10px] text-sky-400" data-i18n="tag_web">Для сайтов</span>
                        </div>
                        <p class="text-[11px] text-zinc-400 leading-relaxed" data-i18n="cf_desc">
                            Бесплатный инструмент Cloudflare. Пробрасывает локальный порт на домен без белого IP и с защитой от DDoS.
                        </p>
                        <a href="https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/" target="_blank" class="inline-block text-[11px] text-sky-400 hover:underline font-mono">Cloudflare Tunnels &rarr;</a>
                    </div>

                    <div class="p-3.5 rounded bg-zinc-900 border border-zinc-800 space-y-2">
                        <div class="font-semibold text-white font-mono flex items-center justify-between">
                            <span>Tailscale</span>
                            <span class="text-[10px] text-indigo-400" data-i18n="tag_vpn">Для RDP и друзей</span>
                        </div>
                        <p class="text-[11px] text-zinc-400 leading-relaxed" data-i18n="tailscale_desc">
                            Создает защищенную виртуальную локальную сеть на базе WireGuard для подключения к ПК откуда угодно.
                        </p>
                        <a href="https://tailscale.com/" target="_blank" class="inline-block text-[11px] text-sky-400 hover:underline font-mono">Tailscale &rarr;</a>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 4: ЗАПУСК ПРИЛОЖЕНИЙ -->
        <section id="tabContent-apps" class="hidden space-y-4">
            <div>
                <h2 class="text-sm font-semibold text-white tracking-tight" data-i18n="apps_title">Диспетчер процессов и серверов</h2>
                <p class="text-xs text-muted mt-0.5" data-i18n="apps_desc">Быстрый запуск зарегистрированных серверов, ярлыков и утилит на компьютере.</p>
            </div>

            <div id="appsGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"></div>

            <div id="launchToast" class="fixed bottom-6 right-6 hidden bg-zinc-900 border border-zinc-700 p-3 rounded-md shadow-xl z-50 text-xs flex items-center space-x-2.5 font-mono">
                <span class="w-2 h-2 rounded-full bg-sky-400 animate-pulse"></span>
                <span id="launchToastMsg" class="text-zinc-200">...</span>
            </div>
        </section>

        <!-- TAB 5: НАСТРОЙКИ -->
        <section id="tabContent-settings" class="hidden space-y-4">
            <div class="border border-border bg-[#121215] rounded-lg p-5 space-y-4">
                <div>
                    <h2 class="text-sm font-semibold text-white tracking-tight" data-i18n="oauth_title">Авторизация Google OAuth 2.0</h2>
                    <p class="text-xs text-muted mt-0.5" data-i18n="oauth_desc">Безопасный доступ к панели управления по вашей учетной записи Google.</p>
                </div>

                <div class="space-y-4 text-xs">
                    <div class="p-3.5 rounded bg-zinc-900/60 border border-zinc-800 space-y-2 text-zinc-300">
                        <div class="font-medium text-white" data-i18n="oauth_steps_title">Инструкция по привязке:</div>
                        <ol class="list-decimal list-inside space-y-1 text-zinc-400 font-mono text-[11px]">
                            <li>Google Cloud Console &rarr; APIs & Services &rarr; Credentials &rarr; OAuth 2.0 Client ID.</li>
                            <li>Redirect URI: <code class="bg-black/60 text-zinc-200 px-1.5 py-0.5 rounded border border-zinc-800">http://localhost:8080/auth/callback</code></li>
                            <li>Вставьте <code>client_id</code> и <code>client_secret</code> в <code>config.json</code>.</li>
                            <li>Добавьте ваш Gmail в <code>allowed_emails</code>.</li>
                        </ol>
                    </div>

                    <div>
                        <div class="text-[11px] font-mono uppercase tracking-wider text-zinc-400 mb-2" data-i18n="allowed_emails_title">Разрешенные адреса:</div>
                        <div id="allowedEmailsList" class="flex flex-wrap gap-1.5"></div>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="border-t border-border py-4 mt-8 bg-[#09090b] text-center text-[11px] text-zinc-500 font-mono">
        NetHub Windows 11 Network Toolkit &bull; White IP Diagnostics &bull; UPnP Controller
    </footer>

    <!-- Client Script with i18n Dictionary -->
    <script>
        let currentLang = 'ru';
        let currentAnalysisData = null;

        const DICT = {
            ru: {
                tab_analysis: "Анализ: Белый или Серый IP",
                tab_upnp: "UPnP: Авто-проброс портов",
                tab_guide: "Как получить Белый IP / Обход",
                tab_apps: "Запуск серверов и программ",
                tab_settings: "Настройки и OAuth",
                your_public_ip: "Ваш публичный адрес",
                diagnosing: "Выполняется диагностика...",
                isp_label: "Провайдер (ISP)",
                asn_label: "Автономная система (AS)",
                loc_label: "Локация",
                route_label: "Маршрутизация",
                wan_check_title: "Проверка доступности порта из внешней сети (WAN Reachability)",
                wan_check_desc: "Проверяет, могут ли игроки, друзья или внешние устройства подключиться к вашему порту из Интернета.",
                port_label: "Номер порта",
                proto_label: "Протокол",
                btn_check_port: "Проверить из Интернета",
                upnp_title: "UPnP: Автоматическое открытие портов на роутере",
                upnp_desc: "Открывайте порты для игр и серверов в 1 клик прямо с компьютера, без необходимости заходить в панель управления роутером (192.168.1.1).",
                custom_upnp_title: "Кастомный проброс порта",
                btn_forward_upnp: "Открыть порт через UPnP",
                guide_1_title: "1. Как заказать Белый (Статический) IP у вашего провайдера",
                badge_best: "Лучший вариант",
                guide_1_desc: "Белый IP позволяет подключаться к вашему ПК напрямую по IP-адресу без задержек и сторонних посредников. Стоимость у большинства провайдеров составляет от 100 до 150 рублей в месяц.",
                guide_1_template_title: "Готовый шаблон для техподдержки вашего провайдера:",
                guide_1_template_text: "«Здравствуйте! Мне необходимо подключить услугу \\"Статический белый IP-адрес\\" (публичный IPv4) на моём договоре для хостинга игрового сервера и удаленного доступа. Подключите, пожалуйста.»",
                guide_2_title: "2. Бесплатные способы открыть доступ, если у вас Серый IP (CGNAT)",
                badge_free: "Без доплат",
                tag_gaming: "Для игр",
                playit_desc: "Идеально для Minecraft, CS2, Palworld. Дает постоянный публичный адрес без белого IP и без роутера.",
                tag_web: "Для сайтов",
                cf_desc: "Бесплатный инструмент Cloudflare. Пробрасывает локальный порт на домен без белого IP и с защитой от DDoS.",
                tag_vpn: "Для RDP и друзей",
                tailscale_desc: "Создает защищенную виртуальную локальную сеть на базе WireGuard для подключения к ПК откуда угодно.",
                apps_title: "Диспетчер процессов и серверов",
                apps_desc: "Быстрый запуск зарегистрированных серверов, ярлыков и утилит на компьютере.",
                oauth_title: "Авторизация Google OAuth 2.0",
                oauth_desc: "Безопасный доступ к панели управления по вашей учетной записи Google.",
                oauth_steps_title: "Инструкция по привязке:",
                allowed_emails_title: "Разрешенные адреса:",
                dev_notice: "Режим отладки: Google OAuth не настроен в config.json. Доступ к панели открыт локально."
            },
            en: {
                tab_analysis: "White vs Gray IP Inspector",
                tab_upnp: "UPnP Port Forwarder",
                tab_guide: "White IP Guide & Bypass",
                tab_apps: "Server & Process Dispatcher",
                tab_settings: "OAuth Settings",
                your_public_ip: "Public Gateway IP",
                diagnosing: "Running network diagnostics...",
                isp_label: "Provider (ISP)",
                asn_label: "Autonomous System (AS)",
                loc_label: "Location",
                route_label: "Routing Mode",
                wan_check_title: "External Port Reachability Diagnostic (WAN)",
                wan_check_desc: "Verifies whether external clients and game players can reach your open port from the public Internet.",
                port_label: "Port Number",
                proto_label: "Protocol",
                btn_check_port: "Probe from Internet",
                upnp_title: "UPnP: Automated Router Port Mapping",
                upnp_desc: "Forward ports for game servers in 1 click directly from your PC without entering router admin panel (192.168.1.1).",
                custom_upnp_title: "Custom Port Forwarding",
                btn_forward_upnp: "Forward via UPnP",
                guide_1_title: "1. How to Request a White (Static) IP from your ISP",
                badge_best: "Recommended",
                guide_1_desc: "A White IP allows direct WAN connectivity without third-party proxies. Typically costs around $1-2/mo from major telecommunication providers.",
                guide_1_template_title: "Support Request Template:",
                guide_1_template_text: "“Hello, I would like to enable the Static Public IPv4 address service on my account for dedicated game server hosting and remote access.”",
                guide_2_title: "2. Free Alternatives if you have a Gray IP (CGNAT)",
                badge_free: "Zero Cost",
                tag_gaming: "Gaming",
                playit_desc: "Ideal for Minecraft, CS2, Palworld. Grants a persistent domain tunnel with zero port-forwarding required.",
                tag_web: "Web / API",
                cf_desc: "Cloudflare Tunnels expose your local HTTP services to your domain with complimentary enterprise DDoS protection.",
                tag_vpn: "RDP & Friends",
                tailscale_desc: "Peer-to-peer WireGuard mesh VPN for connecting friend groups and remote desktop securely.",
                apps_title: "Process & Server Dispatcher",
                apps_desc: "One-click execution of dedicated server binaries and scripts configured in config.json.",
                oauth_title: "Google OAuth 2.0 Identity Gating",
                oauth_desc: "Secures this local control plane with cryptographic email authorization.",
                oauth_steps_title: "Provisioning Steps:",
                allowed_emails_title: "Authorized Email Accounts:",
                dev_notice: "Notice: Development mode active. Google OAuth bypassed until client_id is configured."
            }
        };

        function setLanguage(lang) {
            currentLang = lang;
            localStorage.setItem('nethub_lang', lang);
            document.getElementById('langBtn').textContent = lang.toUpperCase();

            // Update all data-i18n elements
            document.querySelectorAll('[data-i18n]').forEach(el => {
                const key = el.getAttribute('data-i18n');
                if (DICT[lang] && DICT[lang][key]) {
                    el.textContent = DICT[lang][key];
                }
            });

            // Re-render analysis verdict if present
            if (currentAnalysisData) renderVerdict(currentAnalysisData);
        }

        function toggleLang() {
            setLanguage(currentLang === 'ru' ? 'en' : 'ru');
        }

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
                // Detect System Language
                const stored = localStorage.getItem('nethub_lang');
                if (stored) {
                    setLanguage(stored);
                } else {
                    const langRes = await fetch('/api/system-lang');
                    const langData = await langRes.json();
                    setLanguage(langData.lang || 'en');
                }

                // Auth Status
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
                        <a href="/auth/logout" class="text-xs text-zinc-400 hover:text-zinc-200 transition font-mono ml-2">Logout</a>
                    `;
                } else {
                    container.innerHTML = `
                        <a href="/auth/login" class="px-2.5 py-1 bg-zinc-100 hover:bg-white text-zinc-950 text-xs font-medium rounded transition">
                            Login
                        </a>
                    `;
                }

                const emailContainer = document.getElementById('allowedEmailsList');
                if (authData.allowed_emails && authData.allowed_emails.length > 0) {
                    emailContainer.innerHTML = authData.allowed_emails.map(e => `
                        <span class="px-2 py-0.5 bg-zinc-900 text-zinc-300 rounded font-mono text-[11px] border border-zinc-800">${e}</span>
                    `).join('');
                } else {
                    emailContainer.innerHTML = '<span class="text-xs text-zinc-500 font-mono">No whitelist configured</span>';
                }

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
                document.getElementById('analysisRoute').textContent = data.is_white 
                    ? (currentLang === 'ru' ? 'Прямой маршрут' : 'Direct Path')
                    : (currentLang === 'ru' ? 'Через CGNAT' : 'Behind CGNAT');

                renderVerdict(data);
            } catch (err) {
                console.error("IP analysis error:", err);
            }
        }

        function renderVerdict(data) {
            const badgeContainer = document.getElementById('ipTypeBadgeContainer');
            const verdictBox = document.getElementById('ipVerdictBox');
            const verdictTitle = document.getElementById('ipVerdictTitle');
            const verdictDesc = document.getElementById('ipVerdictDesc');
            const dot = document.getElementById('ipStatusDot');

            if (data.is_white) {
                dot.className = "w-2 h-2 rounded-full bg-emerald-400";
                badgeContainer.innerHTML = `
                    <span class="inline-flex items-center px-3 py-1 rounded text-xs font-mono font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                        ${currentLang === 'ru' ? 'БЕЛЫЙ (ПУБЛИЧНЫЙ) IP' : 'WHITE (PUBLIC) IP'}
                    </span>
                `;
                verdictBox.className = "p-4 rounded bg-emerald-950/20 border border-emerald-500/30 text-xs space-y-2";
                verdictTitle.className = "font-bold text-sm text-emerald-300";
                verdictTitle.textContent = currentLang === 'ru' 
                    ? "У вас Белый (Публичный) IP-адрес!"
                    : "White (Public) IP Address Confirmed!";
                verdictDesc.className = "text-zinc-300 leading-relaxed";
                verdictDesc.textContent = currentLang === 'ru'
                    ? "Ваш компьютер доступен напрямую из глобальной сети Интернет. Вы можете открывать порты через вкладку UPnP, хостить игровые серверы (Minecraft, CS2, Palworld) и использовать RDP без сторонних туннелей."
                    : "Your PC is directly routable from the public Internet. You can open ports via the UPnP tab, host game servers (Minecraft, CS2, Palworld), and use RDP without third-party proxies.";
            } else if (data.is_cgnat) {
                dot.className = "w-2 h-2 rounded-full bg-amber-400";
                badgeContainer.innerHTML = `
                    <span class="inline-flex items-center px-3 py-1 rounded text-xs font-mono font-bold bg-amber-500/10 text-amber-400 border border-amber-500/30">
                        ${currentLang === 'ru' ? 'СЕРЫЙ IP (CGNAT)' : 'GRAY IP (CGNAT)'}
                    </span>
                `;
                verdictBox.className = "p-4 rounded bg-amber-950/20 border border-amber-500/30 text-xs space-y-2";
                verdictTitle.className = "font-bold text-sm text-amber-300";
                verdictTitle.textContent = currentLang === 'ru'
                    ? "Ваш IP находится за CGNAT провайдера (Серый IP)"
                    : "Your host is behind Carrier-Grade NAT (CGNAT)";
                verdictDesc.className = "text-zinc-300 leading-relaxed";
                verdictDesc.textContent = currentLang === 'ru'
                    ? "Провайдер заблокировал прямой входящий трафик. Перейдите во вкладку «Как получить Белый IP / Обход», чтобы узнать, как подключить Playit.gg или запросить белый IP."
                    : "Your ISP blocks direct inbound connections. Check the 'White IP Guide & Bypass' tab to use Playit.gg or request a static white IP from your ISP.";
            } else {
                dot.className = "w-2 h-2 rounded-full bg-sky-400";
                badgeContainer.innerHTML = `
                    <span class="inline-flex items-center px-3 py-1 rounded text-xs font-mono font-bold bg-sky-500/10 text-sky-400 border border-sky-500/30">
                        ${currentLang === 'ru' ? 'ПУБЛИЧНЫЙ МАРШРУТ' : 'PUBLIC ROUTE'}
                    </span>
                `;
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
            btn.textContent = currentLang === 'ru' ? "Проверка..." : "Probing...";
            card.classList.remove('hidden');
            card.className = "p-3 rounded bg-zinc-900 border border-zinc-800 text-zinc-400 text-xs font-mono";
            card.textContent = currentLang === 'ru'
                ? `Запрос к внешнему сканеру для порта ${port}...`
                : `Querying external WAN probe for port ${port}...`;

            try {
                const res = await fetch('/api/check-port', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({port: port})
                });
                const data = await res.json();

                if (data.is_open) {
                    card.className = "p-3 rounded bg-zinc-900 border border-emerald-500/40 text-emerald-400 text-xs font-mono";
                    card.innerHTML = currentLang === 'ru'
                        ? `<b>УСПЕХ:</b> Порт ${data.port} ОТКРЫТ и доступен из Интернета! Адрес: <code>${currentAnalysisData?.ip || ''}:${data.port}</code>`
                        : `<b>SUCCESS:</b> Port ${data.port} is OPEN and reachable from WAN! Address: <code>${currentAnalysisData?.ip || ''}:${data.port}</code>`;
                } else {
                    card.className = "p-3 rounded bg-zinc-900 border border-amber-500/40 text-amber-300 text-xs font-mono";
                    card.innerHTML = currentLang === 'ru'
                        ? `<b>ЗАКРЫТ:</b> Порт ${data.port} не отвечает из внешней сети. Откройте его во вкладке <b>UPnP</b>.`
                        : `<b>CLOSED:</b> Port ${data.port} is not responding externally. Forward it in the <b>UPnP</b> tab.`;
                }
            } catch (err) {
                card.className = "p-3 rounded bg-zinc-900 border border-red-500/40 text-red-400 text-xs font-mono";
                card.textContent = "Error: " + err;
            } finally {
                btn.disabled = false;
                btn.textContent = currentLang === 'ru' ? "Проверить из Интернета" : "Probe from Internet";
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
                            ${currentLang === 'ru' ? 'Открыть порт ' + p.port : 'Forward Port ' + p.port}
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
            box.textContent = currentLang === 'ru' 
                ? `Отправка UPnP команды на роутер для ${name} (${port} ${protocol})...`
                : `Dispatching UPnP mapping request for ${name} (${port} ${protocol})...`;

            try {
                const res = await fetch('/api/upnp-forward', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({port: port, protocol: protocol, description: name})
                });
                const data = await res.json();

                if (data.success) {
                    box.className = "p-3 rounded bg-zinc-900 border border-emerald-500/40 text-emerald-400 text-xs font-mono";
                    box.innerHTML = `<b>OK:</b> ${data.message}`;
                } else {
                    box.className = "p-3 rounded bg-zinc-900 border border-red-500/40 text-red-400 text-xs font-mono";
                    box.innerHTML = `<b>ERR:</b> ${data.error}`;
                }
            } catch (err) {
                box.className = "p-3 rounded bg-zinc-900 border border-red-500/40 text-red-400 text-xs font-mono";
                box.textContent = "Error: " + err;
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
            grid.innerHTML = '<div class="col-span-full text-center text-zinc-500 text-xs py-6 font-mono">Loading processes...</div>';

            try {
                const res = await fetch('/api/apps');
                const apps = await res.json();

                if (apps.length === 0) {
                    grid.innerHTML = '<div class="col-span-full text-center text-zinc-500 text-xs py-6 font-mono">No processes configured</div>';
                    return;
                }

                grid.innerHTML = apps.map(app => `
                    <div class="border border-border bg-[#121215] rounded-md p-4 flex flex-col justify-between space-y-3 hover:border-zinc-700 transition">
                        <div>
                            <div class="flex items-center justify-between mb-1.5">
                                <h3 class="font-medium text-white text-xs">${app.name}</h3>
                                <span class="text-[10px] font-mono uppercase px-1 rounded bg-zinc-900 border border-zinc-800 text-zinc-400">Process</span>
                            </div>
                            <p class="text-[11px] text-zinc-400 mb-2">${app.description || 'Target Application'}</p>
                            <div class="text-[10px] font-mono text-zinc-500 truncate" title="${app.path}">Path: ${app.path}</div>
                        </div>

                        <button onclick="launchApp('${app.id}')" 
                                class="w-full py-1.5 px-3 bg-zinc-900 hover:bg-zinc-800 text-zinc-200 text-xs font-mono font-medium rounded border border-zinc-700 transition flex items-center justify-center space-x-1.5">
                            <span>${currentLang === 'ru' ? 'Запустить' : 'Execute'}</span>
                            <span class="text-zinc-500">&rarr;</span>
                        </button>
                    </div>
                `).join('');

            } catch (err) {
                grid.innerHTML = `<div class="col-span-full text-center text-red-400 text-xs py-6 font-mono">Error: ${err}</div>`;
            }
        }

        async function launchApp(appId) {
            const toast = document.getElementById('launchToast');
            const msg = document.getElementById('launchToastMsg');

            toast.classList.remove('hidden');
            msg.textContent = currentLang === 'ru' ? `Запуск ${appId}...` : `Executing ${appId}...`;

            try {
                const res = await fetch(`/api/launch/${appId}`, { method: 'POST' });
                const data = await res.json();

                if (data.success) {
                    msg.textContent = `OK: ${data.message}`;
                } else {
                    msg.textContent = `ERR: ${data.error}`;
                }
            } catch (err) {
                msg.textContent = `Error: ${err}`;
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
