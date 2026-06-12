import os
import sys
import socket
import threading
import asyncio
import websockets
import pyautogui
import logging
import subprocess
import webbrowser
import tkinter as tk
from tkinter import ttk, scrolledtext
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

# Silence internal websocket protocol verbose logs
logging.getLogger('websockets').setLevel(logging.CRITICAL)

class BarcodeServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wireless Barcode Server Manager")
        self.root.geometry("520x620")
        self.root.configure(bg="#f1f5f9")
        
        self.pc_ip = self.get_local_ip()
        self.generate_html_file(self.pc_ip)
        
        self.clear_zombie_ports()
        self.create_widgets()
        
        # Start core network processes safely
        try:
            self.start_servers()
        except Exception as e:
            self.write_log(f"[CRITICAL ERROR] Failed starting servers: {e}")

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    def clear_zombie_ports(self):
        """Clears ports 8765 and 8000 directly via native Windows command lines"""
        for port in [8765, 8000]:
            try:
                cmd = f'powershell -Command "Stop-Process -Id (Get-NetTCPConnection -LocalPort {port}).OwningProcess -Force"'
                subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                pass

    def generate_html_file(self, pc_ip):
        html_lines = [
            '<!DOCTYPE html>',
            '<html lang="en">',
            '<head>',
            '    <meta charset="UTF-8">',
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            '    <title>Sleek Web Barcode Scanner</title>',
            '    <script src="https://unpkg.com/html5-qrcode"></script>',
            '    <style>',
            '        :root {',
            '            --primary: #4f46e5;',
            '            --bg-main: #f8fafc;',
            '            --card-bg: #ffffff;',
            '            --text-dark: #1e293b;',
            '            --text-muted: #64748b;',
            '            --success: #10b981;',
            '            --error: #ef4444;',
            '            --warning: #b45309;',
            '        }',
            '        * { box-sizing: border-box; margin: 0; padding: 0; font-family: system-ui, sans-serif; }',
            '        body { background-color: var(--bg-main); color: var(--text-dark); display: flex; flex-direction: column; align-items: center; padding: 16px; min-height: 100vh; }',
            '        .app-container { width: 100%; max-width: 480px; background: var(--card-bg); border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); padding: 24px; display: flex; flex-direction: column; gap: 20px; }',
            '        header { text-align: center; display: flex; flex-direction: column; gap: 8px; }',
            '        h1 { font-size: 1.4rem; font-weight: 700; }',
            '        .status-row { display: flex; align-items: center; justify-content: center; gap: 8px; }',
            '        .status-badge { display: inline-flex; align-items: center; gap: 8px; padding: 6px 14px; border-radius: 30px; font-size: 0.85rem; font-weight: 600; background-color: #fee2e2; color: var(--error); transition: all 0.3s; }',
            '        .status-badge.connected { background-color: #d1fae5; color: var(--success); }',
            '        .status-dot { width: 8px; height: 8px; border-radius: 50%; background-color: currentColor; }',
            '        .btn-settings { background: #e2e8f0; border: none; color: var(--text-dark); padding: 6px 12px; border-radius: 30px; font-size: 0.8rem; font-weight: 600; cursor: pointer; }',
            '        #reader { border: none !important; border-radius: 16px; overflow: hidden; background: #000; width: 100%; }',
            '        #reader button { background-color: var(--primary) !important; color: white !important; border: none !important; padding: 10px 18px !important; border-radius: 8px !important; cursor: pointer; margin-top: 10px; font-weight: 600; }',
            '        #reader select { padding: 8px !important; border-radius: 6px !important; margin-top: 5px; }',
            '        .history-box { background: var(--bg-main); border-radius: 12px; padding: 14px; width: 100%; }',
            '        .history-title { font-size: 0.8rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700; margin-bottom: 8px; }',
            '        .history-list { list-style: none; max-height: 120px; overflow-y: auto; font-size: 0.95rem; }',
            '        .history-item { display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #e2e8f0; font-family: monospace; }',
            '        .history-timestamp { color: var(--text-muted); font-size: 0.8rem; }',
            '        .security-alert { background-color: #ffedd5; border: 1px solid #f97316; color: var(--warning); padding: 10px 14px; border-radius: 12px; font-size: 0.88rem; line-height: 1.4; margin-bottom: 16px; max-width: 480px; width: 100%; cursor: pointer; user-select: none; }',
            '        .alert-header { display: flex; justify-content: space-between; align-items: center; font-weight: 600; }',
            '        .alert-content { margin-top: 12px; display: none; border-top: 1px dashed #f97316; padding-top: 10px; }',
            '        .alert-content.expanded { display: block; }',
            '    </style>',
            '</head>',
            '<body>',
            '    <div id="http-warning-banner" class="security-alert" style="display: none;" onclick="toggleAlertBanner()">',
            '        <div class="alert-header">',
            '            <span>⚠️ Mobile Camera Security Setup Help</span>',
            '            <span id="alert-chevron">▼</span>',
            '        </div>',
            '        <div id="http-warning-content" class="alert-content">',
            '            Browsers block mobile cameras on insecure local <code>http://</code> connections.<br><br>',
            '            <strong>To bypass and unlock camera on Android Chrome:</strong><br>',
            '            1. Open a new tab and go to:<br><code style="background:#fed7aa; padding:2px 4px; border-radius:4px;">chrome://flags/#unsafely-treat-insecure-origin-as-secure</code><br>',
            '            2. Set it to <strong>Enabled</strong>.<br>',
            '            3. Add this exact link into the text input area: <br><strong id="flag-link"></strong><br>',
            '            4. Tap <strong>Relaunch</strong> at the bottom of Chrome.',
            '        </div>',
            '    </div>',
            '    <div class="app-container">',
            '        <header>',
            '            <h1>Barcode Terminal</h1>',
            '            <div class="status-row">',
            '                <div id="status-container" class="status-badge">',
            '                    <div class="status-dot"></div>',
            '                    <span id="status-text">Connecting...</span>',
            '                </div>',
            '                <button class="btn-settings" onclick="changeIP()">Change IP</button>',
            '            </div>',
            '        </header>',
            '        <div id="reader"></div>',
            '        <div class="history-box">',
            '            <div class="history-title">Recent Scans</div>',
            '            <ul id="history-list" class="history-list">',
            '                <li style="color: var(--text-muted); font-style: italic; font-size: 0.85rem;">No codes scanned yet</li>',
            '            </ul>',
            '        </div>',
            '    </div>',
            '    <script>',
            '        const statusContainer = document.getElementById("status-container");',
            '        const statusText = document.getElementById("status-text");',
            '        const historyList = document.getElementById("history-list");',
            '        let ws, lastScannedCode = "", lastScanTime = 0;',
            '        const COOLDOWN_MS = 2500;',
            '',
            '        if (window.location.protocol !== "https:" && window.location.hostname !== "localhost" && window.location.hostname !== "127.0.0.1") {',
            '            document.getElementById("http-warning-banner").style.display = "block";',
            '            document.getElementById("flag-link").innerText = window.location.origin;',
            '            ',
            '            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {',
            '                document.getElementById("http-warning-content").classList.add("expanded");',
            '                document.getElementById("alert-chevron").innerText = "▲";',
            '            }',
            '        }',
            '',
            '        function toggleAlertBanner() {',
            '            const content = document.getElementById("http-warning-content");',
            '            const chevron = document.getElementById("alert-chevron");',
            '            if (content.classList.contains("expanded")) {',
            '                content.classList.remove("expanded");',
            '                chevron.innerText = "▼";',
            '            } else {',
            '                content.classList.add("expanded");',
            '                chevron.innerText = "▲";',
            '            }',
            '        }',
            '',
            '        function getSavedIP() {',
            '            let savedIP = localStorage.getItem("pc_target_ip");',
            '            if (savedIP && savedIP.trim() !== "") return savedIP;',
            '            let hostIP = window.location.hostname;',
            '            if (hostIP && hostIP !== "localhost" && hostIP !== "127.0.0.1") {',
            '                localStorage.setItem("pc_target_ip", hostIP);',
            '                return hostIP;',
            '            }',
            '            localStorage.setItem("pc_target_ip", "TARGET_PC_IP");',
            '            return "TARGET_PC_IP";',
            '        }',
            '',
            '        function connectWebSocket() {',
            '            const pcIP = getSavedIP();',
            '            statusText.innerText = "Connecting...";',
            '            if (ws) ws.close();',
            '            ws = new WebSocket("ws://" + pcIP + ":8765");',
            '            ws.onopen = () => {',
            '                statusText.innerText = "Connected to PC";',
            '                statusContainer.classList.add("connected");',
            '            };',
            '            ws.onerror = () => {',
            '                statusText.innerText = "Connection Failed";',
            '                statusContainer.classList.remove("connected");',
            '            };',
            '            ws.onclose = () => { statusContainer.classList.remove("connected"); };',
            '        }',
            '',
            '        function changeIP() {',
            '            let currentIP = localStorage.getItem("pc_target_ip") || "TARGET_PC_IP";',
            '            let newIP = prompt("Enter Windows PC IP Address manually:", currentIP);',
            '            if (newIP && newIP.trim() !== "") {',
            '                localStorage.setItem("pc_target_ip", newIP.trim());',
            '                connectWebSocket();',
            '            }',
            '        }',
            '',
            '        function playBeep() {',
            '            try {',
            '                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();',
            '                const oscillator = audioCtx.createOscillator();',
            '                const gainNode = audioCtx.createGain();',
            '                oscillator.type = "sine";',
            '                oscillator.frequency.setValueAtTime(1200, audioCtx.currentTime);',
            '                gainNode.gain.setValueAtTime(0.15, audioCtx.currentTime);',
            '                oscillator.connect(gainNode);',
            '                gainNode.connect(audioCtx.destination);',
            '                oscillator.start();',
            '                oscillator.stop(audioCtx.currentTime + 0.08);',
            '            } catch (e) { console.warn(e); }',
            '        }',
            '',
            '        function addScanToLog(text) {',
            '            if (historyList.children.length === 1 && historyList.children[0].style.fontStyle) historyList.innerHTML = "";',
            '            const timeStr = new Date().toTimeString().split(" ")[0];',
            '            const li = document.createElement("li");',
            '            li.className = "history-item";',
            '            li.innerHTML = "<span>" + text + "</span><span class=\'history-timestamp\'>" + timeStr + "</span>";',
            '            historyList.insertBefore(li, historyList.firstChild);',
            '        }',
            '',
            '        function onScanSuccess(decodedText) {',
            '            const currentTime = Date.now();',
            '            if (decodedText === lastScannedCode && (currentTime - lastScanTime) < COOLDOWN_MS) return;',
            '            lastScannedCode = decodedText;',
            '            lastScanTime = currentTime;',
            '            if (ws && ws.readyState === WebSocket.OPEN) {',
            '                ws.send(decodedText);',
            '                addScanToLog(decodedText);',
            '                playBeep();',
            '                if (navigator.vibrate) navigator.vibrate(120);',
            '            }',
            '        }',
            '',
            '        connectWebSocket();',
            '        let html5QrcodeScanner = new Html5QrcodeScanner("reader", {',
            '            fps: 20,',
            '            qrbox: function(w, h) { return { width: Math.floor(w * 0.8), height: Math.floor(h * 0.4) } },',
            '            rememberLastUsedCamera: true',
            '        });',
            '        html5QrcodeScanner.render(onScanSuccess);',
            '    </script>',
            '</body>',
            '</html>'
        ]
        
        html_content = "\n".join(html_lines).replace("TARGET_PC_IP", pc_ip)
        with open("barcode_server.html", "w", encoding="utf-8") as f:
            f.write(html_content)

    def create_widgets(self):
        title_lbl = tk.Label(
            self.root, 
            text="WIRELESS BARCODE SERVER", 
            font=("Helvetica", 14, "bold"), 
            bg="#1e293b", 
            fg="#ffffff", 
            pady=12
        )
        title_lbl.pack(fill=tk.X)
        
        panel = tk.Frame(self.root, bg="#ffffff", bd=1, relief=tk.SOLID)
        panel.pack(fill=tk.X, padx=16, pady=16)
        
        ip_title = tk.Label(
            panel, 
            text=f">>> TARGET PC IP ADDRESS: {self.pc_ip}", 
            font=("Consolas", 11, "bold"), 
            bg="#ffffff", 
            fg="#1e293b"
        )
        ip_title.pack(anchor="w", padx=12, pady=(12, 4))
        
        link_lbl = tk.Label(
            panel, 
            text="Visit this link with your mobile phone:", 
            font=("Helvetica", 10), 
            bg="#ffffff", 
            fg="#64748b"
        )
        link_lbl.pack(anchor="w", padx=12)
        
        url_box = tk.Label(
            panel, 
            text=f"http://{self.pc_ip}:8000", 
            font=("Consolas", 13, "bold"), 
            bg="#d1fae5", 
            fg="#065f46", 
            padx=10, 
            pady=8, 
            relief=tk.FLAT
        )
        url_box.pack(fill=tk.X, padx=12, pady=(6, 8))

        notice_lbl = tk.Label(
            panel, 
            text="⚠️ Note: Make sure the PC and mobile device are on the same local network.", 
            font=("Helvetica", 9, "bold"), 
            bg="#ffffff", 
            fg="#b45309", 
            wraplength=460, 
            justify=tk.LEFT
        )
        notice_lbl.pack(anchor="w", padx=12, pady=(0, 12))

        log_title = tk.Label(
            self.root, 
            text="System Activity Streaming Log:", 
            font=("Helvetica", 10, "bold"), 
            bg="#f1f5f9", 
            fg="#475569"
        )
        log_title.pack(anchor="w", padx=16)
        
        self.txt_log = scrolledtext.ScrolledText(
            self.root, 
            height=14, 
            font=("Consolas", 10), 
            bg="#1e293b", 
            fg="#f8fafc", 
            insertbackground="white"
        )
        self.txt_log.pack(fill=tk.BOTH, expand=True, padx=16, pady=(4, 12))
        self.write_log("System running. Awaiting dynamic connection handshakes...")

        footer = tk.Frame(self.root, bg="#e2e8f0")
        footer.pack(fill=tk.X, side=tk.BOTTOM, ipady=6)
        
        dev_lbl = tk.Label(
            footer, 
            text="Developed by Wohan", 
            font=("Helvetica", 9), 
            bg="#e2e8f0", 
            fg="#4f46e5"
        )
        dev_lbl.pack(side=tk.LEFT, padx=10)
        
        info_lbl = tk.Label(
            footer, 
            text="Help & Doubts", 
            font=("Helvetica", 9, "underline"), 
            bg="#e2e8f0", 
            fg="#475569", 
            cursor="hand2"
        )
        info_lbl.pack(side=tk.RIGHT, padx=10)
        info_lbl.bind("<Button-1>", lambda event: webbrowser.open("https://wa.me/+94771599229"))

    def write_log(self, text):
        if hasattr(self, 'txt_log'):
            self.root.after(0, lambda: self.txt_log.insert(tk.END, f"{text}\n"))
            self.root.after(0, self.txt_log.see, tk.END)

    def start_servers(self):
        def run_http():
            class QuietHandler(SimpleHTTPRequestHandler):
                def log_message(self, format, *args): 
                    return
                def do_GET(self):
                    if self.path == '/':
                        self.path = '/barcode_server.html'
                    return super().do_GET()
            try:
                httpd = ThreadingHTTPServer(('0.0.0.0', 8000), QuietHandler)
                httpd.serve_forever()
            except Exception as e:
                self.write_log(f"[SERVER ERROR] Web UI failed: {e}")
            
        threading.Thread(target=run_http, daemon=True).start()
        
        async def handle_barcode(websocket):
            self.write_log(f"[INFO] Mobile Device Connected Successfully.")
            async for message in websocket:
                self.write_log(f"[SCANNED] Received Value: {message}")
                pyautogui.write(message)
                pyautogui.press('enter')

        async def run_ws():
            try:
                async with websockets.serve(handle_barcode, "0.0.0.0", 8765):
                    await asyncio.Future()
            except Exception as e:
                self.write_log(f"[SERVER ERROR] Websocket system failed: {e}")

        def start_async_loop():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(run_ws())

        threading.Thread(target=start_async_loop, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = BarcodeServerApp(root)
    root.mainloop()
