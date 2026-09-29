from sqlalchemy import or_

from database.db import db
from models.student import Student


class StudentService:

    @staticmethod
    def get_all_students(search=None):

        query = Student.query

        if search:

            search = search.strip()

            query = query.filter(

                or_(

                    Student.name.ilike(f"%{search}%"),

                    Student.rollno.ilike(f"%{search}%"),

                    Student.department.ilike(f"%{search}%")

                )

            )

        return query.order_by(Student.name.asc()).all()

    @staticmethod
    def get_student(rollno):

        return Student.query.filter_by(
            rollno=rollno
        ).first()

    @staticmethod
    def get_student_by_email(email):

        return Student.query.filter_by(
            email=email
        ).first()

    @staticmethod
    def save(student):

        db.session.add(student)

        db.session.commit()

    @staticmethod
    def delete(student):

        db.session.delete(student)

        db.session.commit()

    @staticmethod
    def total_students():

        return Student.query.count()

    @staticmethod
    def active_students():

        return Student.query.filter_by(
            status="Active"
        ).count()

    @staticmethod
    def inactive_students():

        return Student.query.filter_by(
            status="Inactive"
        ).count()

    @staticmethod
    def total_departments():

        return db.session.query(
            Student.department
        ).distinct().count()

    @staticmethod
    def recent_students(limit=5):

        return Student.query.order_by(

            Student.created_at.desc()

        ).limit(limit).all()

    @staticmethod
    def department_counts():

        result = db.session.query(

            Student.department,

            db.func.count(Student.id)

        ).group_by(

            Student.department

        ).all()

        return result
