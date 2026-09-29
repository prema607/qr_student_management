import os
import uuid

from flask import current_app
from werkzeug.utils import secure_filename


class FileHandler:

    @staticmethod
    def allowed_file(filename):

        if "." not in filename:
            return False

        extension = filename.rsplit(".", 1)[1].lower()

        return extension in current_app.config["ALLOWED_EXTENSIONS"]


    @staticmethod
    def save_photo(photo):

        if not photo or photo.filename == "":
            return None

        if not FileHandler.allowed_file(photo.filename):
            return None

        extension = photo.filename.rsplit(".", 1)[1].lower()

        filename = f"{uuid.uuid4().hex}.{extension}"

        filepath = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            filename
        )

        photo.save(filepath)

        return filename


    @staticmethod
    def delete_photo(filename):

        if not filename:
            return

        filepath = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            filename
        )

        if os.path.exists(filepath):
            os.remove(filepath)


    @staticmethod
    def delete_qr(filename):

        if not filename:
            return

        filepath = os.path.join(
            current_app.config["QR_FOLDER"],
            filename
        )

        if os.path.exists(filepath):
            os.remove(filepath)