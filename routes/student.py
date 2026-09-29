# from PIL.SpiderImagePlugin import filename
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
)
import os
import uuid

from models.student import Student
from models.scan_log import ScanLog

from services.student_service import StudentService
from services.qr_service import QRService
from services.scan_log_service import ScanLogService

from utils.file_handler import FileHandler
from utils.validators import Validator
from flask import send_file
from services.report_service import ReportService
from services.email_service import EmailService
student_bp = Blueprint(
    "student",
    __name__,
    url_prefix="/student"
)


# =====================================================
# REGISTER STUDENT
# =====================================================

@student_bp.route("/register")
def register_student():

    return render_template(
        "admin/register_student.html"
    )


@student_bp.route("/save", methods=["POST"])
def save_student():

    # ------------------------------
    # Validate Form
    # ------------------------------

    valid, message = Validator.validate_registration(
        request.form
    )

    if not valid:

        flash(message, "danger")

        return redirect(
            url_for("student.register_student")
        )

    rollno = request.form.get(
        "rollno"
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip()

    # ------------------------------
    # Duplicate Roll Number
    # ------------------------------

    if StudentService.get_student(rollno):

        flash(
            "Roll Number already exists.",
            "danger"
        )

        return redirect(
            url_for("student.register_student")
        )

    # ------------------------------
    # Duplicate Email
    # ------------------------------

    if email:

        existing = Student.query.filter_by(
            email=email
        ).first()

        if existing:

            flash(
                "Email already exists.",
                "danger"
            )

            return redirect(
                url_for("student.register_student")
            )

    # ------------------------------
    # Upload Photo
    # ------------------------------

    photo = request.files.get("photo")

    filename = FileHandler.save_photo(photo)

    if photo and filename is None:

        flash(
            "Only JPG, JPEG and PNG images are allowed.",
            "danger"
        )

        return redirect(
            url_for("student.register_student")
        )

    # ------------------------------
    # Create Student Object
    # ------------------------------

    student = Student(

        student_id=str(uuid.uuid4())[:8],

        name=request.form["name"].strip(),

        rollno=rollno,

        email=email,

        phone=request.form["phone"].strip(),

        parent_phone=request.form["parent_phone"].strip(),

        department=request.form["department"],

        year=request.form["year"],

        section=request.form["section"],

        blood_group=request.form["blood_group"],

        address=request.form["address"],

        photo=filename

    )

    try:

        qr = QRService.generate_qr(
            student.rollno
    )

        student.qr_code = qr

        StudentService.save(student)

    # ------------------------------
    # Send Welcome Email
    # ------------------------------

        if student.email:

            try:

                EmailService.send_welcome_email(student)

                flash(
                    "Student Registered Successfully. Welcome email sent.",
                    "success"
                )

            except Exception as e:

                print("Email Error :", e)

                flash(
                    "Student Registered Successfully, but email could not be sent.",
                    "warning"
                )

        else:

            flash(
                "Student Registered Successfully.",
                "success"
            )

        return redirect(
            url_for("student.student_list")
        )

    except Exception as e:

        FileHandler.delete_photo(filename)

        flash(
        f"Registration Failed: {e}",
        "danger"
    )

    return redirect(
        url_for("student.register_student")
    )

    

# =====================================================
# STUDENT LIST
# =====================================================

@student_bp.route("/list")
def student_list():

    search = request.args.get("search")

    students = StudentService.get_all_students(search)

    return render_template(
        "admin/student_list.html",
        students=students,
        search=search
    )
# =====================================================
# STUDENT PROFILE
# =====================================================

@student_bp.route("/profile/<rollno>")
def student_profile(rollno):

    student = StudentService.get_student(rollno)

    if student is None:

        flash(
            "Student not found.",
            "danger"
        )

        return redirect(
            url_for("student.student_list")
        )

    if student.status != "Active":

        return render_template(
            "security/verify.html",
            message="This Student ID is Inactive."
        )

    log = ScanLog(

        student_id=student.id,

        status="Success",

        location=request.remote_addr

    )

    ScanLogService.save(log)

    return render_template(
        "student/profile.html",
        student=student
    )


# =====================================================
# REGENERATE QR
# =====================================================

@student_bp.route("/regenerate_qr/<rollno>")
def regenerate_qr(rollno):

    student = StudentService.get_student(rollno)

    if student is None:

        flash(
            "Student not found.",
            "danger"
        )

        return redirect(
            url_for("student.student_list")
        )

    try:

        FileHandler.delete_qr(student.qr_code)

        qr = QRService.generate_qr(
            student.rollno
        )

        student.qr_code = qr

        StudentService.save(student)

        flash(
            "QR regenerated successfully.",
            "success"
        )

    except Exception as e:

        flash(
            f"QR generation failed : {e}",
            "danger"
        )

    return redirect(
        url_for("student.student_list")
    )


# =====================================================
# EDIT STUDENT
# =====================================================

@student_bp.route("/edit/<rollno>")
def edit_student(rollno):

    student = StudentService.get_student(rollno)

    if student is None:

        flash(
            "Student not found.",
            "danger"
        )

        return redirect(
            url_for("student.student_list")
        )

    return render_template(
        "admin/edit_student.html",
        student=student
    )


# =====================================================
# UPDATE STUDENT
# =====================================================

@student_bp.route("/update/<rollno>", methods=["POST"])
def update_student(rollno):

    student = StudentService.get_student(rollno)

    if student is None:

        flash(
            "Student not found.",
            "danger"
        )

        return redirect(
            url_for("student.student_list")
        )

    valid, message = Validator.validate_registration(
        request.form
    )

    if not valid:

        flash(
            message,
            "danger"
        )

        return redirect(
            url_for(
                "student.edit_student",
                rollno=rollno
            )
        )

    email = request.form.get(
        "email",
        ""
    ).strip()

    if email != (student.email or ""):

        existing = Student.query.filter_by(
            email=email
        ).first()

        if existing:

            flash(
                "Email already exists.",
                "danger"
            )

            return redirect(
                url_for(
                    "student.edit_student",
                    rollno=rollno
                )
            )

    student.name = request.form["name"].strip()
    student.email = email
    student.phone = request.form["phone"].strip()
    student.parent_phone = request.form["parent_phone"].strip()
    student.department = request.form["department"]
    student.year = request.form["year"]
    student.section = request.form["section"]
    student.blood_group = request.form["blood_group"]
    student.address = request.form["address"]

    photo = request.files.get("photo")
        # ------------------------------
    # Update Photo
    # ------------------------------

    if photo and photo.filename != "":

        filename = FileHandler.save_photo(photo)

        if filename is None:

            flash(
                "Only JPG, JPEG and PNG images are allowed.",
                "danger"
            )

            return redirect(
                url_for(
                    "student.edit_student",
                    rollno=rollno
                )
            )

        FileHandler.delete_photo(student.photo)

        student.photo = filename

    try:

        StudentService.save(student)

        flash(
            "Student updated successfully.",
            "success"
        )

    except Exception as e:

        flash(
            f"Update Failed : {e}",
            "danger"
        )

    return redirect(
        url_for("student.student_list")
    )


# =====================================================
# DELETE STUDENT
# =====================================================

@student_bp.route("/delete/<rollno>")
def delete_student(rollno):

    student = StudentService.get_student(rollno)

    if student is None:

        flash("Student not found.", "danger")

        return redirect(
            url_for("student.student_list")
        )

    try:

        # --------------------------------
        # Delete student's scan logs first
        # --------------------------------

        ScanLog.query.filter_by(
            student_id=student.id
        ).delete(
            synchronize_session=False
        )

        # --------------------------------
        # Delete student photo
        # --------------------------------

        if student.photo:

            photo_path = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                student.photo
            )

            if os.path.exists(photo_path):

                os.remove(photo_path)

        # --------------------------------
        # Delete student QR code
        # --------------------------------

        if student.qr_code:

            qr_path = os.path.join(
                current_app.config["QR_FOLDER"],
                student.qr_code
            )

            if os.path.exists(qr_path):

                os.remove(qr_path)

        # --------------------------------
        # Delete student
        # --------------------------------

        StudentService.delete(student)

        flash(
            "Student and associated scan logs deleted successfully.",
            "success"
        )

    except Exception as e:

        print("Delete Error :", e)

        flash(
            f"Delete Failed : {e}",
            "danger"
        )

    return redirect(
        url_for("student.student_list")
    )
