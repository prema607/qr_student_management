from app import app
from models.admin import Admin
from database.db import db

with app.app_context():
    admin = Admin.query.filter_by(username="admin").first()

    if admin:
        admin.set_password("admin123")
        db.session.commit()
        print("Admin password reset successfully.")
        print("Username: admin")
        print("Password: admin123")
    else:
        print("Admin user not found.")