# Ready-to-Post Reddit Templates for NetHub

Below are three tailored, high-converting posts for specific subreddits. Copy and paste them directly!

---

## 1. r/selfhosted

**Suggested Title:**
> I got tired of logging into my router to forward ports, so I built NetHub: a Windows 11 tool that classifies Public vs CGNAT IPs and opens ports via UPnP in 1 click (with a local Web UI)

**Post Body:**
```markdown
Hey everyone!

Like many of you hosting game servers (Minecraft, Palworld, CS2) or local services at home, I constantly ran into two persistent frustrations:

1. **"Am I trapped behind CGNAT or do I actually have a Public (White) IP?"**
2. **"Why do I need to log into 192.168.1.1 every time I need to test or open a port for a self-hosted server?"**

I'm still a beginner in Python programming, so I decided to build a tool called **NetHub** to solve this once and for all for myself and my friends.

### What it does:
- **Instant IP Inspector:** Classifies your route (`WHITE_PUBLIC`, `GRAY_CGNAT`, or `PRIVATE`) in under 1 second, showing your ISP organization, AS number, and geolocation.
- **1-Click UPnP Automated Port Mapper:** Forwards ports (Minecraft 25565, Palworld 8211, CS2 27015, RDP 3389, Jellyfin, etc.) on your home router directly via UPnP SOAP protocols — zero router admin login required.
- **External WAN Reachability Check:** Probes your opened port through an external test node to verify actual inbound connectivity from the Internet.
- **Self-Hosted Web UI + CLI:** Works either directly in your Windows Terminal or as a local web dashboard (`http://localhost:8080`) built with FastAPI.
- **Remote Process Launcher:** Lets you launch configured dedicated server scripts and `.lnk` shortcuts right from the browser.
- **Standalone Binary:** Available as a single compiled `NetHub.exe` (no Python install required).

### Tech Stack:
- Python 3.10+, FastAPI, Asyncio, pure HTML/CSS/JS frontend embedded in the binary.
- Open Source (MIT License).

### Links:
- **GitHub Repository:** https://github.com/Frozen-starTony/nethub
- **Releases (.exe download):** https://github.com/Frozen-starTony/nethub/releases

I'd really love your feedback, feature ideas, or a ⭐ star if you find this useful!
```

---

## 2. r/admincraft & r/Minecraft

**Suggested Title:**
> Built a free Windows tool for hosting Minecraft servers: tests if you have a Public IP or CGNAT, and forwards port 25565 on your router in 1 click (no router password needed)

**Post Body:**
```markdown
Hey guys,

How many times have you set up a local Minecraft server, gave your IP to friends, and they just couldn't connect?

Usually it's one of two things:
1. Your ISP has you behind CGNAT (Carrier-Grade NAT / Gray IP), which blocks all incoming connections.
2. Port 25565 isn't forwarded on your router, and logging into 192.168.1.1 is confusing or you don't know the password.

I made a free open-source utility called **NetHub** to solve this:
- Double click `NetHub.exe`.
- It immediately tells you if your IP is **White/Public** (friends can join) or **CGNAT/Gray** (blocked by ISP, with tips on using Playit.gg to bypass it).
- Has a **1-click button to forward port 25565 (Minecraft)** on your router automatically using UPnP.
- Includes a button to launch your server `.bat` script from a browser UI.

It's completely free and open source:
- **GitHub:** https://github.com/Frozen-starTony/nethub
- **Download:** https://github.com/Frozen-starTony/nethub/releases/latest

Hope this saves you guys some headaches when playing with friends!
```

---

## 3. r/Python (For "Showoff Saturday")

**Suggested Title:**
> [Showoff Saturday] NetHub — An asynchronous network diagnostic & UPnP port mapper with hybrid Terminal CLI + FastAPI Web Control Plane

**Post Body:**
```markdown
Hi r/Python!

I wanted to share a project I've been working on as I learn Python: **NetHub**.

It's designed to solve common networking and self-hosting hurdles on Windows 11. It operates in dual modes: an interactive rich terminal CLI and an in-process FastAPI web server.

### Technical Highlights:
- **Async UPnP Client:** Implements SSDP multicast discovery (`239.255.255.250:1900`) and executes SOAP XML requests (`AddPortMapping`, `DeletePortMapping`) against `urn:schemas-upnp-org:service:WANIPConnection:1`.
- **IP Route Classifier:** Queries independent STUN/HTTP reflection endpoints and parses IP subnet ranges (RFC 6598 `100.64.0.0/10` and RFC 1918) to detect CGNAT.
- **Embedded Web UI:** Pure responsive CSS/vanilla JS served directly in-process from Python templates without external node/npm build dependencies.
- **Packaging:** Bundled into a standalone executable via PyInstaller.

Repo: https://github.com/Frozen-starTony/nethub

All feedback and code review critiques are welcome!
```
