"""
IoT Phishing Attack Simulation — Utility Functions
====================================================
Helper functions for credential logging, IP extraction, QR generation, and statistics.
"""

import os
import io
import base64
from datetime import datetime
from config import LOG_FILE


def get_client_ip(request):
    """Extract client IP address with reverse-proxy awareness."""
    forwarded = request.headers.get('X-Forwarded-For')
    if forwarded:
        return forwarded.split(',')[0].strip()
    real_ip = request.headers.get('X-Real-IP')
    if real_ip:
        return real_ip.strip()
    return request.remote_addr or '127.0.0.1'


def log_credentials(username, password, scenario, ip, demo=False):
    """
    Log captured credentials with timestamp, IP, and scenario metadata.
    In demo mode, prints to console instead of writing to file.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = (
        f"[{timestamp}] "
        f"IP: {ip} | "
        f"Scenario: {scenario} | "
        f"Username: {username} | "
        f"Password: {password}\n"
    )

    if demo:
        print(f"[DEMO LOG] {entry.strip()}")
        return

    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(entry)
    except IOError as e:
        print(f"[ERROR] Failed to write log: {e}")


def get_log_stats():
    """
    Parse credentials.txt and return structured statistics.
    Returns dict with total count, per-scenario breakdown, entries list, and last entry.
    """
    stats = {
        'total': 0,
        'entries': [],
        'by_scenario': {'storage': 0, 'warranty': 0, 'security': 0},
        'last_entry': None,
        'last_timestamp': 'No captures yet'
    }

    if not os.path.exists(LOG_FILE):
        return stats

    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except IOError:
        return stats

    for line in lines:
        line = line.strip()
        if not line:
            continue

        stats['total'] += 1

        # Parse entry into structured dict
        entry = {'raw': line}
        try:
            # Extract timestamp
            ts_start = line.index('[') + 1
            ts_end = line.index(']')
            entry['timestamp'] = line[ts_start:ts_end]

            # Extract fields
            parts = line[ts_end + 2:].split(' | ')
            for part in parts:
                key, _, value = part.partition(': ')
                entry[key.strip().lower()] = value.strip()
        except (ValueError, IndexError):
            entry['timestamp'] = 'Unknown'

        stats['entries'].append(entry)

        # Count by scenario
        for scenario_key in stats['by_scenario']:
            if f'Scenario: {scenario_key}' in line:
                stats['by_scenario'][scenario_key] += 1
                break

    if stats['entries']:
        stats['last_entry'] = stats['entries'][-1]
        stats['last_timestamp'] = stats['entries'][-1].get('timestamp', 'Unknown')

    return stats


def clear_logs():
    """Clear the credentials log file."""
    try:
        open(LOG_FILE, 'w').close()
        return True
    except IOError:
        return False


def generate_qr(url):
    """
    Generate a QR code for the given URL, returned as a base64-encoded PNG string.
    Returns None if the qrcode library is not installed.
    """
    try:
        import qrcode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')

        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    except ImportError:
        print("[WARN] qrcode library not installed. Run: pip install qrcode[pil]")
        return None
