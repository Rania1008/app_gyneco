from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import os

def export_consultation_pdf(path, patient_name, age, date, sections, images=None):
    c = canvas.Canvas(path, pagesize=A4)
    w, h = A4
    y = h - 2 * cm

    c.setFont("Helvetica-Bold", 16)
    c.drawString(2 * cm, y, "RAPPORT DE CONSULTATION")
    y -= 1 * cm
    
    c.setFont("Helvetica", 10)
    c.drawString(2 * cm, y, f"Patiente : {patient_name} | Age : {age}")
    c.drawString(w - 5 * cm, y, f"Date : {date}")
    y -= 1.5 * cm

    for title, content in sections.items():
        if content and len(str(content)) > 2:
            c.setFont("Helvetica-Bold", 11)
            c.drawString(2 * cm, y, title)
            y -= 0.5 * cm
            c.setFont("Helvetica", 10)
            c.drawString(2.5 * cm, y, str(content))
            y -= 0.8 * cm

            # Insertion d'image si elle existe pour cette section
            key = title.lower().replace("examen ", "")
            if images and key in images and images[key]:
                if os.path.exists(images[key]):
                    c.drawImage(images[key], 3 * cm, y - 6 * cm, width=8 * cm, preserveAspectRatio=True)
                    y -= 7 * cm

            if y < 4 * cm:
                c.showPage()
                y = h - 2 * cm

    c.save()