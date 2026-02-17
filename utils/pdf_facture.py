from reportlab.lib.pagesizes import portrait
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from datetime import datetime

def generer_ticket_caisse(path, patient_name, reference, acte, total, paye, reste):
    # Format ticket de caisse standard (80mm de large, hauteur variable)
    width = 8 * cm
    height = 15 * cm
    c = canvas.Canvas(path, pagesize=(width, height))
    
    # Entête
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(width/2, height - 1*cm, "CABINET DE GYNÉCOLOGIE")
    c.setFont("Helvetica", 8)
    c.drawCentredString(width/2, height - 1.5*cm, "Reçu de Paiement")
    
    c.line(0.5*cm, height - 2*cm, 7.5*cm, height - 2*cm)
    
    # Infos
    y = height - 2.5*cm
    c.setFont("Helvetica-Bold", 8)
    c.drawString(0.5*cm, y, f"Réf: {reference}")
    y -= 0.5*cm
    c.setFont("Helvetica", 8)
    c.drawString(0.5*cm, y, f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    y -= 0.5*cm
    c.drawString(0.5*cm, y, f"Patiente: {patient_name}")
    
    c.line(0.5*cm, y - 0.3*cm, 7.5*cm, y - 0.3*cm)
    y -= 0.8*cm
    
    # Détails des actes
    c.setFont("Helvetica-Bold", 8)
    c.drawString(0.5*cm, y, "Désignation")
    c.drawRightString(7.5*cm, y, "Total")
    y -= 0.5*cm
    
    c.setFont("Helvetica", 7)
    # Gestion du texte long pour les actes multiples
    text_obj = c.beginText(0.5*cm, y)
    for line in str(acte).split('\n'):
        text_obj.textLine(line[:30]) # Coupe si trop long
    c.drawText(text_obj)
    
    y -= 1.5*cm
    c.line(0.5*cm, y, 7.5*cm, y)
    y -= 0.5*cm
    
    # Totaux
    c.setFont("Helvetica-Bold", 9)
    c.drawString(0.5*cm, y, "TOTAL À PAYER")
    c.drawRightString(7.5*cm, y, f"{total} DH")
    y -= 0.4*cm
    c.setFont("Helvetica", 8)
    c.drawString(0.5*cm, y, "Montant Versé")
    c.drawRightString(7.5*cm, y, f"{paye} DH")
    y -= 0.4*cm
    c.setFont("Helvetica-Bold", 8)
    c.drawString(0.5*cm, y, "RESTE")
    c.drawRightString(7.5*cm, y, f"{reste} DH")
    
    y -= 1*cm
    c.setFont("Helvetica-Oblique", 7)
    c.drawCentredString(width/2, y, "Merci de votre confiance.")
    
    c.save()