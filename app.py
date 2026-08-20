"""
Flask application initialization and configuration
Main entry point for the ADS Monitoring Dashboard
"""
import os
import sys
from pathlib import Path

from flask import Flask, render_template
from flask_login import LoginManager
from models.user import User
from services.socket_manager import socketio
from dashboard.auth import role_required
from dashboard.routes import register_routes

# ===========================
# PROJECT SETUP
# ===========================
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ===========================
# FLASK APP CONFIGURATION
# ===========================
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.config['SECRET_KEY'] = os.getenv(
    "FLASK_SECRET_KEY",
    "ads-monitor-secret-key"
)

# Initialize Socket.IO
socketio.init_app(app)

# ===========================
# LOGIN MANAGER
# ===========================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Default users (should be moved to database)
DEFAULT_USERS = {
    "admin": {
        "password": "admin123",
        "role": "Admin"
    },
    "supervisor": {
        "password": "super123",
        "role": "Supervisor"
    }
}


@login_manager.user_loader
def load_user(username):
    """Load user from session"""
    if username in DEFAULT_USERS:
        return User(
            username,
            DEFAULT_USERS[username]["role"]
        )
    return None


# ===========================
# ROUTE REGISTRATION
# ===========================
register_routes(app)

# ===========================
# ERROR HANDLERS
# ===========================
@app.errorhandler(403)
def forbidden(error):
    """Handle 403 Forbidden errors"""
    return render_template("403.html"), 403


@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors"""
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server errors"""
    return render_template("500.html"), 500


# ===========================
# APP ENTRY POINT
# ===========================
if __name__ == "__main__":
    socketio.run(
        app,
        host=os.getenv("FLASK_HOST", "0.0.0.0"),
        port=int(os.getenv("FLASK_PORT", 5000)),
        debug=os.getenv("FLASK_DEBUG", "True").lower() == "true"
    )
