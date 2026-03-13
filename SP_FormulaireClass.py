# -*- coding: utf-8 -*-
"""
Formulaire pour Soft Pos — identique au Formulaire Combinatoire
mais retourne au menu Soft Pos (enum=9).
"""
import gc
from FormulaireClass import Formulaire


class SP_Formulaire(Formulaire):
    def __init__(self):
        super().__init__()
        # Override du titre
        self.titre.setText("Formulaire — Soft Pos")

    def RetourMenu(self):
        self.windowPlace = self.geometry()
        self.destroy()
        gc.collect()
        self.enum = 9  # MenuSoftPos
