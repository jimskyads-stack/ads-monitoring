"""
Dashboard routes and endpoints
Main route handlers for the ADS Monitoring Dashboard
"""
from flask import (
    render_template,
    jsonify,
    request,
    redirect,
    url_for
)
from flask_login import (
    login_user,
    current_user,
    login_required,
    logout_user
)

from models.user import User
from services.dashboard_service import DashboardService
from services.alert_history_service import AlertHistoryService
from services.settings_dashboard_service import SettingsDashboardService
from services.user_service import UserService
from services.audit_service import AuditService
from dashboard.auth import role_required
from database.alert_repository import AlertRepository

# ===========================
# SERVICE INITIALIZATION
# ===========================
alert_repo = AlertRepository()
audit_service = AuditService()
user_service = UserService()
dashboard_service = DashboardService()
alert_service = AlertHistoryService()
settings_service = SettingsDashboardService()

# Default users (should be moved to database)
USERS = {
    "admin": {
        "password": "admin123",
        "role": "Admin"
    },
    "supervisor": {
        "password": "super123",
        "role": "Supervisor"
    }
}


def register_routes(app):
    """
    Register all routes for the Flask application
    
    Args:
        app: Flask application instance
    """

    # ===========================
    # AUTHENTICATION ROUTES
    # ===========================

    @app.route("/login", methods=["GET", "POST"])
    def login():
        """Handle user login"""
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            if username in USERS and USERS[username]["password"] == password:
                user = User(username, USERS[username]["role"])
                login_user(user)
                
                audit_service.log(
                    username,
                    "Login",
                    "User logged into the dashboard"
                )

                return redirect(url_for("dashboard"))

            return render_template(
                "login.html",
                error="Invalid username or password."
            )

        return render_template("login.html")

    @app.route("/logout")
    @login_required
    def logout():
        """Handle user logout"""
        logout_user()
        return redirect(url_for("login"))

    # ===========================
    # DASHBOARD ROUTES
    # ===========================

    @app.route("/")
    @login_required
    def dashboard():
        """Main dashboard page"""
        dashboard_data = dashboard_service.get_dashboard()
        return render_template(
            "dashboard.html",
            dashboard=dashboard_data
        )

    # ===========================
    # CAMPAIGNS ROUTES
    # ===========================

    @app.route("/campaigns")
    @login_required
    def campaigns():
        """List all campaigns"""
        dashboard_data = dashboard_service.get_dashboard()
        return render_template(
            "campaigns.html",
            campaigns=dashboard_data["campaigns"],
            dashboard=dashboard_data
        )

    # ===========================
    # ALERTS ROUTES
    # ===========================

    @app.route("/alerts")
    @login_required
    def alerts():
        """List all alerts"""
        dashboard_data = dashboard_service.get_dashboard()
        return render_template(
            "alerts.html",
            alerts=dashboard_data["alerts"]
        )

    @app.route("/alerts/acknowledge/<int:alert_id>")
    @login_required
    def acknowledge_alert(alert_id):
        """Acknowledge an alert"""
        alert_repo.acknowledge(alert_id, current_user.username)
        
        audit_service.log(
            current_user.username,
            "Acknowledge Alert",
            f"Alert #{alert_id}"
        )

        return redirect("/alerts")

    # ===========================
    # TEAMS ROUTES
    # ===========================

    @app.route("/teams")
    @login_required
    def teams():
        """List all teams"""
        dashboard_data = dashboard_service.get_dashboard()
        return render_template(
            "teams.html",
            teams=dashboard_data["teams"]
        )

    # ===========================
    # EMPLOYEES ROUTES
    # ===========================

    @app.route("/employees")
    @login_required
    def employees():
        """List all employees"""
        dashboard_data = dashboard_service.get_dashboard()
        return render_template(
            "employees.html",
            employees=dashboard_data["employees"]
        )

    # ===========================
    # REPORTS ROUTES
    # ===========================

    @app.route("/reports")
    @login_required
    def reports():
        """View reports"""
        dashboard_data = dashboard_service.get_dashboard()
        return render_template(
            "reports.html",
            summary=dashboard_data["summary"]
        )

    # ===========================
    # ANALYTICS ROUTES
    # ===========================

    @app.route("/analytics")
    @login_required
    def analytics():
        """View analytics"""
        dashboard_data = dashboard_service.get_dashboard()
        return render_template(
            "analytics.html",
            dashboard=dashboard_data
        )

    # ===========================
    # SETTINGS ROUTES
    # ===========================

    @app.route("/settings")
    @login_required
    @role_required("Admin")
    def settings():
        """Admin settings page"""
        settings_data = settings_service.get_settings()
        return render_template(
            "settings.html",
            settings=settings_data
        )

    # ===========================
    # AUDIT ROUTES
    # ===========================

    @app.route("/audit")
    @login_required
    @role_required("Admin")
    def audit():
        """View audit logs (Admin only)"""
        logs = audit_service.get_logs()
        return render_template("audit.html", logs=logs)

    # ===========================
    # USER MANAGEMENT ROUTES
    # ===========================

    @app.route("/users")
    @login_required
    @role_required("Admin")
    def users():
        """List all users (Admin only)"""
        users_list = user_service.get_users()
        return render_template("users.html", users=users_list)

    @app.route("/users/add", methods=["GET", "POST"])
    @login_required
    @role_required("Admin")
    def add_user():
        """Add new user (Admin only)"""
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            role = request.form["role"]

            success, message = user_service.add_user(
                username,
                password,
                role
            )

            if success:
                audit_service.log(
                    current_user.username,
                    "Create User",
                    username
                )
                return redirect("/users")

            return message

        return render_template("add_user.html")

    @app.route("/users/edit/<int:user_id>", methods=["GET", "POST"])
    @login_required
    @role_required("Admin")
    def edit_user(user_id):
        """Edit user (Admin only)"""
        user = user_service.get_user_by_id(user_id)

        if not user:
            return "User not found."

        if request.method == "POST":
            username = request.form["username"]
            role = request.form["role"]
            status = request.form["status"]

            user_service.update_user(
                user_id,
                username,
                role,
                status
            )

            return redirect("/users")

        return render_template("edit_user.html", user=user)

    @app.route("/users/password/<int:user_id>", methods=["GET", "POST"])
    def change_password(user_id):
        """Change user password"""
        user = user_service.get_user_by_id(user_id)

        if not user:
            return "User not found."

        if request.method == "POST":
            password = request.form["password"]
            user_service.update_password(user_id, password)
            return redirect("/users")

        return render_template("change_password.html", user=user)

    @app.route("/users/delete/<int:user_id>")
    @login_required
    @role_required("Admin")
    def delete_user(user_id):
        """Delete user (Admin only)"""
        user = user_service.get_user_by_id(user_id)

        if user and user["username"] == "admin":
            return "The default admin account cannot be deleted."

        user_service.delete_user(user_id)
        return redirect("/users")

    # ===========================
    # API ROUTES
    # ===========================

    @app.route("/api/dashboard")
    @login_required
    def api_dashboard():
        """API endpoint for dashboard data"""
        dashboard_data = dashboard_service.get_dashboard()
        return jsonify({
            "summary": dashboard_data["summary"],
            "alerts": dashboard_data["alerts"],
            "teams": dashboard_data["teams"],
            "employees": dashboard_data["employees"]
        })

    @app.route("/api/campaigns")
    @login_required
    def api_campaigns():
        """API endpoint for campaigns data"""
        dashboard_data = dashboard_service.get_dashboard()
        campaigns = []

        for c in dashboard_data["campaigns"]:
            campaigns.append({
                "team": c.team,
                "employee": c.employee,
                "offer": c.offer,
                "campaign": c.campaign,
                "spend": c.spend,
                "results": c.results,
                "cpa": c.cpa,
                "status": c.status,
                "last_updated": c.last_updated
            })

        return jsonify(campaigns)

    @app.route("/api/analytics")
    @login_required
    def api_analytics():
        """API endpoint for analytics data"""
        dashboard_data = dashboard_service.get_dashboard()
        alerts = dashboard_data["alerts"]

        alert_types = {}
        team_alerts = {}

        for alert in alerts:
            alert_type = alert["type"]
            team = alert["campaign"].team

            alert_types[alert_type] = alert_types.get(alert_type, 0) + 1
            team_alerts[team] = team_alerts.get(team, 0) + 1

        return jsonify({
            "alert_types": alert_types,
            "team_alerts": team_alerts
        })

    @app.route("/api/alerts/latest")
    @login_required
    def latest_alert():
        """API endpoint for latest alert"""
        alerts = alert_service.get_alerts()

        if not alerts:
            return jsonify({})

        return jsonify(dict(alerts[0]))
