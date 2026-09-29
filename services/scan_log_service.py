from models.scan_log import ScanLog
from database.db import db


class ScanLogService:

    @staticmethod
    def save(log):

        db.session.add(log)
        db.session.commit()

    @staticmethod
    def get_all():

        return ScanLog.query.order_by(
            ScanLog.scan_time.desc()
        ).all()