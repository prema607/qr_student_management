import re


class Validator:

    @staticmethod
    def validate_name(name):

        if not name:
            return False, "Student name is required."

        name = name.strip()

        if len(name) < 3:
            return False, "Student name must contain at least 3 characters."

        if not re.fullmatch(r"[A-Za-z ]+", name):
            return False, "Student name should contain only letters and spaces."

        return True, ""


    @staticmethod
    def validate_rollno(rollno):

        if not rollno:
            return False, "Roll number is required."

        rollno = rollno.strip()

        if len(rollno) < 6:
            return False, "Roll number is too short."

        return True, ""


    @staticmethod
    def validate_email(email):

        if not email:
            return True, ""

        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        if not re.fullmatch(pattern, email):
            return False, "Invalid email address."

        return True, ""


    @staticmethod
    def validate_phone(phone, field_name="Phone"):

        if not phone:
            return True, ""

        if not phone.isdigit():
            return False, f"{field_name} must contain only digits."

        if len(phone) != 10:
            return False, f"{field_name} must contain exactly 10 digits."

        return True, ""


    @staticmethod
    def validate_required(value, field):

        if not value or not value.strip():
            return False, f"{field} is required."

        return True, ""


    @staticmethod
    def validate_registration(form):

        checks = [

            Validator.validate_name(form.get("name")),

            Validator.validate_rollno(form.get("rollno")),

            Validator.validate_email(form.get("email")),

            Validator.validate_phone(
                form.get("phone"),
                "Phone Number"
            ),

            Validator.validate_phone(
                form.get("parent_phone"),
                "Parent Phone Number"
            ),

            Validator.validate_required(
                form.get("department"),
                "Department"
            ),

            Validator.validate_required(
                form.get("year"),
                "Year"
            ),

            Validator.validate_required(
                form.get("section"),
                "Section"
            )

        ]

        for valid, message in checks:

            if not valid:
                return valid, message

        return True, ""