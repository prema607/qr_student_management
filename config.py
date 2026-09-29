
import os

from dotenv import load_dotenv


# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================

load_dotenv()


# =====================================================
# BASE DIRECTORY
# =====================================================

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)


# =====================================================
# APPLICATION CONFIGURATION
# =====================================================

class Config:

    # -------------------------------------------------
    # Flask Secret Key
    # -------------------------------------------------

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-secret-key-change-this"
    )


    # -------------------------------------------------
    # Database
    # -------------------------------------------------

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///"
        + os.path.join(
            BASE_DIR,
            "database",
            "students.db"
        )
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # -------------------------------------------------
    # Student Photo Upload Configuration
    # -------------------------------------------------

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "static",
        "photos"
    )


    # -------------------------------------------------
    # QR Code Configuration
    # -------------------------------------------------

    QR_FOLDER = os.path.join(
        BASE_DIR,
        "static",
        "qr_codes"
    )


    # -------------------------------------------------
    # File Upload Limit
    # Maximum: 5 MB
    # -------------------------------------------------

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024


    # -------------------------------------------------
    # Allowed Image Extensions
    # -------------------------------------------------

    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg"
    }


    # -------------------------------------------------
    # Server URL
    # Used for QR code links
    # -------------------------------------------------

    SERVER_URL = os.getenv(
        "SERVER_URL",
        "https://onlooker-remote-unturned.ngrok-free.dev"
    )


    # =================================================
    # GMAIL / FLASK-MAIL CONFIGURATION
    # =================================================

    MAIL_SERVER = "smtp.gmail.com"

    MAIL_PORT = 587

    MAIL_USE_TLS = True

    MAIL_USE_SSL = False


    # Gmail account used to send emails
    MAIL_USERNAME = os.getenv(
        "MAIL_USERNAME"
    )


    # Gmail App Password
    MAIL_PASSWORD = os.getenv(
        "MAIL_PASSWORD"
    )


    # Default sender
    MAIL_DEFAULT_SENDER = (
        "CampusConnect <"
        + os.getenv(
            "MAIL_USERNAME",
            "noreply@example.com"
        )
        + ">"
    )

