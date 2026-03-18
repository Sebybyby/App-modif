# -*- coding: utf-8 -*-
"""
Paramétrage Robot pour Soft Pos.
Les positions téléphones sont gérées via le dropdown de la page de test.
Retourne au menu Soft Pos (enum=9).
"""
import gc
from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from InterfaceClass import Interface
from InterfaceAfficheClass import InterfaceAffiche
from RobotClass import Robot

BG = "#1B3A6B"

RETOUR_STYLE = (
    "QPushButton { background:#FFFF00; color:#000000; font-size:13px;"
    " font-weight:bold; padding:8px 20px; border-radius:6px; }"
    "QPushButton:hover   { background:#FFE033; }"
    "QPushButton:pressed { background:#CCBB00; }"
)
BTN_STYLE = (
    "QPushButton { color:#000000; background:#FFFF00; font-size:14px;"
    " font-weight:bold; padding:16px 50px; border-radius:8px; }"
    "QPushButton:hover    { background:#FFE033; }"
    "QPushButton:pressed  { background:#CCBB00; }"
)


class SP_ParametreRobot(Interface):
    def __init__(self):
        Interface.__init__(self)
        self.enum = InterfaceAffiche(11)
        self.windowPlace = []
        self.rob = Robot.Instance()

        self.setStyleSheet(f"background:{BG};")
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self._build_header()
        self._build_buttons()

    # ------------------------------------------------------------------
    def _build_header(self):
        btn_retour = QPushButton("Retour")
        btn_retour.setFixedSize(130, 46)
        btn_retour.setStyleSheet(RETOUR_STYLE)
        btn_retour.clicked.connect(self.RetourMenu)
        self._grid.addWidget(btn_retour, 0, 0, Qt.AlignLeft | Qt.AlignTop)

        titre = QLabel("Paramétrage du Robot — Soft Pos")
        titre.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        titre.setStyleSheet("color:#FFFFFF; background:transparent; border:none;")
        titre.setFont(QFont("Helvetica", 22, QFont.Bold))
        self._grid.addWidget(titre, 0, 0, 1, 5, Qt.AlignHCenter | Qt.AlignVCenter)

    def _btn(self, text, callback):
        btn = QPushButton(text)
        btn.setFixedHeight(64)
        btn.setStyleSheet(BTN_STYLE)
        btn.clicked.connect(callback)
        return btn

    def _build_buttons(self):
        self.boutonConnexion = self._btn("Connexion au robot", self.ConnexionRobotButton)
        self._grid.addWidget(self.boutonConnexion, 1, 1, 1, 3, Qt.AlignCenter)

        self.boutonCentrage = self._btn("Position 0 : paramétrage manuel", self.PositionCentrage)
        self._grid.addWidget(self.boutonCentrage, 2, 1, 1, 3, Qt.AlignCenter)

    # ------------------------------------------------------------------
    def RetourMenu(self):
        self.windowPlace = self.geometry()
        self.destroy()
        gc.collect()
        self.enum = 9  # MenuSoftPos

    def ConnexionRobotButton(self):
        self.rob.ConnexionRobot()

    def PositionCentrage(self):
        """Enregistre la position 0° du robot au centre du téléphone.
        La rotation 90° (groupes D/E/F) est calculée automatiquement — pas de 2ème calibration.
        """
        self._show_ok_dialog(
            "\n   Positionner le robot au centre du téléphone phi=0°\n"
            "   (la rotation 90° sera calculée automatiquement)   \n",
            w=500, h=130
        )
        try:
            self.rob.Position0(1)
        except Exception:
            self._show_ok_dialog("   Vérifier la connexion au robot   \n", w=400, h=120)
