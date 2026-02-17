from models.facture_model import FactureModel
import datetime

def save_facture(data):
    """Génère la référence et sauvegarde la facture via le modèle"""
    if 'reference' not in data or not data['reference']:
        now = datetime.datetime.now()
        data['reference'] = f"FAC-{now.strftime('%y%m%d-%H%M%S')}"
    
    # Appelle la méthode create du FactureModel
    return FactureModel.create(data)