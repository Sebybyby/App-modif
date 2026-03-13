# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 09:59:12 2021
Converted from Tkinter to PySide6
@author: t0247275
"""
from ReadersClass import Readers
from InterfaceAfficheClass import InterfaceAffiche
from FichierClass import Fichier


class AllReader(Readers):
    def __init__(self):
        Readers.__init__(self)
        self.enum = InterfaceAffiche(5)
        self.fichier = Fichier.Instance()
