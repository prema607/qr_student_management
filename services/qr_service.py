import os
import qrcode

from flask import current_app


class QRService:

    @staticmethod
    def generate_qr(rollno):

        url = f"{current_app.config['SERVER_URL']}/student/profile/{rollno}"

        img = qrcode.make(url)

        filename = f"{rollno}.png"

        path = os.path.join(
            current_app.config["QR_FOLDER"],
            filename
        )

        img.save(path)

        return filename