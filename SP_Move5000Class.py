# -*- coding: utf-8 -*-
"""
Move5000 pour Soft Pos — retourne au menu Soft Pos (enum=9).
"""
import gc
from Move5000Class import Move5000
from InterfaceAfficheClass import InterfaceAffiche


class SP_Move5000(Move5000):
    def __init__(self):
        super().__init__()
        self.enum = InterfaceAffiche(13)
        # Mise à jour du titre
        self.titre.setText("Move5000 — Soft Pos")

    def RetourMenu(self):
        self.windowPlace = self.geometry()
        self.destroy()
        try:
            gc.collect()
        except Exception:
            pass
        self.enum = 9  # MenuSoftPos
