# -*- coding: utf-8 -*-
"""
Gestion de la base de données des lecteurs Combinatoire (lecteurs.xlsx).
Les points initiaux sont définis directement dans le fichier Excel.
"""
import os
import openpyxl

LECTEURS_FILE = "./Parametres/lecteurs.xlsx"
HEADERS = ["Nom", "x", "y", "z", "rX", "rY", "rZ", "topZ"]


def _ensure_file():
    """Crée lecteurs.xlsx vide (en-têtes seulement) s'il n'existe pas."""
    os.makedirs("./Parametres", exist_ok=True)
    if not os.path.exists(LECTEURS_FILE):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Lecteurs"
        ws.append(HEADERS)
        wb.save(LECTEURS_FILE)


def get_lecteurs():
    """Retourne la liste des noms de lecteurs Combinatoire."""
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
    """Ajoute ou met à jour un lecteur dans lecteurs.xlsx."""
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
