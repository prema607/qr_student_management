from flask import Blueprint, render_template
from flask_login import login_required, current_user

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


@admin_bp.route("/settings")
@login_required
def settings():

    return render_template(
        "admin/settings.html",
        admin=current_user
    )