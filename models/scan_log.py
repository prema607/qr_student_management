from datetime import datetime

from database.db import db


class ScanLog(db.Model):

    __tablename__ = "scan_logs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )
    student = db.relationship(
    "Student",
    backref="scan_logs"
    )
    scan_time = db.Column(
        db.DateTime,
        default=datetime.now
    )

    status = db.Column(
        db.String(30),
        nullable=False
    )

    location = db.Column(
        db.String(100)
    )