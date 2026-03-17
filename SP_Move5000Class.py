# -*- coding: utf-8 -*-
"""
Move5000 pour Soft Pos — version standalone, indépendante de Move5000Class.py.
Hérite de SP_Reader (Soft Pos) et non de Move5000 (Combinatoire).
Retourne au menu Soft Pos (enum=9).
"""
import gc
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

from SP_ReaderClass import SP_Reader
from InterfaceAfficheClass import InterfaceAffiche
from FichierClass import Fichier


class SP_Move5000(SP_Reader):
    def __init__(self):
        SP_Reader.__init__(self)
        self.AfficheImageReader()
        self.enum = InterfaceAffiche(13)
        self.fichier = Fichier.Instance()

        try:
            self.fichier.Move5000()
        except Exception:
            print("error")

    def AfficheImageReader(self):
        self.titre = QLabel("Move5000 — Soft Pos")
        self.titre.setStyleSheet("color:#FFFFFF; font-size:35px; background:#1B3A6B;")
        self.titre.setAlignment(Qt.AlignCenter)
        self._grid.addWidget(self.titre, 0, 2, 1, 5)

    def RetourMenu(self):
        self.windowPlace = self.geometry()
        self.destroy()
        try:
            gc.collect()
            self._stopAutoFlag = True
            self.robotVariable.gripperrelease()
        except Exception as e:
            print(f"Erreur lors de l'arrêt: {e}")
        self.enum = 9  # MenuSoftPos
