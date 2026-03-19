# -*- coding: utf-8 -*-
"""
Paramétrage Robot pour Soft Pos.
Les positions téléphones sont gérées via le dropdown de la page de test.
Retourne au menu Soft Pos (enum=9).
"""
import gc
from PySide6.QtWidgets import (
    QLabel, QPushButton,
    QDialog, QHBoxLayout, QFormLayout, QLineEdit, QVBoxLayout
)
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

        self.boutonRajoutLecteur = self._btn("Rajout Lecteur", self.RajoutLecteur)
        self._grid.addWidget(self.boutonRajoutLecteur, 3, 1, 1, 3, Qt.AlignCenter)

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

    def RajoutLecteur(self):
        from SP_LecteurDB import add_sp_lecteur

        LBL = "color:#FFFFFF; font-size:13px; background:%s; border:none;" % BG
        INP = "color:#000000; background:#FFFFFF; font-size:13px; border-radius:4px; padding:4px;"
        BTN = (
            "QPushButton { background:#FFFF00; color:#000000; font-size:13px;"
            " font-weight:bold; padding:8px 30px; border-radius:6px; }"
            "QPushButton:hover    { background:#FFE033; }"
            "QPushButton:pressed  { background:#CCBB00; }"
        )

        dialog = QDialog(self)
        dialog.setWindowTitle("Rajout Lecteur — Soft Pos")
        dialog.setFixedSize(460, 530)
        dialog.setStyleSheet("background:%s;" % BG)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(10)

        title = QLabel("Nouveau Lecteur Soft Pos")
        title.setStyleSheet("color:#FFFFFF; font-size:18px; font-weight:bold; background:%s;" % BG)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # ── Bouton récupération coordonnées robot ─────────────────────
        BTN_COORD = (
            "QPushButton { background:#00AA55; color:#FFFFFF; font-size:12px;"
            " font-weight:bold; padding:7px 20px; border-radius:6px; }"
            "QPushButton:hover    { background:#00CC66; }"
            "QPushButton:pressed  { background:#008844; }"
        )
        btn_recup = QPushButton("Récupérer position robot")
        btn_recup.setStyleSheet(BTN_COORD)
        layout.addWidget(btn_recup, alignment=Qt.AlignCenter)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setSpacing(8)

        field_defs = [
            ("Nom",  "Nom du lecteur"),
            ("x",    "Position x (m)"),
            ("y",    "Position y (m)"),
            ("z",    "Position z (m)"),
            ("rX",   "Rotation rX (rad)"),
            ("rY",   "Rotation rY (rad)"),
            ("rZ",   "Rotation rZ (rad)"),
            ("topZ", "Hauteur transit topZ (vide = z+0.2)"),
        ]
        fields = {}
        for fname, placeholder in field_defs:
            lbl = QLabel(fname + " :")
            lbl.setStyleSheet(LBL)
            inp = QLineEdit()
            inp.setPlaceholderText(placeholder)
            inp.setStyleSheet(INP)
            form.addRow(lbl, inp)
            fields[fname] = inp

        layout.addLayout(form)

        def on_recup():
            try:
                if self.rob.variabletest == 2:
                    pos = self.rob.robot.getl()
                else:
                    pos = self.rob.position   # position de test (démo)
                coord_keys = ["x", "y", "z", "rX", "rY", "rZ"]
                for k, v in zip(coord_keys, pos):
                    fields[k].setText(f"{v:.6f}")
            except Exception as e:
                self._show_ok_dialog(
                    f"   Impossible de lire la position robot :\n   {e}   \n",
                    w=420, h=130
                )

        btn_recup.clicked.connect(on_recup)

        btn_row = QHBoxLayout()
        btn_ok = QPushButton("Valider")
        btn_ok.setStyleSheet(BTN)
        btn_cancel = QPushButton("Annuler")
        btn_cancel.setStyleSheet(BTN)
        btn_row.addWidget(btn_ok)
        btn_row.addWidget(btn_cancel)
        layout.addLayout(btn_row)

        def on_ok():
            try:
                nom = fields["Nom"].text().strip()
                if not nom:
                    self._show_ok_dialog("   Le nom du lecteur est obligatoire   \n", w=360, h=120)
                    return
                x    = float(fields["x"].text())
                y    = float(fields["y"].text())
                z    = float(fields["z"].text())
                rX   = float(fields["rX"].text())
                rY   = float(fields["rY"].text())
                rZ   = float(fields["rZ"].text())
                topZ_txt = fields["topZ"].text().strip()
                topZ = float(topZ_txt) if topZ_txt else z + 0.2
                add_sp_lecteur(nom, x, y, z, rX, rY, rZ, topZ)
                self._show_ok_dialog(f"   Lecteur '{nom}' ajouté avec succès   \n", w=400, h=120)
                dialog.accept()
            except ValueError:
                self._show_ok_dialog(
                    "   Valeurs invalides.\n   Vérifier les champs numériques.   \n",
                    w=400, h=130
                )

        btn_ok.clicked.connect(on_ok)
        btn_cancel.clicked.connect(dialog.reject)
        dialog.exec()
