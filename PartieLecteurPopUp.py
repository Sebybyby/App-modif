# -*- coding: utf-8 -*-
"""
Converted from Tkinter to PySide6
"""
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QTimer

from InterfaceClass import Interface


class Popup(Interface):
    def execute_command(self):
        print('je suis dans la commande')
        self._popup_dialog = QDialog(self)
        self._popup_dialog.setWindowTitle("Traitement en cours")
        self._popup_dialog.setFixedSize(200, 100)
        layout = QVBoxLayout(self._popup_dialog)
        label_popup = QLabel("Enregistrement en cours")
        label_popup.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_popup)
        self._popup_dialog.show()

        QTimer.singleShot(4000, lambda: self.close_popup(self._popup_dialog))

    def close_popup(self, popup):
        print("je suis dans la fonction")
        popup.close()
