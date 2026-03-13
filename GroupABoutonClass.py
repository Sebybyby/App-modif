# -*- coding: utf-8 -*-
"""
Created on Mon May  3 16:32:38 2021
Converted from Tkinter to PySide6
@author: t0247275
"""
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt

from InterfaceClass import Interface


class GroupABouton(Interface):
    def __init__(self):
        Interface.__init__(self)
        self.ButtonCreation(1, 3, "2")
        self.ButtonCreation(3, 3, "0")
        self.ButtonCreation(2, 1, "3")
        self.ButtonCreation(2, 2, "8")
        self.ButtonCreation(2, 4, "7")
        self.ButtonCreation(2, 5, "1")
        self.ButtonCreation(4, 1, "4")
        self.ButtonCreation(4, 2, "9")
        self.ButtonCreation(4, 4, "10")
        self.ButtonCreation(4, 5, "6")
        self.ButtonCreation(5, 3, "5")

    def ButtonCreation(self, row, column, text):
        btn = QPushButton(text)
        btn.setStyleSheet(
            "QPushButton { color:#242874; font-size:14px; background:#FFFFFF; border-radius:4px; }"
            "QPushButton:hover    { background:#FFE033; }"
            "QPushButton:pressed  { background:#CCBB00; }"
        )
        self._grid.addWidget(btn, row, column)
