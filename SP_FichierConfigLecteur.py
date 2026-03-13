# -*- coding: utf-8 -*-
"""
Config Son Lecteur pour Soft Pos — retourne au menu Soft Pos (enum=9).
"""
import gc
from FichierConfigLecteur import FichierReader
from InterfaceAfficheClass import InterfaceAffiche


class SP_FichierReader(FichierReader):
    def __init__(self):
        super().__init__()
        self.enum = InterfaceAffiche(15)
        # Mise à jour du titre
        self.ti.setText("Config Son Lecteur — Soft Pos")

    def RetourMenu(self):
        self.windowPlace = self.geometry()
        self.destroy()
        gc.collect()
        self.enum = 9  # MenuSoftPos
