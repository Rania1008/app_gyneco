/* =========================================================
   TABLE UTILISATEURS (AUTHENTIFICATION)
   ========================================================= */
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);

/* =========================================================
   TABLE PATIENTS
   ========================================================= */
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    telephone TEXT,
    adresse TEXT,
    date_naissance TEXT,

    situation_familiale TEXT CHECK (
        situation_familiale IN ('Célibataire', 'Mariée', 'Divorcée', 'Veuve')
    ),

    assurance TEXT CHECK (
        assurance IN ('CNSS', 'CNOPS', 'AMO', 'Privée', 'Aucune')
    ),

    date_premiere_consultation TEXT,
    created_at TEXT
);

/* =========================================================
   TABLE CONSULTATIONS (TEXTE LIBRE)
   ========================================================= */
CREATE TABLE IF NOT EXISTS consultations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    date_consultation TEXT,
    antecedants TEXT,
    motif_consultation TEXT,
    examen_clinique TEXT,
    examen_biologique TEXT,
    examen_radiologique TEXT,
    diagnostique TEXT,
    traitement TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

/* =========================================================
   TABLE SUIVI PATIENT
   ========================================================= */
CREATE TABLE IF NOT EXISTS suivi_patient (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    date_suivi TEXT,
    evolution_clinique TEXT,
    examen_biologique TEXT,
    examen_radiologique TEXT,
    traitement TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

/* =========================================================
   TABLE GROSSESSE
   ========================================================= */
CREATE TABLE IF NOT EXISTS grossesse (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    date_derniere_regle TEXT,
    grossesse_precedente TEXT,
    fetus TEXT,
    status TEXT,
    a_terme_le TEXT,
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

/* =========================================================
   TABLE RENDEZ-VOUS
   ========================================================= */
CREATE TABLE IF NOT EXISTS rendez_vous (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    date_rdv TEXT,
    heure_rdv TEXT,
    statut TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

/* =========================================================
   TABLE SALLE D’ATTENTE (INDÉPENDANTE)
   ========================================================= */
CREATE TABLE IF NOT EXISTS salle_attente (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_attente TEXT,
    nom_patient TEXT,
    numero_identite TEXT
);

/* =========================================================
   TABLE FACTURES (ENTÊTE)
   ========================================================= */
CREATE TABLE IF NOT EXISTS factures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    societe TEXT,
    reference TEXT,
    date_facture TEXT,
    total REAL,
    paye REAL,
    reste REAL,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

/* =========================================================
   TABLE DÉTAILS FACTURE
   ========================================================= */
CREATE TABLE IF NOT EXISTS facture_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    facture_id INTEGER NOT NULL,
    service TEXT,
    frais REAL,
    FOREIGN KEY (facture_id) REFERENCES factures(id)
);

DROP TABLE IF EXISTS factures;

CREATE TABLE IF NOT EXISTS factures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    consultation_id INTEGER,
    societe TEXT,
    reference TEXT UNIQUE,
    date_facture TEXT DEFAULT (DATE('now')),
    total REAL CHECK (total >= 0),
    paye REAL CHECK (paye >= 0),
    reste REAL CHECK (reste >= 0),
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (consultation_id) REFERENCES consultations(id)
);

/* Ajout des types d'actes pour la secrétaire */
CREATE TABLE IF NOT EXISTS actes_medicaux (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    libelle TEXT NOT NULL,
    prix_standard REAL
);

/* Mise à jour de la table factures pour inclure les actes hors consultation */
ALTER TABLE factures ADD COLUMN acte_id INTEGER;
ALTER TABLE factures ADD COLUMN notes TEXT;

