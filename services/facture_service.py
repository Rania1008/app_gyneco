class FactureService:

    @staticmethod
    def calculer_total(actes):
        return sum(acte["frais"] for acte in actes)

    @staticmethod
    def generer_reference():
        from datetime import datetime
        return f"FAC-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    @staticmethod
    def creer_facture(
        patient_id,
        consultation_id,
        actes,
        montant_paye,
        conn
    ):
        if not actes:
            raise ValueError("La facture doit contenir au moins un acte")

        if FactureModel.facture_existe_pour_consultation(consultation_id, conn):
            raise ValueError("Une facture existe déjà pour cette consultation")

        total = FactureService.calculer_total(actes)

        if montant_paye > total:
            raise ValueError("Le montant payé ne peut pas dépasser le total")

        reste = total - montant_paye
        reference = FactureService.generer_reference()

        facture_id = FactureModel.creer_facture(
            patient_id,
            consultation_id,
            reference,
            total,
            montant_paye,
            reste,
            conn
        )

        for acte in actes:
            FactureModel.ajouter_detail(
                facture_id,
                acte["service"],
                acte["frais"],
                conn
            )

        return facture_id
