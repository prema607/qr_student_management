from database.db import db

from models.student import Student
from models.scan_log import ScanLog


class DashboardService:

    @staticmethod
    def get_dashboard_data():

        total_students = Student.query.count()

        active_students = Student.query.filter_by(
            status="Active"
        ).count()

        inactive_students = Student.query.filter_by(
            status="Inactive"
        ).count()

        total_departments = db.session.query(
            Student.department
        ).distinct().count()

        total_scans = ScanLog.query.count()

        recent_students = Student.query.order_by(
            Student.created_at.desc()
        ).limit(5).all()

        recent_scans = ScanLog.query.order_by(
            ScanLog.scan_time.desc()
        ).limit(5).all()

        department_stats = db.session.query(

            Student.department,

            db.func.count(Student.id)

        ).group_by(

            Student.department

        ).all()

        return {

            "total": total_students,

            "active": active_students,

            "inactive": inactive_students,

            "departments": total_departments,

            "total_scans": total_scans,

            "recent_students": recent_students,

            "recent_scans": recent_scans,

            "department_stats": department_stats

        }