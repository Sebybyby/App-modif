# -*- coding: utf-8 -*-
"""
IPP350 / Reader pour Soft Pos.
Override du dropdown lecteur → affiche les téléphones Soft Pos.
Retourne au menu Soft Pos (enum=9).
"""
import gc
from PySide6.QtWidgets import QComboBox
from PySide6.QtCore import Qt

from ReaderClass import Reader, COMBO_STYLE
from InterfaceAfficheClass import InterfaceAffiche
from SP_TelephoneDB import get_telephones, get_telephone_method


class SP_Reader(Reader):
    def __init__(self):
        super().__init__()
        self.enum = InterfaceAffiche(14)

    # ------------------------------------------------------------------
    # Override : dropdown téléphones au lieu des lecteurs (Lane5000/Move5000)
    # ------------------------------------------------------------------
    def AfficheReader(self):
        """Remplace le dropdown lecteur par la liste des téléphones Soft Pos."""
        self.optLecteur = QComboBox()
        self.optLecteur.setStyleSheet(COMBO_STYLE)
        self.optLecteur.blockSignals(True)
        for name in get_telephones():
            self.optLecteur.addItem(name)
        self.optLecteur.blockSignals(False)
        self._grid.addWidget(self.optLecteur, 1, 6, Qt.AlignRight | Qt.AlignTop)
        self.optLecteur.currentTextChanged.connect(self._on_reader_change)

    def _on_reader_change(self, name):
        """Positionne le robot sur la position initiale du téléphone sélectionné."""
        method_suffix = get_telephone_method(name)
        if method_suffix is None:
            return
        try:
            # Ex : self.robotVariable.Position0_IphoneSE()
            getattr(self.robotVariable, f"Position0_{method_suffix}")()
        except Exception as e:
            print(f"Erreur position téléphone '{name}': {e}")
        try:
            self.fichier.EcritureLecteur(name)
        except Exception:
            pass

    # ------------------------------------------------------------------
    def RetourMenu(self):
        self.windowPlace = self.geometry()
        self.destroy()
        try:
            gc.collect()
        except Exception as e:
            print(f"Erreur lors de l'arrêt: {e}")
        self.enum = 9  # MenuSoftPos
