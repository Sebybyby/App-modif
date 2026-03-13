# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 10:55:33 2021
Converted from Tkinter to PySide6
@author: t0247275
"""

import sys
from PySide6.QtWidgets import QApplication, QMessageBox

from AccueilClass import Accueil
from MenuClass import Menu
from MenuSoftPosClass import MenuSoftPos
from FormulaireClass import Formulaire
from Lane5000Class import Lane5000
from Move5000Class import Move5000
from ParametreRobotClass import ParametreRobot
from ReaderClass import Reader
from RobotClass import Robot
from FichierConfigLecteur import FichierReader
from PopUpCardChoice import PopUp_NbCard
# Soft Pos sub-pages
from SP_FormulaireClass import SP_Formulaire
from SP_ParametreRobotClass import SP_ParametreRobot
from SP_Lane5000Class import SP_Lane5000
from SP_Move5000Class import SP_Move5000
from SP_ReaderClass import SP_Reader
from SP_FichierConfigLecteur import SP_FichierReader
from SP_PopUpChoiceClass import SP_PopUpChoice

test3 = 0
test2 = 0


def CreationFenetre2(menu, place):
    """Parse a geometry string like '980x720+26+26' and apply it."""
    import re
    m = re.match(r'(\d+)x(\d+)(?:\+(-?\d+))?(?:\+(-?\d+))?', place)
    if m:
        w, h = int(m.group(1)), int(m.group(2))
        x = int(m.group(3)) if m.group(3) is not None else 26
        y = int(m.group(4)) if m.group(4) is not None else 26
        menu.setGeometry(x, y, w, h)
        menu.setFixedSize(w, h)
    menu._central.setStyleSheet("background:#1B3A6B;")


def Intercepte():
    reply = QMessageBox.question(
        None, "Notice", "Are you sure to close the window",
        QMessageBox.Ok | QMessageBox.Cancel
    )
    if reply == QMessageBox.Ok:
        menu.destroy()
        global test2
        test2 = 1
        return test2


def Intercepte2():
    reply = QMessageBox.question(
        None, "Notice", "Are you sure to close the window",
        QMessageBox.Ok | QMessageBox.Cancel
    )
    if reply == QMessageBox.Ok:
        menu.destroy()
        global test3
        test3 = 1
        return test3


if __name__ == "__main__":
    app = QApplication.instance() or QApplication(sys.argv)

    menu = Accueil()
    place = '980x720+26+26'
    CreationFenetre2(menu, place)
    menu.protocol("WM_DELETE_WINDOW", Intercepte2)

    menu.mainloop()
    while True:
        if menu.enum == 8:
            place = '980x720+26+26'
            menu = Accueil()
        elif menu.enum == 0:
            place = '980x720+26+26'
            menu = Menu()
        elif menu.enum == 9:
            place = '980x720+26+26'
            menu = MenuSoftPos()
        elif menu.enum == 1:
            place = '980x720+26+26'
            menu = Formulaire()
        elif menu.enum == 3:
            place = '980x720+26+26'
            menu = Lane5000()
        elif menu.enum == 4:
            place = '980x720+26+26'
            menu = Move5000()
        elif menu.enum == 2:
            place = '980x720+26+26'
            menu = ParametreRobot()
        elif menu.enum == 5:
            place = '980x720+26+26'
            menu = Reader()
        elif menu.enum == 6:
            place = '980x720+26+26'
            menu = FichierReader()
        elif menu.enum == 7:
            place = '980x720+26+26'
            menu = PopUp_NbCard()
        # --- Soft Pos sub-pages ---
        elif menu.enum == 10:
            place = '980x720+26+26'
            menu = SP_Formulaire()
        elif menu.enum == 11:
            place = '980x720+26+26'
            menu = SP_ParametreRobot()
        elif menu.enum == 12:
            place = '980x720+26+26'
            menu = SP_Lane5000()
        elif menu.enum == 13:
            place = '980x720+26+26'
            menu = SP_Move5000()
        elif menu.enum == 14:
            place = '980x720+26+26'
            menu = SP_Reader()
        elif menu.enum == 15:
            place = '980x720+26+26'
            menu = SP_FichierReader()
        elif menu.enum == 16:
            place = '980x720+26+26'
            menu = SP_PopUpChoice()

        if test3 == 1:
            break

        CreationFenetre2(menu, place)
        menu.protocol("WM_DELETE_WINDOW", Intercepte)
        menu.mainloop()

        if test2 == 1:
            rob = Robot.Instance()
            if rob.variableconnexion == 1:
                rob.Close()
            break

    sys.exit(0)
