from io import BytesIO
from wsgiref import headers

from openpyxl import Workbook
from openpyxl.styles import Font
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from sqlalchemy import table
from yfinance import data
from models.scan_log import ScanLog

class ReportService:

    @staticmethod
    def export_students(students):

        workbook = Workbook()

        sheet = workbook.active

        sheet.title = "Students"

        headers = [

            "Student ID",
            "Name",
            "Roll No",
            "Department",
            "Year",
            "Section",
            "Email",
            "Phone",
            "Status"

        ]

        for col, header in enumerate(headers, start=1):

            cell = sheet.cell(row=1, column=col)

            cell.value = header

            cell.font = Font(bold=True)

        row = 2

        for student in students:

            sheet.cell(row,1).value = student.student_id
            sheet.cell(row,2).value = student.name
            sheet.cell(row,3).value = student.rollno
            sheet.cell(row,4).value = student.department
            sheet.cell(row,5).value = student.year
            sheet.cell(row,6).value = student.section
            sheet.cell(row,7).value = student.email
            sheet.cell(row,8).value = student.phone
            sheet.cell(row,9).value = student.status

            row += 1

        output = BytesIO()

        workbook.save(output)

        output.seek(0)

        return output
    @staticmethod
    def export_students_pdf(students):

        output = BytesIO()

        document = SimpleDocTemplate(
            output,
            pagesize=A4
        )

        data = [

            [
                "Student ID",
                "Name",
                "Roll No",
                "Department",
                "Status"
            ]

        ]

        for student in students:

            data.append([

                student.student_id,
                student.name,
                student.rollno,
                student.department,
            student.status

                ])

            

        table = Table(data)

        table.setStyle(TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.darkblue),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("GRID", (0,0), (-1,-1), 1, colors.grey),

            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

            ("BOTTOMPADDING", (0,0), (-1,0), 10),

            ("BACKGROUND", (0,1), (-1,-1), colors.beige)

        ]))

        document.build([table])

        output.seek(0)

        return output
    @staticmethod
    def export_scan_logs_excel(logs):

        workbook = Workbook()

        sheet = workbook.active

        sheet.title = "Scan Logs"

        headers = [

            "Student",

            "Roll Number",

            "Scan Time",

            "Status",

            "IP Address"

        ]

        for column, header in enumerate(headers, 1):

            cell = sheet.cell(row=1, column=column)

            cell.value = header

            cell.font = Font(bold=True)

        row = 2

        for log in logs:

            sheet.cell(row=row, column=1).value = log.student.name

            sheet.cell(row=row, column=2).value = log.student.rollno

            sheet.cell(row=row, column=3).value = str(log.scan_time)

            sheet.cell(row=row, column=4).value = log.status

            sheet.cell(row=row, column=5).value = log.location

            row += 1

        output = BytesIO()

        workbook.save(output)

        output.seek(0)

        return output
    @staticmethod
    def export_scan_logs_pdf(logs):

        output = BytesIO()

        document = SimpleDocTemplate(

            output,

            pagesize=A4

        )

        data = [[

            "Student",

            "Roll",

            "Time",

            "Status",

            "IP"

        ]]

        for log in logs:

            data.append([

                log.student.name,

                log.student.rollno,

                str(log.scan_time),

                log.status,

                log.location

            ])

        table = Table(data)

        table.setStyle(TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("GRID",(0,0),(-1,-1),1,colors.grey),

            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

            ("BACKGROUND",(0,1),(-1,-1),colors.beige)

        ]))

        document.build([table])

        output.seek(0)

        return output