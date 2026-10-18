INDEX_HTML = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NetHub | Network Operations & Remote Process Control</title>
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2338bdf8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242'/%3E%3Cpath d='m8 17 4-4 4 4'/%3E%3Cpath d='M12 13v9'/%3E%3C/svg%3E">
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
                    <span class="text-[10px] uppercase tracking-wider px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-400 font-mono border border-zinc-700">v1.0.0</span>
                </div>
            </div>

            <!-- Metadata & Auth Badge -->
            <div class="flex items-center space-x-3">
                <div class="flex items-center space-x-2 px-2.5 py-1 rounded bg-zinc-900/80 border border-zinc-800 text-xs font-mono">
                    <span class="text-zinc-500">Public IP:</span>
                    <span id="externalIpBadge" class="text-sky-400 font-medium">Resolving...</span>
                </div>

                <div id="authStatusContainer" class="flex items-center space-x-2">
                    <!-- Dynamic Auth State -->
                </div>
            </div>
        </div>
    </header>

    <!-- Dev Mode Notice -->
    <div id="devModeNotice" class="hidden bg-amber-950/30 border-b border-amber-800/40 px-4 py-2 text-xs text-amber-200/90 text-center font-mono">
        Notice: Running in development mode. Google OAuth authentication is bypassed until client_id is configured.
    </div>

    <!-- Main Container -->
    <main class="flex-1 max-w-6xl mx-auto px-4 py-6 w-full space-y-6">
        <!-- Tab Navigation -->
        <nav class="flex space-x-1 border-b border-border pb-2 overflow-x-auto">
            <button onclick="switchTab('scanner')" id="tabBtn-scanner" class="tab-btn px-3 py-1.5 rounded text-xs font-medium transition flex items-center space-x-2 bg-zinc-800 text-zinc-100 border border-zinc-700">
                <svg class="w-3.5 h-3.5 text-zinc-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>
                </svg>
                <span>Network Diagnostics</span>
            </button>
            <button onclick="switchTab('interfaces')" id="tabBtn-interfaces" class="tab-btn px-3 py-1.5 rounded text-xs font-medium transition flex items-center space-x-2 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/50">
                <svg class="w-3.5 h-3.5 text-zinc-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <rect x="2" y="2" width="20" height="8" rx="2"/><rect x="2" y="14" width="20" height="8" rx="2"/><line x1="6" y1="6" x2="6.01" y2="6"/><line x1="6" y1="18" x2="6.01" y2="18"/>
                </svg>
                <span>Interfaces</span>
            </button>
            <button onclick="switchTab('apps')" id="tabBtn-apps" class="tab-btn px-3 py-1.5 rounded text-xs font-medium transition flex items-center space-x-2 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/50">
                <svg class="w-3.5 h-3.5 text-zinc-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/>
                </svg>
                <span>Process Manager</span>
            </button>
            <button onclick="switchTab('settings')" id="tabBtn-settings" class="tab-btn px-3 py-1.5 rounded text-xs font-medium transition flex items-center space-x-2 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/50">
                <svg class="w-3.5 h-3.5 text-zinc-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
                </svg>
                <span>OAuth Configuration</span>
            </button>
        </nav>

        <!-- SECTION 1: NETWORK DIAGNOSTICS -->
        <section id="tabContent-scanner" class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Ping Panel -->
            <div class="border border-border bg-[#121215] rounded-lg p-5 space-y-4">
                <div>
                    <h2 class="text-sm font-semibold text-white tracking-tight">Host Ping Diagnostic</h2>
                    <p class="text-xs text-muted mt-0.5">Executes ICMP echo verification with round-trip latency parsing.</p>
                </div>

                <div class="space-y-3">
                    <div>
                        <label class="block text-[11px] font-mono text-zinc-400 uppercase tracking-wider mb-1">Target Host / Domain</label>
                        <div class="flex space-x-2">
                            <input type="text" id="pingHostInput" value="8.8.8.8" placeholder="e.g. 1.1.1.1, gateway.local" 
                                   class="flex-1 bg-zinc-900 border border-zinc-700/80 rounded px-3 py-1.5 text-xs text-zinc-100 font-mono focus:outline-none focus:border-zinc-500">
                            <button onclick="runPing()" id="pingBtn" 
                                    class="px-4 py-1.5 bg-zinc-100 hover:bg-white text-zinc-950 text-xs font-medium rounded transition">
                                Ping
                            </button>
                        </div>
                    </div>

                    <div id="pingResultCard" class="hidden p-3 rounded border text-xs font-mono transition-all">
                        <!-- Filled by JS -->
                    </div>
                </div>
            </div>

            <!-- Port Scanner Panel -->
            <div class="border border-border bg-[#121215] rounded-lg p-5 space-y-4">
                <div>
                    <h2 class="text-sm font-semibold text-white tracking-tight">TCP Port Inspector</h2>
                    <p class="text-xs text-muted mt-0.5">Concurrent asynchronous socket verification powered by asyncio.</p>
                </div>

                <div class="space-y-3">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <div>
                            <label class="block text-[11px] font-mono text-zinc-400 uppercase tracking-wider mb-1">Target IP / Hostname</label>
                            <input type="text" id="scanHostInput" value="127.0.0.1" placeholder="127.0.0.1" 
                                   class="w-full bg-zinc-900 border border-zinc-700/80 rounded px-3 py-1.5 text-xs text-zinc-100 font-mono focus:outline-none focus:border-zinc-500">
                        </div>
                        <div>
                            <label class="block text-[11px] font-mono text-zinc-400 uppercase tracking-wider mb-1">Port Range or List</label>
                            <input type="text" id="scanPortsInput" value="20-1000" placeholder="e.g. 80,443,8080 or 1-1024" 
                                   class="w-full bg-zinc-900 border border-zinc-700/80 rounded px-3 py-1.5 text-xs text-zinc-100 font-mono focus:outline-none focus:border-zinc-500">
                        </div>
                    </div>

                    <div class="flex items-center justify-between pt-1">
                        <div class="flex space-x-1.5">
                            <button onclick="setPresetPorts('top20')" class="text-[11px] font-mono px-2 py-0.5 rounded bg-zinc-800 text-zinc-400 hover:text-zinc-200 border border-zinc-700/60">Top 20</button>
                            <button onclick="setPresetPorts('web')" class="text-[11px] font-mono px-2 py-0.5 rounded bg-zinc-800 text-zinc-400 hover:text-zinc-200 border border-zinc-700/60">HTTP/S</button>
                            <button onclick="setPresetPorts('range1k')" class="text-[11px] font-mono px-2 py-0.5 rounded bg-zinc-800 text-zinc-400 hover:text-zinc-200 border border-zinc-700/60">1-1024</button>
                        </div>
                        <button onclick="runPortScan()" id="scanBtn" 
                                class="px-4 py-1.5 bg-zinc-100 hover:bg-white text-zinc-950 text-xs font-medium rounded transition">
                            Scan Target
                        </button>
                    </div>

                    <div id="scanResultCard" class="hidden p-3 rounded bg-zinc-900/60 border border-zinc-800 text-xs font-mono">
                        <!-- Filled by JS -->
                    </div>
                </div>
            </div>
        </section>

        <!-- SECTION 2: NETWORK INTERFACES -->
        <section id="tabContent-interfaces" class="hidden space-y-4">
            <div class="flex justify-between items-center">
                <div>
                    <h2 class="text-sm font-semibold text-white tracking-tight">Active Network Adapters</h2>
                    <p class="text-xs text-muted mt-0.5">Physical and virtual network interfaces detected on the host.</p>
                </div>
                <button onclick="loadInterfaces()" class="px-3 py-1 bg-zinc-900 hover:bg-zinc-800 text-zinc-300 text-xs font-mono rounded border border-zinc-700 transition">
                    Refresh
                </button>
            </div>

            <div id="interfacesGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <!-- Populated dynamically via JS -->
            </div>
        </section>

        <!-- SECTION 3: PROCESS LAUNCHER -->
        <section id="tabContent-apps" class="hidden space-y-4">
            <div>
                <h2 class="text-sm font-semibold text-white tracking-tight">Process Execution Manager</h2>
                <p class="text-xs text-muted mt-0.5">Trigger verified local applications, scripts, or Windows shortcuts (.lnk) configured in config.json.</p>
            </div>

            <div id="appsGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                <!-- Populated dynamically via JS -->
            </div>

            <!-- Execution Status Pill -->
            <div id="launchToast" class="fixed bottom-6 right-6 hidden bg-zinc-900 border border-zinc-700 p-3 rounded-md shadow-xl z-50 text-xs flex items-center space-x-2.5 font-mono">
                <span class="w-2 h-2 rounded-full bg-sky-400 animate-pulse"></span>
                <span id="launchToastMsg" class="text-zinc-200">Executing target...</span>
            </div>
        </section>

        <!-- SECTION 4: OAUTH & SETTINGS -->
        <section id="tabContent-settings" class="hidden space-y-4">
            <div class="border border-border bg-[#121215] rounded-lg p-5 space-y-4">
                <div>
                    <h2 class="text-sm font-semibold text-white tracking-tight">Google OAuth 2.0 Security Configuration</h2>
                    <p class="text-xs text-muted mt-0.5">Specifications for securing this control panel with single sign-on.</p>
                </div>

                <div class="space-y-4 text-xs">
                    <div class="p-3.5 rounded bg-zinc-900/60 border border-zinc-800 space-y-2 text-zinc-300">
                        <div class="font-medium text-white">OAuth Setup Directives:</div>
                        <ol class="list-decimal list-inside space-y-1 text-zinc-400 font-mono text-[11px]">
                            <li>Register a project on <a href="https://console.cloud.google.com/" target="_blank" class="text-sky-400 hover:underline">Google Cloud Console</a>.</li>
                            <li>Navigate to <b>APIs & Services</b> &rarr; <b>Credentials</b> and create an <b>OAuth 2.0 Client ID</b> (Web application).</li>
                            <li>Set <b>Authorized redirect URI</b> to: <code class="bg-black/60 text-zinc-200 px-1.5 py-0.5 rounded border border-zinc-800">http://localhost:8080/auth/callback</code></li>
                            <li>Save <code>client_id</code> and <code>client_secret</code> into <code>config.json</code> in the NetHub folder.</li>
                            <li>Add your authorized email to <code>allowed_emails</code> array.</li>
                        </ol>
                    </div>

                    <div>
                        <div class="text-[11px] font-mono uppercase tracking-wider text-zinc-400 mb-2">Whitelisted Email Addresses:</div>
                        <div id="allowedEmailsList" class="flex flex-wrap gap-1.5">
                            <!-- Populated dynamically via JS -->
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="border-t border-border py-4 mt-8 bg-[#09090b] text-center text-[11px] text-zinc-500 font-mono">
        NetHub Windows 11 Network Toolkit &bull; FastAPI Subsystem &bull; Self-Hosted Control Plane
    </footer>

    <!-- Client Script -->
    <script>
        function switchTab(tabId) {
            document.querySelectorAll('[id^="tabContent-"]').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.className = "tab-btn px-3 py-1.5 rounded text-xs font-medium transition flex items-center space-x-2 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/50";
            });

            const content = document.getElementById(`tabContent-${tabId}`);
            const btn = document.getElementById(`tabBtn-${tabId}`);
            if (content) content.classList.remove('hidden');
            if (btn) btn.className = "tab-btn px-3 py-1.5 rounded text-xs font-medium transition flex items-center space-x-2 bg-zinc-800 text-zinc-100 border border-zinc-700";

            if (tabId === 'interfaces') loadInterfaces();
            if (tabId === 'apps') loadApps();
        }

        function setPresetPorts(preset) {
            const input = document.getElementById('scanPortsInput');
            if (preset === 'top20') input.value = "21,22,23,25,53,80,110,135,139,143,443,445,993,995,1433,3306,3389,5432,8000,8080";
            if (preset === 'web') input.value = "80,443,3000,5000,8000,8080,8443,8888,9000";
            if (preset === 'range1k') input.value = "1-1024";
        }

        async function initData() {
            try {
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
                            Sign in with Google
                        </a>
                    `;
                }

                const ipRes = await fetch('/api/ip');
                const ipData = await ipRes.json();
                document.getElementById('externalIpBadge').textContent = ipData.ip || 'Unreachable';

                const emailContainer = document.getElementById('allowedEmailsList');
                if (authData.allowed_emails && authData.allowed_emails.length > 0) {
                    emailContainer.innerHTML = authData.allowed_emails.map(e => `
                        <span class="px-2 py-0.5 bg-zinc-900 text-zinc-300 rounded font-mono text-[11px] border border-zinc-800">${e}</span>
                    `).join('');
                } else {
                    emailContainer.innerHTML = '<span class="text-xs text-zinc-500 font-mono">No accounts registered</span>';
                }

            } catch (err) {
                console.error("Initialization error:", err);
            }
        }

        async function runPing() {
            const host = document.getElementById('pingHostInput').value.trim();
            const btn = document.getElementById('pingBtn');
            const card = document.getElementById('pingResultCard');

            if (!host) return;

            btn.disabled = true;
            btn.textContent = "Probing...";
            card.classList.remove('hidden');
            card.className = "p-3 rounded bg-zinc-900 border border-zinc-800 text-zinc-400 text-xs font-mono";
            card.innerHTML = "Executing ICMP echo probe...";

            try {
                const res = await fetch('/api/ping', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({host: host})
                });
                const data = await res.json();

                if (data.alive) {
                    const latency = data.latency_ms !== null ? `${data.latency_ms} ms` : '<1 ms';
                    card.className = "p-3 rounded bg-zinc-900/90 border border-emerald-500/30 text-emerald-400 text-xs font-mono";
                    card.innerHTML = `
                        <div class="flex items-center justify-between">
                            <span class="font-medium flex items-center">
                                <span class="w-2 h-2 rounded-full bg-emerald-400 mr-2"></span>
                                Host ${data.host} is reachable
                            </span>
                            <span class="text-zinc-400">RTT: ${latency}</span>
                        </div>
                    `;
                } else {
                    card.className = "p-3 rounded bg-zinc-900/90 border border-red-500/30 text-red-400 text-xs font-mono";
                    card.innerHTML = `
                        <div class="flex items-center space-x-2">
                            <span class="w-2 h-2 rounded-full bg-red-400"></span>
                            <span>Host ${data.host} unreachable (${data.error || 'Request timed out'})</span>
                        </div>
                    `;
                }
            } catch (err) {
                card.className = "p-3 rounded bg-zinc-900/90 border border-red-500/30 text-red-400 text-xs font-mono";
                card.textContent = "Execution failed: " + err;
            } finally {
                btn.disabled = false;
                btn.textContent = "Ping";
            }
        }

        async function runPortScan() {
            const host = document.getElementById('scanHostInput').value.trim();
            const portsVal = document.getElementById('scanPortsInput').value.trim();
            const btn = document.getElementById('scanBtn');
            const card = document.getElementById('scanResultCard');

            if (!host) return;

            btn.disabled = true;
            btn.textContent = "Scanning...";
            card.classList.remove('hidden');
            card.innerHTML = "Executing concurrent socket connections...";

            try {
                const res = await fetch('/api/scan', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({host: host, ports_str: portsVal})
                });
                const data = await res.json();

                if (data.error) {
                    card.innerHTML = `<span class="text-red-400">Error: ${data.error}</span>`;
                    return;
                }

                let html = `
                    <div class="border-b border-zinc-800 pb-2 mb-2 flex justify-between items-center text-zinc-300">
                        <span class="font-medium">Target: ${data.host}</span>
                        <span class="text-zinc-500">Scanned: ${data.scanned_total} | Open: ${data.open_count}</span>
                    </div>
                `;

                if (data.open_ports.length > 0) {
                    html += `<div class="flex flex-wrap gap-1.5 pt-1">`;
                    data.open_ports.forEach(p => {
                        html += `
                            <span class="px-2 py-0.5 bg-zinc-800 border border-emerald-500/30 text-emerald-400 rounded text-[11px] font-mono">
                                ${p} / TCP OPEN
                            </span>
                        `;
                    });
                    html += `</div>`;
                } else {
                    html += `<p class="text-zinc-500 text-[11px]">No responsive TCP ports detected.</p>`;
                }

                card.innerHTML = html;
            } catch (err) {
                card.innerHTML = `<span class="text-red-400">Scan request failed: ${err}</span>`;
            } finally {
                btn.disabled = false;
                btn.textContent = "Scan Target";
            }
        }

        async function loadInterfaces() {
            const grid = document.getElementById('interfacesGrid');
            grid.innerHTML = '<div class="col-span-full text-center text-zinc-500 text-xs py-6 font-mono">Loading interface states...</div>';

            try {
                const res = await fetch('/api/interfaces');
                const ifaces = await res.json();

                if (ifaces.length === 0) {
                    grid.innerHTML = '<div class="col-span-full text-center text-zinc-500 text-xs py-6 font-mono">No network adapters detected</div>';
                    return;
                }

                grid.innerHTML = ifaces.map(iface => {
                    const statusBadge = iface.is_up 
                        ? '<span class="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-mono bg-zinc-800 text-emerald-400 border border-zinc-700"><span class="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-1.5"></span>UP</span>'
                        : '<span class="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-mono bg-zinc-800 text-zinc-500 border border-zinc-700"><span class="w-1.5 h-1.5 rounded-full bg-zinc-500 mr-1.5"></span>DOWN</span>';
                    
                    const ips = iface.ipv4.map(v4 => `<div class="text-zinc-300 font-mono text-[11px]">${v4.address} <span class="text-zinc-500 text-[10px]">/ ${v4.netmask}</span></div>`).join('') || '<div class="text-zinc-600 text-[11px] font-mono">No IPv4 bound</div>';

                    return `
                        <div class="border border-border bg-[#121215] rounded-md p-4 space-y-3">
                            <div class="flex justify-between items-start">
                                <h3 class="font-medium text-white text-xs truncate max-w-[200px]" title="${iface.name}">${iface.name}</h3>
                                ${statusBadge}
                            </div>
                            <div class="text-[11px] font-mono text-zinc-400 space-y-1">
                                <div>Link Speed: <span class="text-zinc-200">${iface.speed_mbps} Mbps</span></div>
                                <div>MAC Address: <span class="text-zinc-300">${iface.mac || 'N/A'}</span></div>
                            </div>
                            <div class="pt-2 border-t border-zinc-800/80">
                                <div class="text-[10px] font-mono uppercase tracking-wider text-zinc-500 mb-1">IPv4 Binding:</div>
                                ${ips}
                            </div>
                        </div>
                    `;
                }).join('');

            } catch (err) {
                grid.innerHTML = `<div class="col-span-full text-center text-red-400 text-xs py-6 font-mono">Failed to retrieve interfaces: ${err}</div>`;
            }
        }

        async function loadApps() {
            const grid = document.getElementById('appsGrid');
            grid.innerHTML = '<div class="col-span-full text-center text-zinc-500 text-xs py-6 font-mono">Loading registered binaries...</div>';

            try {
                const res = await fetch('/api/apps');
                const apps = await res.json();

                if (apps.length === 0) {
                    grid.innerHTML = '<div class="col-span-full text-center text-zinc-500 text-xs py-6 font-mono">No processes configured in config.json</div>';
                    return;
                }

                grid.innerHTML = apps.map(app => `
                    <div class="border border-border bg-[#121215] rounded-md p-4 flex flex-col justify-between space-y-3 hover:border-zinc-700 transition">
                        <div>
                            <div class="flex items-center justify-between mb-1.5">
                                <h3 class="font-medium text-white text-xs">${app.name}</h3>
                                <span class="text-[10px] font-mono uppercase px-1 rounded bg-zinc-900 border border-zinc-800 text-zinc-400">Binary</span>
                            </div>
                            <p class="text-[11px] text-zinc-400 mb-2">${app.description || 'Host Process Execution'}</p>
                            <div class="text-[10px] font-mono text-zinc-500 truncate" title="${app.path}">Path: ${app.path}</div>
                        </div>

                        <button onclick="launchApp('${app.id}')" 
                                class="w-full py-1.5 px-3 bg-zinc-900 hover:bg-zinc-800 text-zinc-200 text-xs font-mono font-medium rounded border border-zinc-700 transition flex items-center justify-center space-x-1.5">
                            <span>Execute Target</span>
                            <span class="text-zinc-500">&rarr;</span>
                        </button>
                    </div>
                `).join('');

            } catch (err) {
                grid.innerHTML = `<div class="col-span-full text-center text-red-400 text-xs py-6 font-mono">Failed to load processes: ${err}</div>`;
            }
        }

        async function launchApp(appId) {
            const toast = document.getElementById('launchToast');
            const msg = document.getElementById('launchToastMsg');

            toast.classList.remove('hidden');
            msg.textContent = `Dispatching execution signal for ${appId}...`;

            try {
                const res = await fetch(`/api/launch/${appId}`, { method: 'POST' });
                const data = await res.json();

                if (data.success) {
                    msg.textContent = `Signal OK: ${data.message}`;
                } else {
                    msg.textContent = `Signal Error: ${data.error}`;
                }
            } catch (err) {
                msg.textContent = `Execution failed: ${err}`;
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
