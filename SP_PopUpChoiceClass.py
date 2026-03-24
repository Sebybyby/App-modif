# -*- coding: utf-8 -*-
"""
Choix du nombre de cartes — Soft Pos.
Même UI que PopUpCardChoice, seul le titre et la navigation changent.
"""
from PySide6.QtWidgets import QLabel, QPushButton, QCheckBox, QWidget, QVBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from InterfaceClass import Interface
from InterfaceAfficheClass import InterfaceAffiche
import json

BG = "#1B3A6B"

CB_STYLE = (
    "QCheckBox {{ color:#FFFFFF; background:{bg}; font-size:15px; padding:6px; spacing:10px; }}"
    "QCheckBox::indicator {{"
    "  width:22px; height:22px; border-radius:4px;"
    "  border:2px solid #8AAAD4; background:#FFFFFF;"
    "}}"
    "QCheckBox::indicator:checked {{"
    "  background:#FFFF00; border:3px solid #FFFFFF;"
    "}}"
    "QCheckBox::indicator:unchecked:hover {{"
    "  border:2px solid #FFE033;"
    "}}"
    "QCheckBox:disabled {{ color:#AAAAAA; }}"
    "QCheckBox::indicator:disabled {{"
    "  background:#FFFF00; border:3px solid #AAAAAA;"
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
        """Cases à cocher cartes + bouton rond Valider centré."""
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

        # Cases à cocher
        self.cb1 = QCheckBox("1 Carte")
        self.cb1.setStyleSheet(CB_STYLE)
        self.cb1.setChecked(True)
        self.cb1.setEnabled(False)   # toujours incluse
        layout.addWidget(self.cb1, 0, Qt.AlignHCenter)

        self.cb2 = QCheckBox("2 Cartes")
        self.cb2.setStyleSheet(CB_STYLE)
        self.cb2.setChecked(True)    # défaut
        self.cb2.stateChanged.connect(self._on_cb2_changed)
        layout.addWidget(self.cb2, 0, Qt.AlignHCenter)

        self.cb3 = QCheckBox("3 Cartes")
        self.cb3.setStyleSheet(CB_STYLE)
        self.cb3.setChecked(False)
        self.cb3.stateChanged.connect(self._on_cb3_changed)
        layout.addWidget(self.cb3, 0, Qt.AlignHCenter)

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
    def _on_cb2_changed(self, state):
        """Décocher cb2 décoche automatiquement cb3."""
        if not state:
            self.cb3.setChecked(False)

    def _on_cb3_changed(self, state):
        """Cocher cb3 coche automatiquement cb2."""
        if state:
            self.cb2.setChecked(True)

    def _valider(self):
        compteur = ["Card 1"]
        if self.cb2.isChecked():
            compteur.append("Card 2")
        if self.cb3.isChecked():
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
