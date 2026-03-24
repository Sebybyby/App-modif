# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 16:15:31 2021
Converted from Tkinter to PySide6
@author: t0247275
"""
from PySide6.QtWidgets import (
    QLabel, QPushButton, QLineEdit, QFrame, QHBoxLayout, QVBoxLayout
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from InterfaceClass import Interface
from InterfaceAfficheClass import InterfaceAffiche
from FichierClass import Fichier
import gc


BG = "#1B3A6B"
FRAME_STYLE = f"QFrame {{ background:{BG}; border:2px solid #FFFFFF; border-radius:8px; }}"
LABEL_STYLE = f"color:#FFFFFF; font-size:16px; font-weight:bold; background:{BG}; border:none;"
INPUT_STYLE = "color:#000000; font-size:13px; background:#FFFFFF; border-radius:4px; padding:4px;"
BTN_YELLOW = (
    "QPushButton { color:#000000; background:#FFFF00; font-size:14px;"
    " font-weight:bold; padding:10px 50px; border-radius:8px; }"
    "QPushButton:hover    { background:#FFE033; }"
    "QPushButton:pressed  { background:#CCBB00; }"
)


class Formulaire(Interface):
    def __init__(self):
        Interface.__init__(self)
        self.etat = False
        self.windowPlace = []
        self.enum = InterfaceAffiche(1)
        self.fichier = Fichier.Instance()

        # Grille : 5 lignes x 9 colonnes
        self.setStyleSheet(f"background:{BG};")

        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        self._build_header()
        self._build_form()

    def _build_header(self):
        # Retour haut gauche
        self.retourBouton = QPushButton("Retour")
        self.retourBouton.setFixedSize(130, 46)
        self.retourBouton.setStyleSheet(
            "QPushButton { background:#FFFF00; color:#000000; font-size:13px;"
            " font-weight:bold; padding:8px 20px; border-radius:6px; }"
            "QPushButton:hover    { background:#FFE033; }"
            "QPushButton:pressed  { background:#CCBB00; }"
        )
        self.retourBouton.clicked.connect(self.RetourMenu)
        self._grid.addWidget(self.retourBouton, 0, 0, Qt.AlignLeft | Qt.AlignTop)

        # Titre centré
        self.titre = QLabel("Formulaire")
        self.titre.setStyleSheet("color:#FFFFFF; background:transparent; border:none;")
        self.titre.setFont(QFont("Helvetica", 28, QFont.Bold))
        self.titre.setAlignment(Qt.AlignCenter)
        self._grid.addWidget(self.titre, 0, 1, 1, 7, Qt.AlignCenter)

    def _field(self, label_text):
        """Crée un QFrame avec label + QLineEdit côte à côte."""
        frame = QFrame()
        frame.setStyleSheet(FRAME_STYLE)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(16, 8, 16, 8)

        lbl = QLabel(label_text)
        lbl.setStyleSheet(LABEL_STYLE)
        lbl.setFixedWidth(180)

        inp = QLineEdit()
        inp.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        inp.setStyleSheet(INPUT_STYLE)

        layout.addWidget(lbl)
        layout.addWidget(inp)
        return frame, inp

    def _build_form(self):
        self.operateurFrame, self.nomOperateur = self._field("Opérateur :")
        self._grid.addWidget(self.operateurFrame, 2, 1, 1, 7)

        self.antenneFrame, self.nomAntenne = self._field("Antenne :")
        self._grid.addWidget(self.antenneFrame, 4, 1, 1, 7)

        self.projetFrame, self.nomCarte = self._field("Nom du projet :")
        self._grid.addWidget(self.projetFrame, 6, 1, 1, 7)

        self.buttonSubmit = QPushButton("Valider")
        self.buttonSubmit.setStyleSheet(BTN_YELLOW)
        self.buttonSubmit.clicked.connect(self.Affichetext)
        self._grid.addWidget(self.buttonSubmit, 7, 3, 1, 3, Qt.AlignCenter)

    def RetourMenu(self):
        self.windowPlace = self.geometry()
        self.destroy()
        gc.collect()
        self.enum = 0

    def Affichetext(self):
        if (self.nomOperateur.text() == "" and
                self.nomAntenne.text() == "" and
                self.nomCarte.text() == ""):
            self.PopUpChamps()
        else:
            print("le nom du projet est : ", self.nomCarte.text())
            print("le nom de l\'antenne est : ", self.nomAntenne.text())
            print("le nom de l\'opérateur est : ", self.nomOperateur.text())
            self.fichier.creationFichier(self.nomCarte, self.nomOperateur, self.nomAntenne)
            self.PopUpFichier()

    def PopUpChamps(self):
        self._show_ok_dialog("\n   Attention les champs ne sont pas remplis   \n", w=370, h=120)

    def PopUpFichier(self):
        self._show_ok_dialog("\n  Fichier créé avec succès   \n", w=300, h=120)
        self.RetourMenu()
