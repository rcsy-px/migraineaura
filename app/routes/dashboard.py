from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.services.event_service import dashboard_stats

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    return redirect(url_for("auth.login"))


@dashboard_bp.route("/dashboard")
@login_required
def index():
    stats = dashboard_stats(current_user.id)
    return render_template("dashboard/index.html", **stats)