# =====================================================
# SCAN LOGS
# =====================================================

@student_bp.route("/scan_logs")
def scan_logs():

    logs = ScanLogService.get_all()

    return render_template(
        "admin/scan_logs.html",
        logs=logs
    )


# =====================================================
# TOGGLE STUDENT STATUS
# =====================================================

@student_bp.route("/toggle_status/<rollno>")
def toggle_status(rollno):

    student = StudentService.get_student(rollno)

    if student is None:

        flash(
            "Student not found.",
            "danger"
        )

        return redirect(
            url_for("student.student_list")
        )

    try:

        if student.status == "Active":

            student.status = "Inactive"

        else:

            student.status = "Active"

        StudentService.save(student)

        flash(
            f"{student.name} is now {student.status}.",
            "success"
        )

    except Exception as e:

        flash(
            f"Status Update Failed : {e}",
            "danger"
        )

    return redirect(
        url_for("student.student_list")
    )
@student_bp.route("/export/students")
def export_students():

    students = StudentService.get_all_students()

    excel_file = ReportService.export_students(students)

    return send_file(

        excel_file,

        download_name="students.xlsx",

        as_attachment=True,

        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )
@student_bp.route("/export/students/pdf")
def export_students_pdf():

    students = StudentService.get_all_students()

    pdf = ReportService.export_students_pdf(students)

    return send_file(

        pdf,

        download_name="students.pdf",

        as_attachment=True,

        mimetype="application/pdf"

    )
@student_bp.route("/reports")
def reports():

    return render_template(
        "admin/reports.html"
    )
@student_bp.route("/export/scan_logs")
def export_scan_logs():

    logs = ScanLogService.get_all()

    excel = ReportService.export_scan_logs_excel(logs)

    return send_file(

        excel,

        download_name="scan_logs.xlsx",

        as_attachment=True,

        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )
@student_bp.route("/export/scan_logs/pdf")
def export_scan_logs_pdf():

    logs = ScanLogService.get_all()

    pdf = ReportService.export_scan_logs_pdf(logs)

    return send_file(

        pdf,

        download_name="scan_logs.pdf",

        as_attachment=True,

        mimetype="application/pdf"

    )