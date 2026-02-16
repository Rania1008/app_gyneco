from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from datetime import datetime
import os

def export_consultation_pdf(path, patient_name, patient_age, date, sections, images=None):
    c = canvas.Canvas(path, pagesize=A4)
    w, h = A4
    y = h - 2 * cm

    # Entête
    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(0.2, 0.4, 0.6) # Bleu médical
    c.drawString(2 * cm, y, "CONSULTATION MÉDICALE")
    y -= 1 * cm

    # Infos Patiente
    c.setFont("Helvetica-Bold", 11)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(2 * cm, y, f"Patiente : {patient_name} ({patient_age} ans)")
    c.drawString(w - 6 * cm, y, f"Date : {date}")
    y -= 1.5 * cm

    # Sections de texte
    for title, content in sections.items():
        if content and content.strip():
            c.setFont("Helvetica-Bold", 11)
            c.drawString(2 * cm, y, title)
            y -= 0.5 * cm
            
            c.setFont("Helvetica", 10)
            text_obj = c.beginText(2.5 * cm, y)
            for line in content.split("\n"):
                text_obj.textLine(line)
                y -= 0.4 * cm
            c.drawText(text_obj)
            y -= 0.5 * cm

        # Gestion des images si présentes pour cette section
        if images and title in images and images[title]:
            img_path = images[title]
            if os.path.exists(img_path):
                # On limite la taille de l'image (max 8cm de haut)
                c.drawImage(img_path, 2.5 * cm, y - 8 * cm, width=10 * cm, preserveAspectRatio=True, mask='auto')
                y -= 8.5 * cm

        if y < 5 * cm: # Saut de page si plus de place
            c.showPage()
            y = h - 2 * cm

    # Bas de page
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(2 * cm, 1 * cm, f"Document généré le {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    c.save()