# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 11:18:36 2021
Converted from Tkinter to PySide6
@author: t0247275
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QRadioButton,
    QButtonGroup
)
from PySide6.QtCore import Qt

BG = "#0054A4"

LBL_STYLE = (
    "color:#FFFFFF; font-size:14px; font-weight:bold;"
    " background:transparent; border:none;"
)
BTN_YELLOW = (
    "QPushButton { background:#FFFF00; color:#000000; font-size:13px;"
    " font-weight:bold; padding:8px 28px; border-radius:6px; }"
    "QPushButton:hover    { background:#FFE033; }"
    "QPushButton:pressed  { background:#CCBB00; }"
)
RB_STYLE = (
    "QRadioButton { color:#FFFFFF; background:transparent; font-size:14px;"
    " padding:4px; spacing:10px; }"
    "QRadioButton::indicator {"
    "  width:20px; height:20px; border-radius:10px;"
    "  border:2px solid #8AAAD4; background:#FFFFFF;"
    "}"
    "QRadioButton::indicator:checked {"
    "  background:#FFFF00; border:3px solid #FFFFFF;"
    "}"
    "QRadioButton::indicator:unchecked:hover {"
    "  border:2px solid #FFE033;"
    "}"
)


class PopUp(QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.message = message
        self.setFixedSize(300, 200)
        self.setStyleSheet(f"background:{BG};")

    def ContenuButtonOk(self):
        self.i = 0
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        self.text = QLabel(self.message)
        self.text.setStyleSheet(LBL_STYLE)
        self.text.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.text)
        self.B1 = QPushButton("Ok")
        self.B1.setStyleSheet(BTN_YELLOW)
        self.B1.clicked.connect(self.accept)
        layout.addWidget(self.B1, alignment=Qt.AlignBottom | Qt.AlignCenter)

    def PopPassOuFail(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        self.text = QLabel(self.message)
        self.text.setStyleSheet(LBL_STYLE)
        self.text.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.text)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        self.B1 = QPushButton("PASS")
        self.B1.setStyleSheet(
            "QPushButton { background:#00AA44; color:#FFFFFF; font-size:13px;"
            " font-weight:bold; padding:8px 24px; border-radius:6px; }"
            "QPushButton:hover    { background:#00CC55; }"
            "QPushButton:pressed  { background:#008833; }"
        )
        self.B1.clicked.connect(self.accept)
        self.B2 = QPushButton("FAIL")
        self.B2.setStyleSheet(
            "QPushButton { background:#CC2200; color:#FFFFFF; font-size:13px;"
            " font-weight:bold; padding:8px 24px; border-radius:6px; }"
            "QPushButton:hover    { background:#EE3300; }"
            "QPushButton:pressed  { background:#AA1100; }"
        )
        self.B2.clicked.connect(self.accept)
        btn_layout.addWidget(self.B1)
        btn_layout.addWidget(self.B2)
        layout.addLayout(btn_layout)

    def cb_i_checked(self):
        choice = self._get_choice()
        self.compteur = []
        if choice == "1Card":
            self.compteur.append("Card 1")
        elif choice == "2Card":
            self.compteur.append("Card 1")
            self.compteur.append("Card 2")
        else:
            self.compteur.append("Card 1")
            self.compteur.append("Card 2")
            self.compteur.append("Card 3")
        print(self.compteur)
        self.accept()

    def _get_choice(self):
        for rb, val in [(self.rb1, "1Card"), (self.rb2, "2Card"), (self.rb3, "3Card")]:
            if rb.isChecked():
                return val
        return "1Card"

    def PopNb_carte(self):
        self.compteur = []
        self.Compteurcard = 0
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        label = QLabel("Nombre de cartes")
        label.setStyleSheet(LBL_STYLE)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self._btn_group = QButtonGroup(self)
        self.rb1 = QRadioButton("1 Card")
        self.rb1.setStyleSheet(RB_STYLE)
        self.rb2 = QRadioButton("2 Cards")
        self.rb2.setStyleSheet(RB_STYLE)
        self.rb3 = QRadioButton("3 Cards")
        self.rb3.setStyleSheet(RB_STYLE)
        self.rb1.setChecked(True)
        self._btn_group.addButton(self.rb1)
        self._btn_group.addButton(self.rb2)
        self._btn_group.addButton(self.rb3)
        layout.addWidget(self.rb1)
        layout.addWidget(self.rb2)
        layout.addWidget(self.rb3)

        bt = QPushButton("Valider")
        bt.setStyleSheet(BTN_YELLOW)
        bt.clicked.connect(self.cb_i_checked)
        layout.addWidget(bt, alignment=Qt.AlignCenter)
