from models.grossesse_model import GrossesseModel

def add_grossesse(data):
    GrossesseModel.create(data)

def get_grossesses(pid):
    return GrossesseModel.get_by_patient(pid)
