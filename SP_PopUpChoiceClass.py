# -*- coding: utf-8 -*-
"""
Choix du nombre de cartes — Soft Pos.
Même UI que PopUpCardChoice, seul le titre et la navigation changent.
"""
from PySide6.QtWidgets import (
    QLabel, QPushButton, QWidget, QVBoxLayout,
    QRadioButton, QButtonGroup
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from InterfaceClass import Interface
from InterfaceAfficheClass import InterfaceAffiche
import json

BG = "#1B3A6B"

RB_STYLE = (
    "QRadioButton {{ color:#FFFFFF; background:{bg}; font-size:15px; padding:6px; spacing:10px; }}"
    "QRadioButton::indicator {{"
    "  width:22px; height:22px; border-radius:11px;"
    "  border:2px solid #8AAAD4; background:#FFFFFF;"
    "}}"
    "QRadioButton::indicator:checked {{"
    "  background:#FFFF00; border:3px solid #FFFFFF;"
    "}}"
    "QRadioButton::indicator:unchecked:hover {{"
    "  border:2px solid #FFE033;"
    "}}"
).format(bg=BG)


class SP_PopUpChoice(Interface):
    def __init__(self):
        Interface.__init__(self)
        with open("cartes.json", "w", encoding="utf-8") as f:
            json.dump({}, f)

        self.enum = InterfaceAffiche(16)

        self.setStyleSheet(f"background:{BG};")

        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self._build_header()
        self._build_center()

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
        btn_retour.clicked.connect(self._go_retour)
        self._grid.addWidget(btn_retour, 0, 0, Qt.AlignLeft | Qt.AlignTop)

        titre = QLabel("UR5 TEST - Soft Pos")
        titre.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        titre.setStyleSheet("color:#FFFFFF; background:transparent; border:none;")
        titre.setFont(QFont("Helvetica", 28, QFont.Bold))
        self._grid.addWidget(titre, 0, 0, 1, 5, Qt.AlignHCenter | Qt.AlignVCenter)

    def _build_center(self):
        """Boutons radio cartes + bouton rond Valider centré."""
        container = QWidget()
        container.setStyleSheet(f"background:{BG};")
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)

        # Label
        lbl = QLabel("Nombre de cartes à tester")
        lbl.setStyleSheet(
            f"color:#FFFFFF; font-size:17px; font-weight:bold; background:{BG};"
        )
        lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl, 0, Qt.AlignHCenter)

        # Boutons radio
        self._btn_group = QButtonGroup(self)

        self.rb1 = QRadioButton("1 Carte")
        self.rb1.setStyleSheet(RB_STYLE)
        self._btn_group.addButton(self.rb1)
        layout.addWidget(self.rb1, 0, Qt.AlignHCenter)

        self.rb2 = QRadioButton("2 Cartes")
        self.rb2.setStyleSheet(RB_STYLE)
        self.rb2.setChecked(True)   # défaut
        self._btn_group.addButton(self.rb2)
        layout.addWidget(self.rb2, 0, Qt.AlignHCenter)

        self.rb3 = QRadioButton("3 Cartes")
        self.rb3.setStyleSheet(RB_STYLE)
        self._btn_group.addButton(self.rb3)
        layout.addWidget(self.rb3, 0, Qt.AlignHCenter)

        # Bouton rond Valider
        btn = QPushButton("Valider")
        btn.setFixedSize(160, 160)
        btn.setStyleSheet("""
            QPushButton {
                background: #FFFF00;
                color: #000000;
                border: none;
                border-radius: 80px;
                font-size: 16px;
                font-weight: 700;
            }
            QPushButton:hover   { background: #FFE033; }
            QPushButton:pressed { background: #CCBB00; }
        """)
        btn.clicked.connect(self._valider)
        layout.addWidget(btn, 0, Qt.AlignHCenter)

        self._grid.addWidget(container, 1, 0, 2, 5, Qt.AlignHCenter | Qt.AlignVCenter)

    # ------------------------------------------------------------------
    def _valider(self):
        compteur = ["Card 1"]
        if self.rb2.isChecked() or self.rb3.isChecked():
            compteur.append("Card 2")
        if self.rb3.isChecked():
            compteur.append("Card 3")

        data = {"cartes": compteur}
        with open("cartes.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        self.windowPlace = self.geometry()
        self.destroy()
        self.etat = True
        self.enum = 14   # SP_Reader (IPP350)

    def _go_retour(self):
        self.windowPlace = self.geometry()
        self.destroy()
        self.etat = True
        self.enum = 9   # MenuSoftPos
