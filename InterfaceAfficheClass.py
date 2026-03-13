# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 11:14:22 2021

@author: t0247275
"""

from enum import Enum

class InterfaceAffiche(Enum):
    Menu = 0
    Formulaire = 1
    ParametrageRobot = 2
    Lane5000 = 3
    Move5000 = 4
    IPP350 = 5
    FichierConfigLecteur = 6
    CardNumber = 7
    Accueil = 8
    MenuSoftPos = 9
    # Soft Pos sub-pages
    SP_Formulaire = 10
    SP_ParametreRobot = 11
    SP_Lane5000 = 12
    SP_Move5000 = 13
    SP_Reader = 14
    SP_FichierConfigLecteur = 15
    SP_PopUpChoice = 16
