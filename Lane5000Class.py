# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 09:35:23 2021
Converted from Tkinter to PySide6
@author: t0247275
"""
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

from ReaderClass import Reader
from InterfaceAfficheClass import InterfaceAffiche
from FichierClass import Fichier


class Lane5000(Reader):
    def __init__(self):
        Reader.__init__(self)
        self.AfficheImageReader()
        self.enum = InterfaceAffiche(3)
        self.fichier = Fichier.Instance()
        Reader.test = 2

        try:
            self.fichier.Lane5000()
        except Exception:
            print("error")

    def AfficheImageReader(self):
        self.label1 = QLabel("Lane5000")
        self.label1.setStyleSheet("color:#FFFFFF; font-size:35px; background:#0054A4;")
        self.label1.setAlignment(Qt.AlignCenter)
        self._grid.addWidget(self.label1, 0, 2, 1, 5)
