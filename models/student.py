from datetime import datetime
from database.db import db


class Student(db.Model):

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.String(30), unique=True)

    name = db.Column(db.String(100), nullable=False)

    rollno = db.Column(db.String(30), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True)

    phone = db.Column(db.String(15))

    parent_phone = db.Column(db.String(15))

    department = db.Column(db.String(100))

    year = db.Column(db.String(20))

    section = db.Column(db.String(10))

    blood_group = db.Column(db.String(5))

    address = db.Column(db.Text)

    photo = db.Column(db.String(255))

    qr_code = db.Column(db.String(255))

    status = db.Column(db.String(20), default="Active")

    created_at = db.Column(db.DateTime, default=datetime.now)

    updated_at = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now
    )