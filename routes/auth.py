from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from models.admin import Admin
from database.db import db
from extensions import mail

from flask_mail import Message


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


# =====================================================
# LOGIN
# =====================================================

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        admin = Admin.query.filter_by(
            username=username
        ).first()

        if admin and admin.check_password(password):

            login_user(admin)

            return redirect(url_for("dashboard"))

        flash(
            "Invalid Username or Password",
            "danger"
        )

    return render_template(
        "auth/login.html"
    )


# =====================================================
# LOGOUT
# =====================================================

@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("auth.login")
    )


# =====================================================
# CHANGE PASSWORD
# =====================================================

@auth_bp.route(
    "/change-password",
    methods=["GET", "POST"]
)
@login_required
def change_password():

    if request.method == "POST":

        current_password = request.form[
            "current_password"
        ]

        new_password = request.form[
            "new_password"
        ]

        confirm_password = request.form[
            "confirm_password"
        ]

        if not current_user.check_password(
            current_password
        ):

            flash(
                "Current password is incorrect.",
                "danger"
            )

            return redirect(
                url_for("auth.change_password")
            )

        if new_password != confirm_password:

            flash(
                "New passwords do not match.",
                "danger"
            )

            return redirect(
                url_for("auth.change_password")
            )

        if len(new_password) < 6:

            flash(
                "New password must be at least 6 characters.",
                "danger"
            )

            return redirect(
                url_for("auth.change_password")
            )

        current_user.set_password(
            new_password
        )

        db.session.commit()

        flash(
            "Password changed successfully.",
            "success"
        )

        return redirect(
            url_for("admin.settings")
        )

    return render_template(
        "auth/change_password.html"
    )


# =====================================================
# FORGOT PASSWORD
# =====================================================

@auth_bp.route(
    "/forgot-password",
    methods=["GET", "POST"]
)
def forgot_password():

    if request.method == "POST":

        email = request.form[
            "email"
        ].strip().lower()

        admin = Admin.query.filter_by(
            email=email
        ).first()

        if admin:

            token = admin.generate_reset_token()

            reset_url = url_for(
                "auth.reset_password",
                token=token,
                _external=True
            )

            msg = Message(
                subject="CampusConnect - Password Reset",
                recipients=[admin.email]
            )

            msg.body = f"""
Hello {admin.username},

We received a request to reset your CampusConnect admin password.

Click the link below to reset your password:

{reset_url}

This link will expire in 30 minutes.

If you did not request a password reset, you can safely ignore this email.

Regards,
CampusConnect
"""

            try:

                mail.send(msg)

            except Exception as e:

                print(
                    "EMAIL ERROR:",
                    e
                )

                flash(
                    "Unable to send reset email. Please try again later.",
                    "danger"
                )

                return redirect(
                    url_for("auth.forgot_password")
                )

        # Do not reveal whether email exists
        flash(
            "If an account exists with that email, "
            "a password reset link has been sent.",
            "info"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "auth/forgot_password.html"
    )


# =====================================================
# RESET PASSWORD
# =====================================================

@auth_bp.route(
    "/reset-password/<token>",
    methods=["GET", "POST"]
)
def reset_password(token):

    admin = Admin.verify_reset_token(
        token
    )

    if admin is None:

        flash(
            "The password reset link is invalid or has expired.",
            "danger"
        )

        return redirect(
            url_for("auth.forgot_password")
        )

    if request.method == "POST":

        new_password = request.form[
            "new_password"
        ]

        confirm_password = request.form[
            "confirm_password"
        ]

        if len(new_password) < 6:

            flash(
                "Password must be at least 6 characters.",
                "danger"
            )

            return redirect(
                url_for(
                    "auth.reset_password",
                    token=token
                )
            )

        if new_password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger"
            )

            return redirect(
                url_for(
                    "auth.reset_password",
                    token=token
                )
            )

        admin.set_password(
            new_password
        )

        db.session.commit()

        flash(
            "Password reset successfully. You can now login.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "auth/reset_password.html"
    )