# -*- coding: utf-8 -*-
"""
Menu principal Soft Pos — 1 bouton rond central.
Même structure visuelle que le menu Combinatoire.
"""
from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from InterfaceClass import Interface
from InterfaceAfficheClass import InterfaceAffiche


class MenuSoftPos(Interface):
    def __init__(self):
        super().__init__()
        self.enum = InterfaceAffiche(9)
        self.etat = False
        self.windowPlace = ""

        self.setStyleSheet("background:#1B3A6B;")

        # Même grille que Combinatoire : 4 lignes x 5 colonnes
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self._build_header()
        self._build_center_button()
        self._build_bottom_buttons()

    # ------------------------------------------------------------------
    def _build_header(self):
        btn_retour = QPushButton("Retour")
        btn_retour.setFixedSize(130, 46)
        btn_retour.setStyleSheet(
            "QPushButton { background:#FFFF00; color:#000000; font-size:13px;"
            " font-weight:bold; padding:8px 20px; border-radius:6px; }"
            "QPushButton:hover   { background:#FFE033; }"
            "QPushButton:pressed { background:#CCBB00; }"
        )
        btn_retour.clicked.connect(self._go_accueil)
        self._grid.addWidget(btn_retour, 0, 0, Qt.AlignLeft | Qt.AlignTop)

        # Titre centré sur toute la largeur (colonnes 0→4)
        titre = QLabel("UR5 TEST - Soft Pos")
        titre.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        titre.setStyleSheet("color:#FFFFFF; background:transparent; border:none;")
        titre.setFont(QFont("Helvetica", 28, QFont.Bold))
        self._grid.addWidget(titre, 0, 0, 1, 5, Qt.AlignHCenter | Qt.AlignVCenter)

    def _build_center_button(self):
        """Un seul bouton rond jaune centré — identique au menu Combinatoire."""
        btn = QPushButton("Soft\nPos")
        btn.setFixedSize(200, 200)
        btn.setStyleSheet("""
            QPushButton {
                background: #FFFF00;
                color: #000000;
                border: none;
                border-radius: 100px;
                font-size: 18px;
                font-weight: 700;
            }
            QPushButton:hover   { background: #FFE033; }
            QPushButton:pressed { background: #CCBB00; }
        """)
        btn.clicked.connect(self._go_choix)
        self._grid.addWidget(btn, 1, 0, 2, 5, Qt.AlignHCenter | Qt.AlignVCenter)

    def _build_bottom_buttons(self):
        """3 boutons en bas — Formulaire SP | Config Son SP | Paramétrage Robot SP."""
        btn_style = (
            "QPushButton { background:#FFFF00; color:#000000; font-size:15px;"
            " font-weight:bold; padding:16px 30px; border-radius:10px; min-width:185px; }"
            "QPushButton:hover   { background:#FFE033; }"
            "QPushButton:pressed { background:#CCBB00; }"
        )

        btn_form = QPushButton("Formulaire\nSoft Pos")
        btn_form.setStyleSheet(btn_style)
        btn_form.clicked.connect(self._go_formulaire)
        self._grid.addWidget(btn_form, 3, 0, 1, 2, Qt.AlignLeft | Qt.AlignBottom)

        btn_son = QPushButton("Config Son\nSoft Pos")
        btn_son.setStyleSheet(btn_style)
        btn_son.clicked.connect(self._go_son)
        self._grid.addWidget(btn_son, 3, 2, 1, 1, Qt.AlignHCenter | Qt.AlignBottom)

        btn_robot = QPushButton("Paramétrage\nRobot Soft Pos")
        btn_robot.setStyleSheet(btn_style)
        btn_robot.clicked.connect(self._go_robot)
        self._grid.addWidget(btn_robot, 3, 3, 1, 2, Qt.AlignRight | Qt.AlignBottom)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------
    def _nav(self, enum_val):
        self.windowPlace = self.geometry()
        self.destroy()
        self.etat = True
        self.enum = enum_val

    def _go_accueil(self):    self._nav(8)
    def _go_choix(self):      self._nav(16)   # SP_PopUpChoice (nb cartes)
    def _go_formulaire(self): self._nav(10)
    def _go_son(self):        self._nav(15)   # SP_FichierConfigLecteur
    def _go_robot(self):      self._nav(11)
