from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_pdf(report_data):
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "AI Security Scan Report")

    y -= 40
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Generated: {datetime.now()}")

    y -= 30
    for item in report_data:
        c.drawString(50, y, f"{item['process']}  |  Risk: {item['risk']}")
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
    return filename
