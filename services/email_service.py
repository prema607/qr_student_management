from flask_mail import Message
from flask import current_app

from extensions import mail


class EmailService:

    @staticmethod
    def send_welcome_email(student):

        subject = "Welcome to CampusConnect"

        body = f"""
Hello {student.name},

Welcome to CampusConnect.

Your registration has been completed successfully.

Student Details

Name : {student.name}
Roll Number : {student.rollno}
Department : {student.department}
Year : {student.year}
Section : {student.section}

Please keep your QR Code safe for future verification.

Thank you.

CampusConnect
"""

        message = Message(
            subject=subject,
            sender=current_app.config["MAIL_USERNAME"],
            recipients=[student.email],
            body=body
        )

        mail.send(message)