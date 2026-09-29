from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from database.db import db


class Admin(UserMixin, db.Model):

    __tablename__ = "admins"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password,
            password
        )

    def generate_reset_token(self):

        serializer = URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"]
        )

        return serializer.dumps(
            self.email,
            salt="password-reset"
        )

    @staticmethod
    def verify_reset_token(token, max_age=1800):

        serializer = URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"]
        )

        try:

            email = serializer.loads(
                token,
                salt="password-reset",
                max_age=max_age
            )

        except (SignatureExpired, BadSignature):

            return None

        return Admin.query.filter_by(
            email=email
        ).first()