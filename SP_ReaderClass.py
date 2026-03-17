# -*- coding: utf-8 -*-
"""
IPP350 / Reader pour Soft Pos.
Override du dropdown lecteur → affiche les téléphones Soft Pos depuis sp_lecteurs.xlsx.
Retourne au menu Soft Pos (enum=9).
"""
import gc
from PySide6.QtWidgets import QComboBox
from PySide6.QtCore import Qt

from ReaderClass import Reader, COMBO_STYLE
from InterfaceAfficheClass import InterfaceAffiche
from SP_LecteurDB import get_sp_lecteurs, get_sp_lecteur_position


class SP_Reader(Reader):
    def __init__(self):
        super().__init__()
        self.enum = InterfaceAffiche(14)

    # ------------------------------------------------------------------
    # Override : dropdown téléphones Soft Pos (sp_lecteurs.xlsx)
    # ------------------------------------------------------------------
    def AfficheReader(self):
        """Remplace le dropdown lecteur par la liste des téléphones Soft Pos."""
        self.optLecteur = QComboBox()
        self.optLecteur.setStyleSheet(COMBO_STYLE)
        self.optLecteur.blockSignals(True)
        for name in get_sp_lecteurs():
            self.optLecteur.addItem(name)
        self.optLecteur.blockSignals(False)
        self._grid.addWidget(self.optLecteur, 1, 6, Qt.AlignRight | Qt.AlignTop)
        self.optLecteur.currentTextChanged.connect(self._on_reader_change)
        initial = self.optLecteur.currentText()
        if initial:
            self._on_reader_change(initial)

    def _on_reader_change(self, name):
        """Positionne le robot sur la position initiale du téléphone sélectionné."""
        pos = get_sp_lecteur_position(name)
        if pos is None:
            return
        self.robotVariable._init_Position(
            pos["x"], pos["y"], pos["z"],
            pos["rX"], pos["rY"], pos["rZ"],
            self.robotVariable.coeffx,
            self.robotVariable.coeffy,
            self.robotVariable.coeffz,
        )
        # Synchronise la liste `position` pour ReadersClass.ModeAutomatique
        self.robotVariable.position = [
            pos["x"], pos["y"], pos["z"],
            pos["rX"], pos["rY"], pos["rZ"],
        ]
        self.robotVariable.positionTopZ = pos["topZ"]
        try:
            self.fichier.EcritureLecteur(name)
        except Exception:
            pass
        print(f"SP Lecteur: {name}, topZ={pos['topZ']}")

    # ------------------------------------------------------------------
    def RetourMenu(self):
        self.windowPlace = self.geometry()
        self.destroy()
        try:
            gc.collect()
        except Exception as e:
            print(f"Erreur lors de l'arrêt: {e}")
        self.enum = 9  # MenuSoftPos
