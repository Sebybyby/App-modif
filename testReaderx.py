# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 11:39:57 2021
Converted from Tkinter to PySide6
@author: t0247275
"""
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout,
    QLabel, QPushButton, QComboBox
)
from PySide6.QtCore import Qt


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Combinatoire test")
        self.resize(800, 500)

        central = QWidget()
        self.setCentralWidget(central)
        central.setStyleSheet("background:#49A;")
        grid = QGridLayout(central)

        optionPositionList = ["Groupe : A", "Groupe : B", "Groupe : C", "Groupe : D", "Groupe : E"]
        optionList = ["Automatique", "Manuel"]

        self.opt = QComboBox()
        for item in optionPositionList:
            self.opt.addItem(item)
        self.opt.hide()
        grid.addWidget(self.opt, 1, 3)

        self.opt2 = QComboBox()
        self.opt2.setStyleSheet("background:#49A; font-size:12px;")
        for item in optionList:
            self.opt2.addItem(item)
        self.opt2.currentTextChanged.connect(self.essaie)
        grid.addWidget(self.opt2, 1, 4)

        label1 = QLabel()
        label1.setStyleSheet("background:#49A;")
        grid.addWidget(label1, 1, 1)

        boutonPass = QPushButton("PASS ")
        boutonPass.setStyleSheet("QPushButton { background:green; font-size:12px; padding:10px 50px; }")
        grid.addWidget(boutonPass, 3, 4)

        boutonFail = QPushButton("  FAIL  ")
        boutonFail.setStyleSheet("QPushButton { background:Red; font-size:12px; padding:10px 50px; }")
        grid.addWidget(boutonFail, 4, 4)

    def ApparitionGroupe(self):
        self.opt.setCurrentIndex(0)
        self.opt.show()
        print("1234")

    def SuppressionGroupe(self):
        self.opt.hide()

    def essaie(self, value):
        if value == "Automatique":
            print("auto")
            self.SuppressionGroupe()
        elif value == "Manuel":
            print("manuel")
            self.ApparitionGroupe()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())
