from models.rendezvous_model import RendezVousModel


def add_rdv(data):
    RendezVousModel.create(data)


def update_rdv(rdv_id, data):
    RendezVousModel.update(rdv_id, data)


def delete_rdv(rdv_id):
    RendezVousModel.delete(rdv_id)


def get_rendezvous():
    return RendezVousModel.get_all()


def get_rdv_du_jour():
    return RendezVousModel.get_today()


def get_rdv_dates():
    return RendezVousModel.get_all_dates()


def get_rdv_by_date(date_str):
    return RendezVousModel.get_by_date(date_str)
