# -*- coding: utf-8 -*-
"""
Page d'accueil : choix entre Soft Pos et Test Combinatoire.
"""
from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from InterfaceClass import Interface
from InterfaceAfficheClass import InterfaceAffiche

BG = "#1B3A6B"

ROUND_BTN = (
    "QPushButton {{"
    "  background:#FFFF00; color:#000000; border:none;"
    "  border-radius:{r}px; font-size:18px; font-weight:700;"
    "}}"
    "QPushButton:hover   {{ background:#FFE033; }}"
    "QPushButton:pressed {{ background:#CCBB00; }}"
)


class Accueil(Interface):
    def __init__(self):
        super().__init__()
        self.enum = InterfaceAffiche(8)
        self.etat = False
        self.windowPlace = ""

        self.setStyleSheet(f"background:{BG};")

        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self._build_title()
        self._build_buttons()

    def _build_title(self):
        lbl = QLabel("UR5 TEST")
        lbl.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        lbl.setStyleSheet(f"color:#FFFFFF; background:transparent; border:none;")
        lbl.setFont(QFont("Helvetica", 28, QFont.Bold))
        self._grid.addWidget(lbl, 0, 0, 1, 4)

    def _build_buttons(self):
        SIZE = 200
        R = SIZE // 2

        btn_soft = QPushButton("Soft\nPos")
        btn_soft.setFixedSize(SIZE, SIZE)
        btn_soft.setStyleSheet(ROUND_BTN.format(r=R))
        btn_soft.clicked.connect(self._go_soft_pos)
        self._grid.addWidget(btn_soft, 1, 0, 2, 2, Qt.AlignHCenter | Qt.AlignVCenter)

        btn_combi = QPushButton("Test\nCombinatoire")
        btn_combi.setFixedSize(SIZE, SIZE)
        btn_combi.setStyleSheet(ROUND_BTN.format(r=R))
        btn_combi.clicked.connect(self._go_combinatoire)
        self._grid.addWidget(btn_combi, 1, 2, 2, 2, Qt.AlignHCenter | Qt.AlignVCenter)

    def _go_soft_pos(self):
        self.windowPlace = self.geometry()
        self.destroy()
        self.etat = True
        self.enum = 9  # MenuSoftPos

    def _go_combinatoire(self):
        self.windowPlace = self.geometry()
        self.destroy()
        self.etat = True
        self.enum = 0  # Menu Combinatoire
