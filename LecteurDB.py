# -*- coding: utf-8 -*-
"""
Gestion de la base de données des lecteurs (lecteurs.xlsx).
Chaque lecteur a un nom et sa position 0 : x, y, z, rX, rY, rZ, topZ.
Les coordonnées sont extraites des méthodes Position0_XXX de RobotClass.py.
Tous les points de test sont calculés relativement à ce premier point (voir Conversion()).
"""
import os
import openpyxl

LECTEURS_FILE = "./Parametres/lecteurs.xlsx"
HEADERS = ["Nom", "x", "y", "z", "rX", "rY", "rZ", "topZ"]

def get_lecteurs():
    wb = openpyxl.load_workbook(LECTEURS_FILE)
    ws = wb.active
    return [row[0] for row in ws.iter_rows(min_row=2, values_only=True) if row[0]]


def get_lecteur_position(nom):


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
