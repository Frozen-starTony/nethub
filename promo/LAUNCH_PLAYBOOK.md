# 🚀 NetHub: Viral Launch & Promotional Blitz Playbook
**Repository:** [Frozen-starTony/nethub](https://github.com/Frozen-starTony/nethub)  
**Author:** Frozen-starTony  
**License:** MIT  
**Release:** v1.0.0 (`NetHub.exe` standalone binary)

---

## 📑 Table of Contents
1. [Direct 1-Click Reddit Submissions (Pre-filled URLs)](#1-direct-1-click-reddit-submissions)
2. [Hacker News (Show HN) Submission Package](#2-hacker-news-show-hn-submission-package)
3. [Twitter / X Viral Thread Architecture](#3-twitter--x-viral-thread-architecture)
4. [Telegram Broadcast Announcements (RU & EN)](#4-telegram-broadcast-announcements)
5. [Algorithm Timing Playbook (Reddit, HN, Habr)](#5-algorithm-timing-playbook)
6. [Platform & Directory Submissions (Product Hunt, AlternativeTo, LibHunt, Awesome-Selfhosted, Winget)](#6-platform--directory-submissions)

---

## 1. Direct 1-Click Reddit Submissions

> [!TIP]
> Click any of the links below in your web browser. Reddit will immediately open the submission form with the target subreddit, tailored post title, and complete Markdown post body already filled in.

### 🌐 Direct Submission Links:

| Subreddit | Angle & Target Audience | 1-Click Direct Launch Link |
| :--- | :--- | :--- |
| **r/selfhosted** (350k+ members) | Self-hosters hosting local services, CGNAT pain, zero-router-login UPnP | [🚀 **Click to Submit to r/selfhosted**](https://www.reddit.com/r/selfhosted/submit?title=I+built+NetHub%3A+A+lightweight+Windows+tool+to+detect+CGNAT+%28RFC+6598%29+vs+Public+IP+and+1-click+UPnP+port+forward+without+router+passwords&text=Hey+r%2Fselfhosted%21%0A%0ALike+many+of+you%2C+I+host+services+and+local+game+servers+%28Minecraft%2C+Palworld%2C+media%2Fremote+tools%29+from+my+home+Windows+machine.+Over+the+years%2C+the+two+most+common+stumbling+blocks+I+saw+%28and+suffered+through+with+friends%29+were%3A%0A%0A1.+%2A%2AThe+CGNAT+trap%3A%2A%2A+Friends+couldn%27t+connect+despite+forwarding+ports.+Turns+out+their+ISP+stuck+them+behind+Carrier-Grade+NAT+%28RFC+6598+%60100.64.0.0%2F10%60+or+internal+ISP+NAT%29%2C+making+direct+incoming+connections+impossible+without+a+relay%2Ftunnel.%0A2.+%2A%2ARouter+UI+friction%3A%2A%2A+Logging+into+cluttered+192.168.1.1+interfaces%2C+hunting+through+obscure+menus%2C+forgetting+ISP+admin+credentials%2C+or+dealing+with+locked-down+ISP+gateway+boxes.%0A%0ATo+solve+this+once+and+for+all%2C+I+built+%2A%2ANetHub%2A%2A+%E2%80%93+an+open-source%2C+hybrid+CLI+%26+Web+UI+utility+for+Windows+11.%0A%0A%23%23%23+%F0%9F%8C%9F+What+it+does%3A%0A-+%F0%9F%94%8D+%2A%2AInstant+IP+%26+CGNAT+Detection%3A%2A%2A+In+under+1+second%2C+it+checks+whether+your+WAN+IP+is+a+true+Public+%28%22White%22%29+IP+or+locked+behind+CGNAT+%28%60100.64.x.x%60+%2F+RFC+6598%29.+It+displays+your+external+ISP%2C+AS+number%2C+and+geolocation.%0A-+%E2%9A%A1+%2A%2A1-Click+UPnP+Port+Forwarding%3A%2A%2A+Uses+UPnP+IGD+SOAP+calls+to+open+ports+on+your+router+directly+from+your+PC.+No+192.168.1.1+login+or+admin+password+required.%0A-+%F0%9F%8C%90+%2A%2AExternal+WAN+Reachability+Verification%3A%2A%2A+Verifies+from+an+external+network+gateway+whether+the+port+is+actually+receiving+inbound+traffic.%0A-+%F0%9F%9A%80+%2A%2ARemote+Server+Launcher%3A%2A%2A+Built-in+web+dashboard+%28FastAPI%29+at+%60localhost%3A8080%60+allows+triggering+game+servers%2C+batch+files%2C+and+shortcuts+locally+or+remotely.%0A-+%F0%9F%94%92+%2A%2ASecurity%3A%2A%2A+Includes+optional+Google+OAuth+2.0+whitelist+for+web+dashboard+access.%0A%0A%23%23%23+%F0%9F%92%BB+Tech+Stack+%26+Open+Source%3A%0A-+Written+in+Python+3.10%2B+%28FastAPI%2C+asyncio%2C+UPnP+protocol%29.%0A-+Dual+interface%3A+slick+Rich+terminal+CLI+%2B+modern+responsive+Web+UI.%0A-+Available+as+raw+Python+script+or+a+pre-compiled+standalone+%60NetHub.exe%60+%28no+Python+install+needed%29.%0A-+Fully+open+source+under+the+%2A%2AMIT+License%2A%2A.%0A%0AI%27m+a+beginner+programmer+who+built+this+tool+out+of+personal+necessity+to+help+friends+and+the+self-hosting+community.+I%27d+love+your+feedback%2C+code+review%2C+or+feature+requests%21%0A%0A-+%2A%2AGitHub+Repository%3A%2A%2A+https%3A%2F%2Fgithub.com%2FFrozen-starTony%2Fnethub%0A-+%2A%2APre-built+EXE+Release%3A%2A%2A+https%3A%2F%2Fgithub.com%2FFrozen-starTony%2Fnethub%2Freleases%2Ftag%2Fv1.0.0%0A%0AIf+you+find+it+useful%2C+a+star+%E2%AD%90+on+GitHub+would+mean+the+world+to+me%21) |
| **r/admincraft** (140k+ members) | Dedicated Minecraft admins, fixing "Connection Timed Out" on port 25565 | [🚀 **Click to Submit to r/admincraft**](https://www.reddit.com/r/admincraft/submit?title=I+made+NetHub%3A+An+open-source+tool+that+diagnoses+why+friends+can%27t+join+your+Minecraft+server+%28CGNAT+check+%2B+1-click+UPnP+port+forwarding+for+25565%29&text=Hey+everyone%21%0A%0AIf+you%27ve+ever+tried+hosting+a+Minecraft+server+%28Paper%2C+Fabric%2C+Purpur%2C+or+Vanilla%29+on+your+own+Windows+PC%2C+you%27ve+probably+encountered+the+dreaded%3A+%2A%22I+gave+my+friends+my+IP%2C+but+they+get+Connection+Timed+Out.%22%2A%0A%0A99%25+of+the+time%2C+the+issue+is+one+of+two+things%3A%0A1.+%2A%2AYour+ISP+placed+you+behind+CGNAT+%28Carrier-Grade+NAT+%2F+RFC+6598%29%3A%2A%2A+Your+router+doesn%27t+have+a+real+public+IP%2C+so+no+amount+of+port+forwarding+will+let+outside+players+in+directly.%0A2.+%2A%2APort+25565+isn%27t+forwarded+correctly%2A%2A%2C+or+you+can%27t+access+your+router%27s+192.168.1.1+admin+panel+because+your+family%2FISP+changed+the+password.%0A%0AI+got+tired+of+walking+friends+through+this+exact+troubleshooting+loop+every+single+time+we+wanted+to+play%2C+so+I+built+%2A%2ANetHub%2A%2A+%E2%80%94+a+free%2C+open-source+tool+for+Windows.%0A%0A%23%23%23+%F0%9F%8E%AE+How+it+helps+Minecraft+Server+Hosts%3A%0A-+%E2%9A%A1+%2A%2A1-Click+UPnP+Forwarding+for+Port+25565%3A%2A%2A+Automatically+tells+your+router+to+open+Minecraft%27s+port+%28TCP+25565%29+via+UPnP+in+under+a+second.+You+don%27t+need+to+log+into+your+router+or+remember+the+admin+password.%0A-+%F0%9F%94%8D+%2A%2AInstant+CGNAT+Diagnosis%3A%2A%2A+Tells+you+immediately+whether+you+have+a+real+Public+%28White%29+IP+or+if+you%27re+stuck+behind+CGNAT+%28%60100.64.x.x%60%29.+If+you+are+on+CGNAT%2C+you+know+right+away+you%27ll+need+a+tunnel+%28Playit.gg+%2F+ngrok%29+instead+of+wasting+hours+fiddling+with+router+menus.%0A-+%F0%9F%8C%90+%2A%2AExternal+WAN+Reachability+Test%3A%2A%2A+Tests+from+an+outside+gateway+whether+external+players+can+actually+see+your+server.%0A-+%F0%9F%95%B9%EF%B8%8F+%2A%2AWeb+Remote+Launcher%3A%2A%2A+Start+your+server+%60.bat%60+or+%60.lnk%60+script+from+your+phone+via+the+web+UI+%28%60localhost%3A8080%60%29.%0A%0A%23%23%23+%F0%9F%93%A6+Quick+Info%3A%0A-+100%25+Free+%26+Open+Source+%28MIT+License%29.%0A-+Comes+with+both+a+slick+terminal+interface+and+a+web+dashboard.%0A-+Standalone+single+%60.exe%60+available+in+Releases+%28no+Python+installation+required%29.%0A%0A-+%2A%2AGitHub+Repo%3A%2A%2A+https%3A%2F%2Fgithub.com%2FFrozen-starTony%2Fnethub%0A-+%2A%2ADownload+NetHub.exe%3A%2A%2A+https%3A%2F%2Fgithub.com%2FFrozen-starTony%2Fnethub%2Freleases%2Flatest%0A%0AI%27m+a+beginner+dev%2C+and+this+is+my+passion+project+to+solve+a+real+headache+for+our+gaming+group.+Would+love+to+hear+your+thoughts+and+bug+reports%21) |
| **r/Python** (1.2M+ members) | Technical showcase, FastAPI, asyncio, UPnP SOAP XML, PyInstaller packaging | [🚀 **Click to Submit to r/Python**](https://www.reddit.com/r/Python/submit?title=%5BProject%5D+NetHub%3A+A+hybrid+FastAPI+%2B+UPnP+network+utility+for+Windows+to+diagnose+CGNAT+%28RFC+6598%29+and+automate+port+forwarding&text=%23%23%23+What+My+Project+Does%3A%0A%2A%2ANetHub%2A%2A+is+an+open-source+Windows+11+utility+built+with+Python+that+solves+home+networking+headaches+for+self-hosters+and+gamers.+It%3A%0A1.+Instantly+classifies+your+network+into+%60WHITE_PUBLIC%60%2C+%60GRAY_CGNAT%60+%28RFC+6598+%2F+%60100.64.0.0%2F10%60%29%2C+or+%60PRIVATE%60+by+probing+local+network+interfaces%2C+default+gateways%2C+and+external+STUN%2FWAN+endpoints.%0A2.+Automates+1-click+UPnP+IGD+port+forwarding+over+SOAP+XML%2C+allowing+users+to+map+router+ports+without+accessing+the+router%27s+web+admin+panel.%0A3.+Performs+external+WAN+reachability+checks+to+verify+open+ports+from+an+independent+outside+gateway.%0A4.+Serves+a+dual-mode+interface%3A+an+interactive+terminal+console+%28via+%60rich%60%29+alongside+a+local+web+dashboard+served+by+%60FastAPI%60+%2F+%60uvicorn%60+%28with+optional+Google+OAuth+2.0+whitelist%29.%0A%0A%23%23%23+Target+Audience%3A%0ASelf-hosters%2C+home+lab+enthusiasts%2C+and+gamers+hosting+dedicated+servers+%28Minecraft%2C+Palworld%2C+CS2%2C+Terraria%2C+or+remote+RDP%29+on+Windows.%0A%0A%23%23%23+Technical+Details+%26+Libraries+Used%3A%0A-+%2A%2AFastAPI+%2B+Uvicorn%3A%2A%2A+Powers+the+responsive+web+dashboard+and+REST+API+for+port+actions+and+server+process+management.%0A-+%2A%2Aasyncio+%26+aiohttp%3A%2A%2A+Handles+concurrent+asynchronous+network+requests+for+WAN+IP+checks+and+reachability+tests.%0A-+%2A%2AUPnP+SOAP+Protocol%3A%2A%2A+Discovers+local+router+IGDs+via+SSDP+%28Simple+Service+Discovery+Protocol%29+and+sends+XML+SOAP+payloads+to+manage+NAT+port+mappings.%0A-+%2A%2ARich%3A%2A%2A+Provides+an+aesthetic%2C+color-coded+CLI+with+live+status+indicators.%0A-+%2A%2APyInstaller+%2F+Packaging%3A%2A%2A+Bundled+into+a+standalone+%60NetHub.exe%60+binary+for+zero-dependency+execution+on+Windows+11.%0A%0A%23%23%23+Comparison+to+Alternatives%3A%0AExisting+UPnP+tools+on+Windows+%28like+Port+Mapper+or+old+UPnP+GUI+apps%29+are+either+abandoned+Java-based+utilities+from+2012+or+command-line-only+tools+lacking+CGNAT+detection+and+external+reachability+verification.+NetHub+combines+diagnosis%2C+forwarding%2C+testing%2C+and+service+management+in+a+modern+async+Python+codebase.%0A%0AI+am+relatively+new+to+programming+and+built+this+to+solve+everyday+pains+for+myself+and+my+friends.+I+would+love+feedback+on+code+structure%2C+async+patterns%2C+and+router+compatibility%21%0A%0A-+%2A%2AGitHub+Repository%3A%2A%2A+https%3A%2F%2Fgithub.com%2FFrozen-starTony%2Fnethub%0A-+%2A%2ARelease+%28v1.0.0+Standalone+Binary%29%3A%2A%2A+https%3A%2F%2Fgithub.com%2FFrozen-starTony%2Fnethub%2Freleases%2Ftag%2Fv1.0.0) |
| **r/homelab** (550k+ members) | Network topology diagnostics, ISP troubleshooting, home server admin | [🚀 **Click to Submit to r/homelab**](https://www.reddit.com/r/homelab/submit?title=NetHub%3A+Open-source+Windows+utility+for+instant+CGNAT+%28RFC+6598%29+detection%2C+UPnP+port+mapping%2C+and+WAN+reachability+verification&text=Hey+r%2Fhomelab%2C%0A%0AIf+you+maintain+a+homelab+that+interfaces+with+Windows+machines+or+you+help+family%2Ffriends+diagnose+their+home+network+setups%2C+you%27ve+probably+run+into+ISP+CGNAT+hurdles+and+router+port-forwarding+issues.%0A%0AI+created+%2A%2ANetHub%2A%2A+to+make+diagnosing+WAN+topologies+and+managing+temporary+or+gaming+port+forwards+completely+painless.%0A%0A%23%23%23+%F0%9F%9B%A0%EF%B8%8F+Key+Capabilities%3A%0A-+%2A%2ACGNAT+vs+Public+IP+Classification%3A%2A%2A+Instantly+detects+whether+the+upstream+WAN+interface+is+allocated+a+public+routable+IPv4+address+or+trapped+in+carrier+NAT+%28RFC+6598+%60100.64.0.0%2F10%60+or+RFC+1918%29.+Fetches+ISP+AS+number%2C+ISP+name%2C+and+location.%0A-+%2A%2AUPnP+IGD+Port+Forwarding%3A%2A%2A+Automatically+discovers+the+gateway+IGD+via+SSDP+and+injects+port+mappings+for+common+services+%28custom+ports%2C+Minecraft+25565%2C+Palworld+8211%2C+Terraria+7777%2C+RDP+3389%29+without+needing+router+credentials.%0A-+%2A%2AExternal+WAN+Reachability+Testing%3A%2A%2A+Checks+whether+the+mapped+port+is+actually+accessible+from+the+public+internet.%0A-+%2A%2ADual+Interface%3A%2A%2A+Terminal+CLI+with+colored+diagnostics+%2B+FastAPI-backed+Web+UI+at+%60localhost%3A8080%60+with+optional+Google+OAuth+protection.%0A-+%2A%2AProcess+Launcher%3A%2A%2A+Can+trigger+local+dedicated+server+scripts+or+processes+remotely+from+any+device+on+the+local+network.%0A%0A%23%23%23+%F0%9F%93%A6+Availability%3A%0A-+MIT+Licensed.%0A-+Standalone+single-file+executable+%28%60NetHub.exe%60%29+or+run+from+source+via+Python+3.10%2B.%0A%0A-+%2A%2ASource+Code%3A%2A%2A+https%3A%2F%2Fgithub.com%2FFrozen-starTony%2Fnethub%0A-+%2A%2AReleases%3A%2A%2A+https%3A%2F%2Fgithub.com%2FFrozen-starTony%2Fnethub%2Freleases%2Flatest%0A%0AAs+an+early-career+programmer%2C+I%27d+appreciate+any+feedback+on+edge-case+router+compatibility+%28especially+nested+NAT+scenarios%29+and+network+detection+logic%21) |

---

## 2. Hacker News (Show HN) Submission Package

HN submission success relies on zero marketing jargon, pure engineering transparency, and an authentic author story.

### 📝 Title:
```text
Show HN: NetHub – Diagnose CGNAT vs. public IP and 1-click UPnP port forward on Windows
```
*(URL field: `https://github.com/Frozen-starTony/nethub`)*

### 💬 First Comment (Submit immediately after posting):
```text
Hey HN,

I built NetHub (https://github.com/Frozen-starTony/nethub). I am a beginner programmer, and I created this to solve a frequent problem when hosting game servers (Minecraft, Palworld, CS2) and home services with friends.

The problem:
Many domestic ISPs now place subscribers behind Carrier-Grade NAT (RFC 6598 100.64.0.0/10 or RFC 1918 blocks) without informing them. When friends or colleagues can't connect, people waste hours troubleshooting Windows Firewall, antivirus, and router NAT rules—unaware that their gateway never had a globally routable IPv4 address in the first place.

Even when a user does have a public IP, configuring domestic routers (192.168.1.1) is often frustrating due to lost admin passwords, ISP-locked firmware, or complex UIs.

How NetHub works:
1. IP & Topology Classification: Queries local interfaces, default gateways, and public STUN/WAN reflection endpoints. Classifies network state into WHITE_PUBLIC, GRAY_CGNAT, or PRIVATE, and inspects AS/ISP details.
2. UPnP IGD Port Forwarding: Discovers the router's Internet Gateway Device (IGD) on the LAN via SSDP (M-SEARCH UDP multicast) and makes asynchronous SOAP XML calls over HTTP to inject AddPortMapping requests. No router web credentials needed.
3. WAN Verification: NetHub probes an independent external gateway service to confirm whether the TCP/UDP port is genuinely reachable from the outside internet.
4. Process & Remote Management: Includes a FastAPI web server running on localhost:8080 (alongside an interactive Rich CLI) that can trigger server scripts remotely, protected by an optional Google OAuth 2.0 email whitelist.

Tech Stack & Packaging:
Python 3.10+, FastAPI, asyncio, aiohttp, Rich. For non-developer gamers and Windows users who don't have Python installed, I built and published a standalone, single-file Windows binary (NetHub.exe in GitHub Releases).

Security considerations:
UPnP inherently allows LAN devices to map ports on the gateway. NetHub includes functions to inspect, view, and purge active port mappings when a gaming or hosting session ends. For the web UI, Google OAuth prevents unauthorized local or remote triggers.

Code is MIT licensed: https://github.com/Frozen-starTony/nethub

I would appreciate any feedback from the HN community on router edge-cases, SOAP compatibility quirks across different vendors (ASUS, Keenetic, TP-Link, Netgear), and async architecture improvements!
```

---

## 3. Twitter / X Viral Thread Architecture

A high-retention 6-part thread engineered for developer, self-hoster, and gaming tech Twitter.

### Tweet 1 (The Viral Hook)
Ever tried hosting a Minecraft or Palworld server for your friends, only for them to get hit with:

"Connection Timed Out: Connect"? 🛑

90% of the time, your ISP quietly stuck you behind CGNAT (Carrier-Grade NAT).

I built NetHub: a free, open-source Windows utility that fixes this in 1 click. 🧵👇

---

### Tweet 2 (The Technical Pain Point)
Because IPv4 addresses are depleted, ISPs bundle thousands of customers behind a shared RFC 6598 address (100.64.0.0/10).

When you're behind CGNAT, standard port forwarding does NOTHING—inbound packets are blocked at your ISP's gateway.

NetHub tests your WAN in <1s and tells you:
✅ Public (White) IP: You can host directly!
⚠️ CGNAT (Gray) IP: You need a tunnel (Playit / ngrok).

---

### Tweet 3 (No More Router Logins)
Even if you have a Public IP, opening ports usually means:
❌ Finding your router IP (192.168.1.1)
❌ Hunting down lost admin passwords
❌ Navigating cryptic ISP firmware

NetHub sends UPnP IGD SOAP requests directly to your router:
Port 25565 (Minecraft), 8211 (Palworld), 7777 (Terraria), or RDP open in under 1 second. No login required.

---

### Tweet 4 (Under The Hood)
How it's built:
🐍 Modern Python 3.10+ with asyncio & aiohttp
⚡ FastAPI dashboard at localhost:8080
🎨 Color-coded CLI powered by Rich
🌐 Independent WAN reachability gateway verification
🔒 Optional Google OAuth 2.0 whitelist protection

Available as raw Python or a zero-dependency standalone `NetHub.exe`!

---

### Tweet 5 (Remote Server Launcher)
Bonus feature:
NetHub turns your PC into a mini gaming dashboard.

You can trigger your dedicated server batch files (`.bat`), shortcuts (`.lnk`), or processes from your phone while sitting on the couch via the local web UI.

---

### Tweet 6 (CTA & Open-Source Link)
I'm a beginner programmer and built this out of frustration to help my friends play together without network headaches.

100% Free & Open Source under MIT.
⭐ Give it a star on GitHub & download the binary:
https://github.com/Frozen-starTony/nethub

RT to save a friend from port-forwarding nightmares! 🔄

#opensource #python #selfhosted #minecraft #networking #windows11 #buildinpublic

---

## 4. Telegram Broadcast Announcements

### 🇷🇺 Вариант для русскоязычных Telegram-каналов
*(Рекомендуемые каналы: Типичный Программист, Хабр, SysAdmin, Minecraft СНГ, Devops / Системное администрирование, Open Source Ru)*

```markdown
🎮 **Устали объяснять друзьям, почему они не могут зайти на ваш сервер Minecraft, Palworld или CS2?**

9 из 10 домашних провайдеров в РФ (Ростелеком, МТС, Дом.ру, Билайн) незаметно сажают абонентов за **CGNAT (Серый IP, RFC 6598)**. В итоге вы тратите часы на ковыряние в роутере, а друзья всё равно получают «Connection Timed Out».

Наш подписчик @Frozen-starTony (начинающий разработчик) написал утилиту **NetHub** — бесплатный Open-Source инструмент для Windows 11, который решает эту проблему за 1 секунду.

⚡ **Что умеет NetHub:**
• 🔍 **Мгновенный детектор IP:** точно определяет, Белый (Public) у вас IP или Серый (CGNAT 100.64.x.x / NAT), выводит вашего провайдера, AS-номер и город.
• 🚀 **1-Click UPnP проброс портов:** открывает порты прямо в роутере по протоколу UPnP без паролей от админки 192.168.1.1. Шаблоны для Minecraft (25565), Palworld (8211), Terraria (7777), CS2, RDP.
• 🌐 **Внешняя проверка доступности:** независимый шлюз проверяет, виден ли ваш открытый порт из глобального интернета.
• 🕹️ **Веб-пульт управления:** встроенный локальный интерфейс на FastAPI (`localhost:8080`) для запуска серверов и батников с телефона.
• 🔒 **Авторизация:** защита через белый список Google OAuth 2.0.

📦 **Установка не требуется:** доступен готовый standalone бинарник `NetHub.exe` без необходимости ставить Python.

⭐ **Исходный код (MIT License):**
👉 https://github.com/Frozen-starTony/nethub

📥 **Скачать релиз v1.0.0:**
👉 https://github.com/Frozen-starTony/nethub/releases/tag/v1.0.0

*Поддержите начинающего автора звёздочкой на GitHub!*
```

---

### 🇬🇧 International English Version (Dev / Sysadmin Telegram Channels)
*(Recommended channels: Python Developers, SelfHosted Community, DevOps World)*

```markdown
🚀 **NetHub — Open-Source Windows 11 Utility for CGNAT Detection & 1-Click UPnP Port Forwarding**

Ever spent hours diagnosing why inbound connections to your home server or Minecraft/Palworld dedicated server fail?

**NetHub** diagnoses your network topology and manages port forwarding without needing router admin logins:

🔹 **CGNAT vs Public IP Classification:** Checks RFC 6598 (`100.64.0.0/10`) blocks in under a second. Displays ISP name, AS number, and geolocation.
🔹 **1-Click UPnP Port Forwarding:** Discovers your gateway IGD and maps ports (25565, 8211, 7777, 3389) via SOAP XML without logging into 192.168.1.1.
🔹 **External WAN Reachability:** Tests actual packet reachability via an outside gateway.
🔹 **Local Web Dashboard & Remote Launcher:** FastAPI-powered dashboard at `localhost:8080` to launch dedicated servers and batch scripts remotely.
🔹 **Zero Dependencies:** Single portable `NetHub.exe` available in Releases.

MIT Licensed • Built with Python, FastAPI, and Rich.

🔗 **GitHub:** https://github.com/Frozen-starTony/nethub  
💾 **Direct Download:** https://github.com/Frozen-starTony/nethub/releases/latest
```

---

## 5. Algorithm Timing Playbook

| Platform | Best Days | Optimal UTC | Optimal MSK | Algorithmic Mechanism |
| :--- | :--- | :--- | :--- | :--- |
| **Reddit** | Tuesday, Wednesday, Thursday | **12:00 – 14:30 UTC** | **15:00 – 17:30 MSK** | US East Coast wakes up (07:00–09:30 AM EST) while Europe is mid-afternoon. Reddit's Hot algorithm weights early upvote velocity in the first 60 minutes. |
| **Hacker News** | Tuesday, Wednesday | **13:00 – 15:00 UTC** | **16:00 – 18:00 MSK** | HN decay formula $S = (U - 1) / (T + 2)^{1.8}$ prioritizes early comment and vote bursts during US working hours. |
| **Habr (Хабр)** | Monday, Tuesday, Wednesday | **07:00 – 09:00 UTC** or **14:00 – 16:00 UTC** | **10:00 – 12:00 MSK** or **17:00 – 19:00 MSK** | Morning reading at office or evening commute reading. Maximizes 24-hour Daily Best rating. |
| **Twitter / X** | Tuesday to Friday | **14:00 – 16:00 UTC** | **17:00 – 19:00 MSK** | Global tech crossover peak between US & EMEA. |

---

## 6. Platform & Directory Submissions

1. **Product Hunt:**
   - Tagline: `Zero-friction UPnP port forwarding & CGNAT diagnosis for Windows`
   - Topics: `Developer Tools`, `Open Source`, `Gaming`, `Tech`
2. **AlternativeTo:**
   - List as an alternative to: `Port Mapper`, `UPnP Port Forwarder`, `Simple Port Forwarding`, `ngrok`, `Playit.gg`, `Hamachi`.
3. **LibHunt GitHub Topics:**
   - Add these topics to the GitHub repo: `cgnat`, `upnp`, `port-forwarding`, `fastapi`, `self-hosted`, `minecraft-server`, `windows11`, `rfc-6598`.
4. **Awesome-Selfhosted PR:**
   - Add entry under `Network Configuration`:
     `- [NetHub](https://github.com/Frozen-starTony/nethub) - Windows utility to diagnose CGNAT (RFC 6598) vs public IP, 1-click UPnP port forwarding, and remote server process launcher. MIT. Python.`
5. **Winget Package Submission:**
   - Run `wingetcreate new https://github.com/Frozen-starTony/nethub/releases/download/v1.0.0/NetHub.exe` to submit directly to `microsoft/winget-pkgs`.
