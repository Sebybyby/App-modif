# MenuClass.py (PySide6)

from __future__ import annotations

from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from InterfaceClass import Interface
from InterfaceAfficheClass import InterfaceAffiche


class Menu(Interface):
    def __init__(self):
        super().__init__()

        self.enum = InterfaceAffiche(0)
        self.etat = False
        self.windowPlace = ""

        self.setStyleSheet("background:#1B3A6B;")

        # Grid : 4 lignes x 5 colonnes
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
        btn_retour.clicked.connect(self.ChangementFenetreAccueil)
        self._grid.addWidget(btn_retour, 0, 0, Qt.AlignLeft | Qt.AlignTop)

        self.titre = QLabel("UR5 TEST - Combinatoire")
        self.titre.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.titre.setStyleSheet("color:#FFFFFF; background:transparent; border:none;")
        self.titre.setFont(QFont("Helvetica", 28, QFont.Bold))
        self._grid.addWidget(self.titre, 0, 1, 1, 4)

    def _build_center_button(self):
        """Un seul bouton rond jaune centré → ouvre Move5000."""
        btn = QPushButton("Test\nCombinatoire")
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
        btn.clicked.connect(self.ChangementFenetreMove5000)
        self._grid.addWidget(btn, 1, 0, 2, 5, Qt.AlignHCenter | Qt.AlignVCenter)

    def _build_bottom_buttons(self):
        """Boutons bas — 3 boutons homogènes."""
        btn_style = (
            "QPushButton { background:#FFFF00; color:#000000; font-size:15px;"
            " font-weight:bold; padding:16px 30px; border-radius:10px; min-width:185px; }"
            "QPushButton:hover   { background:#FFE033; }"
            "QPushButton:pressed { background:#CCBB00; }"
        )

        self.btn_form = QPushButton("Formulaire")
        self.btn_form.setStyleSheet(btn_style)
        self.btn_form.clicked.connect(self.ChangementFenetreFormulaire)
        self._grid.addWidget(self.btn_form, 3, 0, 1, 2, Qt.AlignLeft | Qt.AlignBottom)

        self.btn_son = QPushButton("Paramétrage Son")
        self.btn_son.setStyleSheet(btn_style)
        self.btn_son.clicked.connect(self.ChangementFenetreDetecSon)
        self._grid.addWidget(self.btn_son, 3, 2, 1, 1, Qt.AlignHCenter | Qt.AlignBottom)

        self.btn_robot = QPushButton("Paramétrage\nRobot")
        self.btn_robot.setStyleSheet(btn_style)
        self.btn_robot.clicked.connect(self.ChangementFenetreRobot)
        self._grid.addWidget(self.btn_robot, 3, 3, 1, 2, Qt.AlignRight | Qt.AlignBottom)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------
    def ChangementFenetre(self):
        self.windowPlace = self.geometry()
        self.destroy()
        self.etat = True

    def ChangementFenetreFormulaire(self):
        self.ChangementFenetre()
        self.enum = 1

    def ChangementFenetreMove5000(self):
        self.ChangementFenetre()
        self.enum = 7  # popup choix nb cartes → puis Move5000

    def ChangementFenetreRobot(self):
        self.ChangementFenetre()
        self.enum = 2

    def ChangementFenetreDetecSon(self):
        self.ChangementFenetre()
        self.enum = 6

    def ChangementFenetreAccueil(self):
        self.ChangementFenetre()
        self.enum = 8
