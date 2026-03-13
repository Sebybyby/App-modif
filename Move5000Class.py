# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 14:24:56 2021
Converted from Tkinter to PySide6
@author: t0247275
"""
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

from ReaderClass import Reader
from InterfaceAfficheClass import InterfaceAffiche
from FichierClass import Fichier


class Move5000(Reader):
    def __init__(self):
        Reader.__init__(self)
        self.AfficheImageReader()
        self.enum = InterfaceAffiche(4)
        self.fichier = Fichier.Instance()
        try:
            self.fichier.Move5000()
        except Exception:
            print("error")

    def AfficheImageReader(self):
        self.titre = QLabel("Combination Test")
        self.titre.setStyleSheet("color:#FFFFFF; font-size:35px; background:#1B3A6B;")
        self.titre.setAlignment(Qt.AlignCenter)
        self._grid.addWidget(self.titre, 0, 2, 1, 5)
