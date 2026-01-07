from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from datetime import datetime

def export_consultation_pdf(path, patient_name, date, sections):
    c = canvas.Canvas(path, pagesize=A4)
    w, h = A4
    y = h - 2 * cm

    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, y, "Consultation Médicale – Gynécologie")
    y -= 1 * cm

    c.setFont("Helvetica", 10)
    c.drawString(2 * cm, y, f"Patiente : {patient_name}")
    y -= 0.6 * cm
    c.drawString(2 * cm, y, f"Date : {date}")
    y -= 1 * cm

    for title, content in sections.items():
        if content.strip():
            c.setFont("Helvetica-Bold", 11)
            c.drawString(2 * cm, y, title)
            y -= 0.4 * cm
            c.setFont("Helvetica", 10)
            for line in content.split("\n"):
                c.drawString(2.2 * cm, y, line)
                y -= 0.35 * cm
            y -= 0.5 * cm

            if y < 3 * cm:
                c.showPage()
                y = h - 2 * cm

    c.setFont("Helvetica-Oblique", 8)
    c.drawString(
        2 * cm, 2 * cm,
        f"Document généré le {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )
    c.save()
