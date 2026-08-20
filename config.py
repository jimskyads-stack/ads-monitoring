"""
Configuration management for ADS Monitoring Bot
Centralized settings with environment variable support
"""
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ===========================
# BASE PATHS
# ===========================
BASE_DIR = Path(__file__).resolve().parent
CREDENTIALS_DIR = BASE_DIR / "credentials"
DATABASE_DIR = BASE_DIR / "database"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
for directory in [CREDENTIALS_DIR, DATABASE_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# ===========================
# CREDENTIALS & DATABASE
# ===========================
SERVICE_ACCOUNT = CREDENTIALS_DIR / "service_account.json"
DATABASE_NAME = DATABASE_DIR / "history.db"

# ===========================
# TELEGRAM BOT
# ===========================
BOT_TOKEN = os.getenv("BOT_TOKEN", "8766536073:AAH53KI5q9CUOze2RAxSLpA0gnek1Dx_hLI")

# ===========================
# GOOGLE SHEETS
# ===========================
DATABASE_SPREADSHEET = "ADS Monitoring Database"
REPORT_SPREADSHEET = "ADS Monitoring Reports"

TEAM_SPREADSHEETS = {
    "Team A": "ADS Campaign Encoder - Team A",
    "Team B": "ADS Campaign Encoder - Team B",
    "Team C1": "ADS Campaign Encoder - Team C1",
    "Team C2": "ADS Campaign Encoder - Team C2",
}

# ===========================
# MONITORING SETTINGS
# ===========================
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 30))
REMINDER_INTERVAL = int(os.getenv("REMINDER_INTERVAL", 30))
DEFAULT_MIN_SPEND_NO_RESULTS = float(os.getenv("MIN_SPEND_NO_RESULTS", 30))
DEFAULT_STALE_MINUTES = int(os.getenv("STALE_MINUTES", 30))
DEFAULT_CPA_SPIKE_PERCENT = float(os.getenv("CPA_SPIKE_PERCENT", 40))

# ===========================
# FLASK APP
# ===========================
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "ads-monitor-secret-key-change-in-production")
FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
