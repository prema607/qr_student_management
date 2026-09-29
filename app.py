import os

from flask import Flask, render_template
from flask_login import login_required

from config import Config
from database.db import db, login_manager

# Models
from models.admin import Admin

# Services
from services.dashboard_service import DashboardService

# Blueprints
from routes.auth import auth_bp
from routes.student import student_bp
from routes.admin import admin_bp

# Mail
from extensions import mail


# =====================================================
# APP CONFIGURATION
# =====================================================

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
mail.init_app(app)
login_manager.init_app(app)

login_manager.login_view = "auth.login"
login_manager.login_message = "Please login to continue."
login_manager.login_message_category = "warning"


# =====================================================
# LOGIN MANAGER
# =====================================================

@login_manager.user_loader
def load_user(user_id):

    return Admin.query.get(int(user_id))


# =====================================================
# REGISTER BLUEPRINTS
# =====================================================

app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(admin_bp)


# =====================================================
# DEBUG ROUTES
# =====================================================

print("\n========== REGISTERED ROUTES ==========")

for rule in app.url_map.iter_rules():

    print(f"{rule.endpoint:35} -> {rule.rule}")

print("=======================================\n")


# =====================================================
# HOME
# =====================================================

@app.route("/")
def home():

    return render_template("index.html")


# =====================================================
# DASHBOARD
# =====================================================

@app.route("/dashboard")
@login_required
def dashboard():

    data = DashboardService.get_dashboard_data()

    return render_template(
        "dashboard.html",
        **data
    )


# =====================================================
# ERROR PAGES
# =====================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "errors/404.html"
    ), 404


@app.errorhandler(500)
def server_error(error):

    db.session.rollback()

    return render_template(
        "errors/500.html"
    ), 500


# =====================================================
# DEFAULT ADMIN
# =====================================================

def create_default_admin():

    # Get the email configured in .env
    admin_email = app.config.get("MAIL_USERNAME")

    if not admin_email:

        print("\n======================================")
        print("WARNING: MAIL_USERNAME is not configured.")
        print("Please check your .env file.")
        print("======================================\n")

        return

    admin = Admin.query.filter_by(
        username="admin"
    ).first()

    # -------------------------------------------------
    # If admin already exists, update the email
    # -------------------------------------------------

    if admin:

        if admin.email != admin_email:

            admin.email = admin_email

            db.session.commit()

            print("\n======================================")
            print("Existing Admin Email Updated")
            print("Username :", admin.username)
            print("Email    :", admin.email)
            print("======================================\n")

        else:

            print("\n======================================")
            print("Admin Already Exists")
            print("Username :", admin.username)
            print("Email    :", admin.email)
            print("======================================\n")

        return

    # -------------------------------------------------
    # Create admin if it does not exist
    # -------------------------------------------------

    admin = Admin(
        username="admin",
        email=admin_email
    )

    admin.set_password("admin123")

    db.session.add(admin)

    db.session.commit()

    print("\n======================================")
    print("Default Admin Created")
    print("Username :", admin.username)
    print("Email    :", admin.email)
    print("Password : admin123")
    print("======================================\n")


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

        create_default_admin()

        os.makedirs(
            app.config["UPLOAD_FOLDER"],
            exist_ok=True
        )

        os.makedirs(
            app.config["QR_FOLDER"],
            exist_ok=True
        )

    app.run(
        debug=True
    )