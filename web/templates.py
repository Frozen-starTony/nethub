INDEX_HTML = """<!DOCTYPE html>
<html lang="ru" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NetHub // Панель управления</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        darkbg: '#0B0F19',
                        darkcard: '#111827',
                        accent: '#06B6D4',
                        accentHover: '#0891B2'
                    }
                }
            }
        }
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap');
        body {
            font-family: 'Inter', sans-serif;
            background-color: #0B0F19;
        }
        .code-font {
            font-family: 'JetBrains Mono', monospace;
        }
    </style>
</head>
<body class="text-slate-200 min-h-screen flex flex-col antialiased">

    <!-- Верхний навбар -->
    <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="w-9 h-9 rounded-lg bg-cyan-500/20 border border-cyan-500/40 flex items-center justify-center text-cyan-400 font-bold text-xl code-font">
                    ⚡
                </div>
                <div>
                    <span class="text-xl font-bold tracking-tight text-white">Net<span class="text-cyan-400">Hub</span></span>
                    <span class="ml-2 text-xs uppercase px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 code-font">Win11 Hybrid</span>
                </div>
            </div>

            <!-- Внешний IP & Статус пользователя -->
            <div class="flex items-center space-x-4">
                <div class="hidden sm:flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700/60 text-xs code-font">
                    <span class="text-slate-400">Внешний IP:</span>
                    <span id="externalIpBadge" class="text-cyan-400 font-bold">Определение...</span>
                </div>

                <div id="authStatusContainer" class="flex items-center space-x-3">
                    <!-- Заполняется JS -->
                </div>
            </div>
        </div>
    </header>

    <!-- Баннер режима отладки / Google OAuth -->
    <div id="devModeNotice" class="hidden bg-amber-500/10 border-b border-amber-500/30 px-4 py-2 text-xs text-amber-300 text-center">
        ⚡ <b>Режим быстрой настройки:</b> Google Client ID не задан в <code class="bg-amber-950/60 px-1 py-0.5 rounded">config.json</code>. Доступ открыт в режиме администратора для локальной отладки.
    </div>

    <!-- Основной контент -->
    <main class="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
        <!-- Навигационные вкладки -->
        <div class="flex space-x-2 border-b border-slate-800 mb-8 pb-3 overflow-x-auto">
            <button onclick="switchTab('scanner')" id="tabBtn-scanner" class="tab-btn px-4 py-2 rounded-lg text-sm font-medium transition bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
                🔍 Сканер и Пинг
            </button>
            <button onclick="switchTab('interfaces')" id="tabBtn-interfaces" class="tab-btn px-4 py-2 rounded-lg text-sm font-medium transition text-slate-400 hover:text-white hover:bg-slate-800/50">
                🌐 Сетевые интерфейсы
            </button>
            <button onclick="switchTab('apps')" id="tabBtn-apps" class="tab-btn px-4 py-2 rounded-lg text-sm font-medium transition text-slate-400 hover:text-white hover:bg-slate-800/50">
                🚀 Запуск приложений
            </button>
            <button onclick="switchTab('settings')" id="tabBtn-settings" class="tab-btn px-4 py-2 rounded-lg text-sm font-medium transition text-slate-400 hover:text-white hover:bg-slate-800/50">
                ⚙️ Настройки и OAuth
            </button>
        </div>

        <!-- ВКЛАДКА 1: СКАНЕР И ПИНГ -->
        <section id="tabContent-scanner" class="space-y-8">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <!-- Блок Пинга -->
                <div class="bg-slate-900/60 border border-slate-800 rounded-xl p-6 shadow-xl backdrop-blur">
                    <h3 class="text-lg font-semibold text-white mb-2 flex items-center">
                        <span class="mr-2 text-cyan-400">📡</span> Проверка доступности хоста (Ping)
                    </h3>
                    <p class="text-sm text-slate-400 mb-4">Отправка сетевых запросов и замер задержки отклика сервера.</p>

                    <div class="space-y-4">
                        <div>
                            <label class="block text-xs font-medium text-slate-300 mb-1">IP-адрес или домен</label>
                            <div class="flex space-x-2">
                                <input type="text" id="pingHostInput" value="8.8.8.8" placeholder="например, google.com или 192.168.1.1" 
                                       class="flex-1 bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm text-white code-font focus:outline-none focus:border-cyan-500">
                                <button onclick="runPing()" id="pingBtn" 
                                        class="px-5 py-2 bg-cyan-600 hover:bg-cyan-500 text-white text-sm font-medium rounded-lg transition shadow-lg shadow-cyan-600/20">
                                    Ping
                                </button>
                            </div>
                        </div>

                        <!-- Результат Пинга -->
                        <div id="pingResultCard" class="hidden p-4 rounded-lg border text-sm code-font transition-all">
                            <!-- Заполняется JS -->
                        </div>
                    </div>
                </div>

                <!-- Блок Сканера Портов -->
                <div class="bg-slate-900/60 border border-slate-800 rounded-xl p-6 shadow-xl backdrop-blur">
                    <h3 class="text-lg font-semibold text-white mb-2 flex items-center">
                        <span class="mr-2 text-cyan-400">🔌</span> Асинхронный сканер TCP портов
                    </h3>
                    <p class="text-sm text-slate-400 mb-4">Параллельная проверка открытых портов на базе asyncio.</p>

                    <div class="space-y-4">
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div>
                                <label class="block text-xs font-medium text-slate-300 mb-1">Целевой хост</label>
                                <input type="text" id="scanHostInput" value="127.0.0.1" placeholder="IP или домен" 
                                       class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm text-white code-font focus:outline-none focus:border-cyan-500">
                            </div>
                            <div>
                                <label class="block text-xs font-medium text-slate-300 mb-1">Порты (диапазон / список)</label>
                                <input type="text" id="scanPortsInput" value="20-1000" placeholder="Пример: 80,443,8080 или 1-500" 
                                       class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm text-white code-font focus:outline-none focus:border-cyan-500">
                            </div>
                        </div>

                        <div class="flex items-center justify-between pt-2">
                            <div class="flex space-x-2">
                                <button onclick="setPresetPorts('top20')" class="text-xs px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300">Топ 20</button>
                                <button onclick="setPresetPorts('web')" class="text-xs px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300">Web (80,443,8080...)</button>
                                <button onclick="setPresetPorts('range1k')" class="text-xs px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300">1 - 1024</button>
                            </div>
                            <button onclick="runPortScan()" id="scanBtn" 
                                    class="px-5 py-2 bg-cyan-600 hover:bg-cyan-500 text-white text-sm font-medium rounded-lg transition shadow-lg shadow-cyan-600/20">
                                Сканировать
                            </button>
                        </div>

                        <!-- Результат сканирования -->
                        <div id="scanResultCard" class="hidden p-4 rounded-lg bg-slate-800/60 border border-slate-700/80 text-sm code-font">
                            <!-- Заполняется JS -->
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- ВКЛАДКА 2: СЕТЕВЫЕ ИНТЕРФЕЙСЫ -->
        <section id="tabContent-interfaces" class="hidden space-y-6">
            <div class="flex justify-between items-center">
                <div>
                    <h3 class="text-lg font-semibold text-white">Адаптеры и интерфейсы Windows</h3>
                    <p class="text-sm text-slate-400">Информация о физических и виртуальных сетевых картах системы.</p>
                </div>
                <button onclick="loadInterfaces()" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs rounded-lg border border-slate-700 transition">
                    🔄 Обновить список
                </button>
            </div>

            <div id="interfacesGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <!-- Карточки интерфейсов рендерятся через JS -->
            </div>
        </section>

        <!-- ВКЛАДКА 3: ЗАПУСК ПРИЛОЖЕНИЙ -->
        <section id="tabContent-apps" class="hidden space-y-6">
            <div>
                <h3 class="text-lg font-semibold text-white">Менеджер процессов и ярлыков</h3>
                <p class="text-sm text-slate-400">Безопасный удаленный запуск программ и .lnk ярлыков на хосте Windows 11.</p>
            </div>

            <div id="appsGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                <!-- Карточки приложений -->
            </div>

            <!-- Уведомление о запуске -->
            <div id="launchToast" class="fixed bottom-6 right-6 hidden bg-slate-900 border border-cyan-500/50 p-4 rounded-xl shadow-2xl z-50 text-sm flex items-center space-x-3">
                <span class="text-cyan-400 text-xl">🚀</span>
                <span id="launchToastMsg" class="text-white font-medium">Приложение запускается...</span>
            </div>
        </section>

        <!-- ВКЛАДКА 4: НАСТРОЙКИ И GOOGLE OAUTH -->
        <section id="tabContent-settings" class="hidden space-y-6">
            <div class="bg-slate-900/60 border border-slate-800 rounded-xl p-6 shadow-xl">
                <h3 class="text-lg font-semibold text-white mb-2">Настройка Google OAuth 2.0</h3>
                <p class="text-sm text-slate-400 mb-6">Инструкция по защите панели управления учетной записью Google.</p>

                <div class="space-y-4 text-sm text-slate-300">
                    <div class="p-4 rounded-lg bg-slate-800/60 border border-slate-700/60 space-y-2">
                        <div class="font-semibold text-white">Шаги подключения:</div>
                        <ol class="list-decimal list-inside space-y-1 text-slate-400 text-xs sm:text-sm">
                            <li>Перейдите в <a href="https://console.cloud.google.com/" target="_blank" class="text-cyan-400 underline">Google Cloud Console</a> и создайте проект.</li>
                            <li>В разделе <b>APIs & Services -> Credentials</b> создайте <b>OAuth 2.0 Client ID</b> (Web application).</li>
                            <li>Укажите <b>Authorized redirect URI</b>: <code class="bg-slate-900 text-cyan-300 px-2 py-0.5 rounded" id="cfgRedirectUri">http://localhost:8080/auth/callback</code></li>
                            <li>Скопируйте <code>client_id</code> и <code>client_secret</code> в файл <code class="text-cyan-400">config.json</code> в корне утилиты.</li>
                            <li>Добавьте ваш Gmail в массив <code class="text-cyan-400">allowed_emails</code>.</li>
                        </ol>
                    </div>

                    <div class="pt-4">
                        <h4 class="font-medium text-white mb-2">Разрешенные Email-адреса (Белый список):</h4>
                        <div id="allowedEmailsList" class="flex flex-wrap gap-2">
                            <!-- Заполняется JS -->
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <!-- Подвал -->
    <footer class="border-t border-slate-800 py-6 mt-12 bg-slate-900/40 text-center text-xs text-slate-500">
        NetHub Windows 11 Network Toolkit • FastAPI + AsyncIO • Self-Hosted Edition
    </footer>

    <!-- Скрипты фронтенда -->
    <script>
        // Переключение табов
        function switchTab(tabId) {
            document.querySelectorAll('[id^="tabContent-"]').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.className = "tab-btn px-4 py-2 rounded-lg text-sm font-medium transition text-slate-400 hover:text-white hover:bg-slate-800/50";
            });

            const content = document.getElementById(`tabContent-${tabId}`);
            const btn = document.getElementById(`tabBtn-${tabId}`);
            if (content) content.classList.remove('hidden');
            if (btn) btn.className = "tab-btn px-4 py-2 rounded-lg text-sm font-medium transition bg-cyan-500/10 text-cyan-400 border border-cyan-500/30";

            if (tabId === 'interfaces') loadInterfaces();
            if (tabId === 'apps') loadApps();
        }

        // Пресеты портов
        function setPresetPorts(preset) {
            const input = document.getElementById('scanPortsInput');
            if (preset === 'top20') input.value = "21,22,23,25,53,80,110,135,139,143,443,445,993,995,1433,3306,3389,5432,8000,8080";
            if (preset === 'web') input.value = "80,443,3000,5000,8000,8080,8443,8888,9000";
            if (preset === 'range1k') input.value = "1-1024";
        }

        // Загрузка начальных данных
        async function initData() {
            try {
                // Статус авторизации
                const authRes = await fetch('/auth/status');
                const authData = await authRes.json();
                
                const container = document.getElementById('authStatusContainer');
                if (authData.dev_mode) {
                    document.getElementById('devModeNotice').classList.remove('hidden');
                    container.innerHTML = `
                        <span class="text-xs text-amber-400 bg-amber-500/10 border border-amber-500/20 px-2.5 py-1 rounded-lg">
                            Admin (Dev Mode)
                        </span>
                    `;
                } else if (authData.authenticated) {
                    container.innerHTML = `
                        <span class="text-xs text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-1 rounded-lg">
                            👤 ${authData.user}
                        </span>
                        <a href="/auth/logout" class="text-xs text-slate-400 hover:text-red-400">Выход</a>
                    `;
                } else {
                    container.innerHTML = `
                        <a href="/auth/login" class="px-3 py-1.5 bg-red-600/80 hover:bg-red-500 text-white text-xs font-semibold rounded-lg transition flex items-center space-x-1.5">
                            <span>Войти через Google</span>
                        </a>
                    `;
                }

                // Внешний IP
                const ipRes = await fetch('/api/ip');
                const ipData = await ipRes.json();
                document.getElementById('externalIpBadge').textContent = ipData.ip || 'Недоступен';

                // Настройки email
                const emailContainer = document.getElementById('allowedEmailsList');
                if (authData.allowed_emails && authData.allowed_emails.length > 0) {
                    emailContainer.innerHTML = authData.allowed_emails.map(e => `
                        <span class="px-2.5 py-1 bg-slate-800 text-cyan-300 rounded text-xs border border-slate-700">${e}</span>
                    `).join('');
                } else {
                    emailContainer.innerHTML = '<span class="text-xs text-slate-500">Список пуст</span>';
                }

            } catch (err) {
                console.error("Ошибка инициализации:", err);
            }
        }

        // Пинг
        async function runPing() {
            const host = document.getElementById('pingHostInput').value.trim();
            const btn = document.getElementById('pingBtn');
            const card = document.getElementById('pingResultCard');

            if (!host) return;

            btn.disabled = true;
            btn.textContent = "Проверка...";
            card.classList.remove('hidden');
            card.className = "p-4 rounded-lg bg-slate-800/40 border border-slate-700 text-slate-300 text-xs code-font";
            card.innerHTML = "⏳ Отправка пакетов...";

            try {
                const res = await fetch('/api/ping', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({host: host})
                });
                const data = await res.json();

                if (data.alive) {
                    card.className = "p-4 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs code-font";
                    card.innerHTML = `
                        <div class="font-bold flex items-center justify-between">
                            <span>✓ Хост ${data.host} ДОСТУПЕН</span>
                            <span>Задержка: ${data.latency_ms !== null ? data.latency_ms + ' ms' : '< 1 ms'}</span>
                        </div>
                    `;
                } else {
                    card.className = "p-4 rounded-lg bg-red-500/10 border border-red-500/30 text-red-300 text-xs code-font";
                    card.innerHTML = `✗ Хост ${data.host} НЕДОСТУПЕН (${data.error || 'Таймаут'})`;
                }
            } catch (err) {
                card.className = "p-4 rounded-lg bg-red-500/10 border border-red-500/30 text-red-300 text-xs code-font";
                card.textContent = "Ошибка выполнения запроса: " + err;
            } finally {
                btn.disabled = false;
                btn.textContent = "Ping";
            }
        }

        // Сканирование портов
        async function runPortScan() {
            const host = document.getElementById('scanHostInput').value.trim();
            const portsVal = document.getElementById('scanPortsInput').value.trim();
            const btn = document.getElementById('scanBtn');
            const card = document.getElementById('scanResultCard');

            if (!host) return;

            btn.disabled = true;
            btn.textContent = "Сканирую...";
            card.classList.remove('hidden');
            card.innerHTML = "⏳ Асинхронное сканирование портов... Пожалуйста, подождите...";

            try {
                const res = await fetch('/api/scan', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({host: host, ports_str: portsVal})
                });
                const data = await res.json();

                if (data.error) {
                    card.innerHTML = `<span class="text-red-400">Ошибка: ${data.error}</span>`;
                    return;
                }

                let html = `
                    <div class="border-b border-slate-700/80 pb-2 mb-3 flex justify-between items-center">
                        <span class="text-white font-semibold">Хост: ${data.host}</span>
                        <span class="text-xs text-slate-400">Проверено: ${data.scanned_total} | Найдено: ${data.open_count}</span>
                    </div>
                `;

                if (data.open_ports.length > 0) {
                    html += `<div class="flex flex-wrap gap-2">`;
                    data.open_ports.forEach(p => {
                        html += `
                            <span class="px-2.5 py-1 bg-emerald-500/15 border border-emerald-500/40 text-emerald-300 rounded text-xs font-bold">
                                PORT ${p} : OPEN
                            </span>
                        `;
                    });
                    html += `</div>`;
                } else {
                    html += `<p class="text-slate-400 text-xs">Открытых портов не обнаружено.</p>`;
                }

                card.innerHTML = html;
            } catch (err) {
                card.innerHTML = `<span class="text-red-400">Ошибка запроса: ${err}</span>`;
            } finally {
                btn.disabled = false;
                btn.textContent = "Сканировать";
            }
        }

        // Загрузка сетевых интерфейсов
        async function loadInterfaces() {
            const grid = document.getElementById('interfacesGrid');
            grid.innerHTML = '<div class="col-span-full text-center text-slate-500 text-sm py-8">Загрузка адаптеров...</div>';

            try {
                const res = await fetch('/api/interfaces');
                const ifaces = await res.json();

                if (ifaces.length === 0) {
                    grid.innerHTML = '<div class="col-span-full text-center text-slate-500 text-sm">Сетевые интерфейсы не найдены</div>';
                    return;
                }

                grid.innerHTML = ifaces.map(iface => {
                    const statusBadge = iface.is_up 
                        ? '<span class="text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2 py-0.5 rounded">ONLINE</span>'
                        : '<span class="text-xs bg-red-500/10 text-red-400 border border-red-500/20 px-2 py-0.5 rounded">OFFLINE</span>';
                    
                    const ips = iface.ipv4.map(v4 => `<div class="code-font text-cyan-300">${v4.address} <span class="text-slate-500 text-xs">/ ${v4.netmask}</span></div>`).join('') || '<div class="text-slate-500 text-xs">Нет IPv4</div>';

                    return `
                        <div class="bg-slate-900/60 border border-slate-800 rounded-xl p-5 shadow-lg space-y-3">
                            <div class="flex justify-between items-start">
                                <h4 class="font-semibold text-white text-base truncate max-w-[200px]" title="${iface.name}">${iface.name}</h4>
                                ${statusBadge}
                            </div>
                            <div class="text-xs text-slate-400 space-y-1">
                                <div>Скорость: <span class="text-slate-200">${iface.speed_mbps} Mbps</span></div>
                                <div>MAC: <span class="code-font text-slate-300">${iface.mac || 'N/A'}</span></div>
                            </div>
                            <div class="pt-2 border-t border-slate-800 text-xs">
                                <div class="text-slate-400 mb-1">IPv4 Адреса:</div>
                                ${ips}
                            </div>
                        </div>
                    `;
                }).join('');

            } catch (err) {
                grid.innerHTML = `<div class="col-span-full text-center text-red-400 text-sm">Ошибка загрузки: ${err}</div>`;
            }
        }

        // Загрузка приложений
        async function loadApps() {
            const grid = document.getElementById('appsGrid');
            grid.innerHTML = '<div class="col-span-full text-center text-slate-500 text-sm py-8">Загрузка списка программ...</div>';

            try {
                const res = await fetch('/api/apps');
                const apps = await res.json();

                if (apps.length === 0) {
                    grid.innerHTML = '<div class="col-span-full text-center text-slate-500 text-sm">Нет зарегистрированных программ в config.json</div>';
                    return;
                }

                grid.innerHTML = apps.map(app => `
                    <div class="bg-slate-900/60 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col justify-between space-y-4 hover:border-slate-700 transition">
                        <div>
                            <div class="flex items-center space-x-3 mb-2">
                                <span class="text-2xl">💻</span>
                                <h4 class="font-semibold text-white text-base">${app.name}</h4>
                            </div>
                            <p class="text-xs text-slate-400 mb-2">${app.description || 'Ярлык Windows'}</p>
                            <div class="text-xs code-font text-slate-500 truncate" title="${app.path}">Путь: ${app.path}</div>
                        </div>

                        <button onclick="launchApp('${app.id}')" 
                                class="w-full py-2 px-4 bg-slate-800 hover:bg-cyan-600 hover:text-white text-slate-200 text-xs font-medium rounded-lg border border-slate-700 hover:border-cyan-500 transition flex items-center justify-center space-x-2">
                            <span>Запустить</span>
                            <span>▶</span>
                        </button>
                    </div>
                `).join('');

            } catch (err) {
                grid.innerHTML = `<div class="col-span-full text-center text-red-400 text-sm">Ошибка загрузки приложений: ${err}</div>`;
            }
        }

        // Запуск программы
        async function launchApp(appId) {
            const toast = document.getElementById('launchToast');
            const msg = document.getElementById('launchToastMsg');

            toast.classList.remove('hidden');
            msg.textContent = `Запуск ${appId}...`;

            try {
                const res = await fetch(`/api/launch/${appId}`, { method: 'POST' });
                const data = await res.json();

                if (data.success) {
                    msg.textContent = `✓ ${data.message}`;
                } else {
                    msg.textContent = `✗ ${data.error}`;
                }
            } catch (err) {
                msg.textContent = `Ошибка: ${err}`;
            }

            setTimeout(() => {
                toast.classList.add('hidden');
            }, 4500);
        }

        // Старт при загрузке
        window.addEventListener('DOMContentLoaded', () => {
            initData();
        });
    </script>
</body>
</html>
"""
