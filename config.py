"""
IoT Phishing Attack Simulation — Configuration
================================================
Central configuration for scenarios, demo mode, and application settings.
"""

SECRET_KEY = 'iot-phishing-sim-2026-edu-key'

# Set to True for safe demonstrations (logs to console only, shows DEMO watermark)
DEMO_MODE = False

# Credential log file path
LOG_FILE = 'credentials.txt'

# Network binding — set HOST to '0.0.0.0' for LAN demos, '127.0.0.1' for local only
HOST = '127.0.0.1'
PORT = 5000

# Attack scenario definitions
SCENARIOS = {
    'storage': {
        'id': 'storage',
        'name': 'IoT Cloud Storage Attack',
        'menu_label': '[1] IoT Cloud Storage Phishing',
        'hook': 'reward',
        'headline': 'Your IoT Cloud Storage is 95% Full',
        'subheadline': 'Upgrade to Premium Storage — Completely FREE',
        'urgency': 'Limited time offer — expires in 24 hours',
        'cta_text': 'Upgrade Now — Free',
        'brand_name': 'SmartCloud IoT',
        'device_name': 'SmartCloud Hub Pro v3.2',
        'color': '#1a73e8',
        'icon': '☁️',
        'description': 'Lures victim with a free cloud storage upgrade offer for their IoT devices.'
    },
    'warranty': {
        'id': 'warranty',
        'name': 'Device Warranty Expiry Attack',
        'menu_label': '[2] Device Warranty Expiry Phishing',
        'hook': 'fear',
        'headline': '⚠️ Your Device Warranty Expires Tomorrow',
        'subheadline': 'Renew now to keep your devices protected',
        'urgency': 'Renew before expiry to avoid $149 service charges',
        'cta_text': 'Renew Warranty Now',
        'brand_name': 'HomeGuard IoT',
        'device_name': 'HomeGuard Security System v2.8',
        'color': '#ea4335',
        'icon': '🛡️',
        'description': 'Exploits fear of warranty loss and unexpected service charges.'
    },
    'security': {
        'id': 'security',
        'name': 'Critical Security Update Attack',
        'menu_label': '[3] Critical Security Update Phishing',
        'hook': 'authority',
        'headline': 'Critical Security Patch Required',
        'subheadline': 'A vulnerability has been detected on your device',
        'urgency': 'Immediate action required — CVE-2026-4821 detected',
        'cta_text': 'Install Security Patch',
        'brand_name': 'SecureNet IoT',
        'device_name': 'SecureNet Gateway v4.1',
        'color': '#f9ab00',
        'icon': '🔒',
        'description': 'Uses authority and urgency of a fake security vulnerability to compel login.'
    }
}
