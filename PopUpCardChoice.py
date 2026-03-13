# -*- coding: utf-8 -*-
"""
Choix du nombre de cartes — menu déroulant + bouton rond central.
Même principe visuel que le menu Soft Pos / Combinatoire.
"""
from PySide6.QtWidgets import QLabel, QPushButton, QComboBox, QWidget, QVBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from InterfaceClass import Interface
from InterfaceAfficheClass import InterfaceAffiche
import json

BG = "#1B3A6B"


class PopUp_NbCard(Interface):
    def __init__(self):
        Interface.__init__(self)
        with open("cartes.json", "w", encoding="utf-8") as f:
            json.dump({}, f)

        self.enum = InterfaceAffiche(7)
        self.compteur = []

        self.setStyleSheet(f"background:{BG};")

        # Même grille que Combinatoire : 4 lignes x 5 colonnes
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

        titre = QLabel("UR5 TEST - Choix Cartes")
        titre.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        titre.setStyleSheet("color:#FFFFFF; background:transparent; border:none;")
        titre.setFont(QFont("Helvetica", 28, QFont.Bold))
        self._grid.addWidget(titre, 0, 1, 1, 4)

    def _build_center(self):
        """Menu déroulant nb cartes + bouton rond Valider centré."""
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.setSpacing(18)
        layout.setContentsMargins(0, 0, 0, 0)

        # Menu déroulant
        self.combo = QComboBox()
        self.combo.addItems(["1 Carte", "2 Cartes", "3 Cartes"])
        self.combo.setCurrentIndex(1)   # 2 Cartes par défaut
        self.combo.setFixedWidth(210)
        self.combo.setStyleSheet("""
            QComboBox {
                background: #FFFF00;
                color: #000000;
                font-size: 14px;
                font-weight: bold;
                border-radius: 6px;
                padding: 8px 12px;
                border: none;
            }
            QComboBox::drop-down {
                border: none;
                width: 24px;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background: #FFFF00;
                color: #000000;
                selection-background-color: #FFE033;
                font-size: 14px;
                font-weight: bold;
                border: 1px solid #CCBB00;
            }
        """)
        layout.addWidget(self.combo, 0, Qt.AlignHCenter)

        # Bouton rond central Valider
        btn = QPushButton("Valider")
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
        btn.clicked.connect(self._valider)
        layout.addWidget(btn, 0, Qt.AlignHCenter)

        self._grid.addWidget(container, 1, 0, 2, 5, Qt.AlignHCenter | Qt.AlignVCenter)

    # ------------------------------------------------------------------
    def _valider(self):
        idx = self.combo.currentIndex()
        self.compteur = ["Card 1"]
        if idx >= 1:
            self.compteur.append("Card 2")
        if idx >= 2:
            self.compteur.append("Card 3")

        print(self.compteur)
        data = {"cartes": self.compteur}
        with open("cartes.json", "w") as f:
            json.dump(data, f, indent=4)

        self.windowPlace = self.geometry()
        self.destroy()
        self.etat = True
        self.enum = 4   # Move5000

    def _go_retour(self):
        self.windowPlace = self.geometry()
        self.destroy()
        self.etat = True
        self.enum = 0   # Menu Combinatoire
