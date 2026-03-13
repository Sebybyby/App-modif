# -*- coding: utf-8 -*-
"""
Gestion de la base de données des lecteurs (lecteurs.xlsx).
Chaque lecteur a un nom et sa position 0 : x, y, z, rX, rY, rZ, topZ.
"""
import os
import openpyxl

LECTEURS_FILE = "./Parametres/lecteurs.xlsx"
HEADERS = ["Nom", "x", "y", "z", "rX", "rY", "rZ", "topZ"]

# Lecteurs par défaut (données issues des positions hardcodées dans RobotClass.py)
DEFAULT_LECTEURS = [
    [
        "Lane 5000",
        -0.4547756256699072, 0.09449841328596138, 0.21046844075096408,
        -2.2162304932532844, 2.2250713469998527, 0.01629001438342314,
        0.399821937815115,
    ],
    [
        "Move 5000",
        -0.4540141593144729, 0.031580682143320125, 0.30871004420187936,
        -2.2037218160115697, 2.2372876043326744, 0.01616534026994103,
        0.5025886995214306,
    ],
]


def _ensure_file():
    """Crée le fichier lecteurs.xlsx s'il n'existe pas."""
    os.makedirs("./Parametres", exist_ok=True)
    if not os.path.exists(LECTEURS_FILE):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Lecteurs"
        ws.append(HEADERS)
        for row in DEFAULT_LECTEURS:
            ws.append(row)
        wb.save(LECTEURS_FILE)


def get_lecteurs():
    """Retourne la liste des noms de lecteurs."""
    _ensure_file()
    wb = openpyxl.load_workbook(LECTEURS_FILE)
    ws = wb.active
    return [row[0] for row in ws.iter_rows(min_row=2, values_only=True) if row[0]]


def get_lecteur_position(nom):
    """Retourne un dict {x, y, z, rX, rY, rZ, topZ} pour le lecteur donné."""
    _ensure_file()
    wb = openpyxl.load_workbook(LECTEURS_FILE)
    ws = wb.active
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] == nom:
            return {
                "x": row[1], "y": row[2], "z": row[3],
                "rX": row[4], "rY": row[5], "rZ": row[6],
                "topZ": row[7],
            }
    return None


def add_lecteur(nom, x, y, z, rX, rY, rZ, topZ):
    """Ajoute ou met à jour un lecteur dans la base de données."""
    _ensure_file()
    wb = openpyxl.load_workbook(LECTEURS_FILE)
    ws = wb.active
    vals = [nom, x, y, z, rX, rY, rZ, topZ]
    for row in ws.iter_rows(min_row=2):
        if row[0].value == nom:
            for i, v in enumerate(vals):
                row[i].value = v
            wb.save(LECTEURS_FILE)
            return
    ws.append(vals)
    wb.save(LECTEURS_FILE)
