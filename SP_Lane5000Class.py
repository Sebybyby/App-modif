# -*- coding: utf-8 -*-
"""
Lane5000 pour Soft Pos — retourne au menu Soft Pos (enum=9).
"""
import gc
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

from Lane5000Class import Lane5000
from InterfaceAfficheClass import InterfaceAffiche


class SP_Lane5000(Lane5000):
    def __init__(self):
        super().__init__()
        self.enum = InterfaceAffiche(12)
        # Mise à jour du titre
        self.label1.setText("Lane5000 — Soft Pos")

    def RetourMenu(self):
        self.windowPlace = self.geometry()
        self.destroy()
        try:
            import gc
            gc.collect()
        except Exception:
            pass
        self.enum = 9  # MenuSoftPos
