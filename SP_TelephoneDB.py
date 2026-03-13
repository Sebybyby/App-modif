# -*- coding: utf-8 -*-
"""
Gestion des téléphones Soft Pos (SP_Telephones.xlsx).
Même principe que LecteurDB.py — fournit noms et méthodes de positionnement.
"""
import openpyxl

SP_PHONES_FILE = "./Parametres/SP_Telephones.xlsx"

# Correspondance : nom affiché → suffixe de méthode dans RobotClass
PHONE_METHODS = {
    "iPhone SE":       "IphoneSE",
    "iPhone 13/14/15": "Iphone13",
    "Samsung A34":     "SMGA34",
    "Samsung S23":     "SMGS23",
    "Samsung A15":     "SMGA15",
    "Redmi 13C":       "Redmi13C",
}


def get_telephones():
    """Retourne la liste des noms de téléphones depuis SP_Telephones.xlsx."""
    try:
        wb = openpyxl.load_workbook(SP_PHONES_FILE)
        ws = wb.active
        noms = [row[0] for row in ws.iter_rows(min_row=2, values_only=True) if row[0]]
        return noms if noms else list(PHONE_METHODS.keys())
    except Exception:
        return list(PHONE_METHODS.keys())


def get_telephone_method(nom):
    """Retourne le suffixe de méthode RobotClass pour le téléphone donné.
    Ex : 'iPhone SE' → 'IphoneSE'  (→ robot.Position0_IphoneSE())
    """
    return PHONE_METHODS.get(nom)
