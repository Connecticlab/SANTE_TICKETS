"""
Logique de recherche patient anti-doublons — CDC SanteTicket §6.1
Ordre de priorité :
  1. Téléphone
  2. Numéro de carte patient / QR code
  3. Nom + prénom + date de naissance combinés
  4. Recherche approximative (fuzzy) sur le nom
Un nouveau Patient n'est créé que si aucune de ces recherches n'aboutit.
"""
from difflib import SequenceMatcher
from .models import Patient

FUZZY_THRESHOLD = 0.80  # seuil de similarité (0 a 1) pour la recherche approximative


def rechercher_patient(telephone=None, numero_patient=None, qr_code=None,
                        nom=None, prenom=None, date_naissance=None):
    """
    Retourne un tuple (patient_ou_None, methode_trouvee_str)
    methode_trouvee est l'une de : 'telephone', 'numero_carte', 'nom_prenom_naissance',
    'fuzzy', ou None si rien trouve.
    """

    # 1. Recherche par telephone (le plus fiable si disponible)
    if telephone:
        patient = Patient.objects.filter(telephone=telephone).first()
        if patient:
            return patient, 'telephone'

    # 2. Recherche par numero de carte patient ou QR code (scan)
    if numero_patient:
        patient = Patient.objects.filter(numero_patient=numero_patient).first()
        if patient:
            return patient, 'numero_carte'

    if qr_code:
        patient = Patient.objects.filter(qr_code=qr_code).first()
        if patient:
            return patient, 'numero_carte'

    # 3. Recherche par nom + prenom + date de naissance combines
    if nom and prenom and date_naissance:
        patient = Patient.objects.filter(
            nom__iexact=nom,
            prenom__iexact=prenom,
            date_naissance=date_naissance,
        ).first()
        if patient:
            return patient, 'nom_prenom_naissance'

    # 4. Recherche approximative (fuzzy) sur le nom, pour capter fautes de frappe
    if nom:
        candidats = Patient.objects.all()
        meilleur_score = 0.0
        meilleur_patient = None
        nom_normalise = nom.strip().lower()

        for candidat in candidats:
            score = SequenceMatcher(None, nom_normalise, candidat.nom.strip().lower()).ratio()
            if score > meilleur_score:
                meilleur_score = score
                meilleur_patient = candidat

        if meilleur_patient and meilleur_score >= FUZZY_THRESHOLD:
            return meilleur_patient, 'fuzzy'

    # Aucune correspondance : un nouveau Patient devra etre cree
    return None, None
