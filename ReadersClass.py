# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 09:54:12 2021
Converted from Tkinter to PySide6
@author: t0247275
"""
from PySide6.QtWidgets import (
    QLabel, QPushButton, QComboBox, QLineEdit, QFrame, QHBoxLayout,
    QDialog, QVBoxLayout, QApplication, QMessageBox
)
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QBrush
from PySide6.QtCore import Qt, QSize

from InterfaceClass import Interface
import gc
from InterfaceAfficheClass import InterfaceAffiche
from RobotClass import Robot
from FichierClass import Fichier
from Detection_Transaction import FFT_signal


class Readers(Interface, FFT_signal):
    optionListMode = ["Automatique", "Manuel"]
    optionPositionList = [
        "Groupe : A1", "Groupe : B1", "Groupe : C1", "Groupe : D1", "Groupe : E1",
        "Groupe : A2", "Groupe : B2", "Groupe : C2", "Groupe : D2", "Groupe : E2"
    ]

    def __init__(self):
        Interface.__init__(self)
        self.texteOffset = "null"
        self.tabGroupeA = []
        self.saveEtatGroupeA = []
        self.tabGroupeB = []
        self.saveEtatGroupeB = []
        self.tabGroupeD = []
        self.saveEtatGroupeD = []
        self.tabGroupeC = []
        self.saveEtatGroupeC = []
        self.tabGroupeE = []
        self.saveEtatGroupeE = []

        self.tabGroupeA2 = []
        self.saveEtatGroupeA2 = []
        self.tabGroupeB2 = []
        self.saveEtatGroupeB2 = []
        self.tabGroupeD2 = []
        self.saveEtatGroupeD2 = []
        self.tabGroupeC2 = []
        self.saveEtatGroupeC2 = []
        self.tabGroupeE2 = []
        self.saveEtatGroupeE2 = []

        for i in range(0, 11):
            self.saveEtatGroupeA.append(0)
            self.saveEtatGroupeA2.append(0)
        for i in range(0, 13):
            self.saveEtatGroupeB.append(0)
            self.saveEtatGroupeC.append(0)
            self.saveEtatGroupeD.append(0)
            self.saveEtatGroupeE.append(0)
            self.saveEtatGroupeB2.append(0)
            self.saveEtatGroupeC2.append(0)
            self.saveEtatGroupeD2.append(0)
            self.saveEtatGroupeE2.append(0)

        self.rond_pix = QPixmap(40, 40)
        self.rond_pix.fill(Qt.transparent)
        _p = QPainter(self.rond_pix)
        _p.setRenderHint(QPainter.Antialiasing)
        _p.setBrush(QBrush(QColor("#AAAAAA")))
        _p.setPen(Qt.NoPen)
        _p.drawEllipse(0, 0, 40, 40)
        _p.end()
        self.photo_pix = QPixmap("./Image/rondVert.png")
        self.photo2_pix = QPixmap("./Image/rondRouge.png")

        self.robotVariable = Robot.Instance()
        self.fichier = Fichier.Instance()
        self.enum = InterfaceAffiche(5)

        self.AffichageMode()
        self.optGroupe = QComboBox()
        self.optGroupe.setStyleSheet("QComboBox { background:#FFFFFF; color:#000000; font-size:12px; padding:13px; }")
        for item in self.optionPositionList:
            self.optGroupe.addItem(item)
        self._grid.addWidget(self.optGroupe, 1, 0, Qt.AlignLeft | Qt.AlignTop)
        self.optGroupe.hide()

        self.RetourBouton()
        self.PlayBouton()
        self.windowPlace = []
        InterfaceAffiche(3)
        self.test2 = 0
        self.gp = 0
        self.compteur = 0
        self.i = 0
        self.manuelActive = False
        self.titre_build()
        self.testposition2 = 0
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure((1, 2, 3, 4, 5, 6), weight=2)
        self.OffsetIHM()

    def titre_build(self):
        self.label1 = QLabel(" Readers ")
        self.label1.setStyleSheet("color:#FFFFFF; font-size:35px; background:#0054A4;")
        self.label1.setAlignment(Qt.AlignCenter)
        self._grid.addWidget(self.label1, 0, 2, 1, 5)

    def _make_status_btn(self, tab_list, idx):
        btn = QPushButton()
        btn.setIcon(QIcon(self.rond_pix))
        btn.setIconSize(QSize(30, 30))
        btn.setStyleSheet("QPushButton { background:#0054A4; border:none; }")
        btn.setFlat(True)
        btn.clicked.connect(lambda checked=False, n=idx: self.FunctionManuel(n))
        return btn

    def _update_group_icons(self, tab, save):
        for i in range(len(tab)):
            if save[i] == 0:
                tab[i].setIcon(QIcon(self.rond_pix))
            elif save[i] == 2:
                tab[i].setIcon(QIcon(self.photo2_pix))
            elif save[i] == 1:
                tab[i].setIcon(QIcon(self.photo_pix))

    def destroyPop(self):
        gc.collect()

    def PositionCentrage(self):
        self.testposition2 = 1
        self._show_ok_dialog(
            "\n   Positionner le robot \n au centre du deuxième lecteur   \n", w=400, h=120
        )
        try:
            print("1")
            self.robotVariable.Position02()
        except Exception:
            print("error")

    def OffsetIHM(self):
        parts = []
        if self.robotVariable.offsetX != 0:
            parts.append("Attention l'offset X est de : " + str(self.robotVariable.offsetX))
        if self.robotVariable.offsetY != 0:
            parts.append("Attention l'offset Y est de : " + str(self.robotVariable.offsetY))
        if self.robotVariable.offsetZ != 0:
            parts.append("Attention l'offset Z est de : " + str(self.robotVariable.offsetZ))
        if parts:
            self.texteOffset = "\n".join(parts)
            self.labelOffset = QLabel(self.texteOffset)
            self.labelOffset.setStyleSheet("background:red; color:#FFFFFF; font-size:10px;")
            self._grid.addWidget(self.labelOffset, 14, 8)
            pix = QPixmap("./Image/attention.png")
            if not pix.isNull():
                self.photolabel = QLabel()
                self.photolabel.setPixmap(pix.scaled(30, 30, Qt.KeepAspectRatio))
                self._grid.addWidget(self.photolabel, 14, 7)

    def ApparitionGroupe(self):
        self.playBouton.hide()
        self.optGroupe.setCurrentIndex(0)
        self.optGroupe.show()
        self.testGroupe()
        self.GroupeA(self.tabGroupeA, self.saveEtatGroupeA)
        try:
            self.fichier.Manuel()
        except Exception:
            self.PopUpErreurFichier()

        def AffichagePoint(text):
            self.testGroupe()
            if text == "Groupe : A1":
                self.GroupeA(self.tabGroupeA, self.saveEtatGroupeA)
                self.label1.setText("Reader X")
            elif text == "Groupe : C1":
                self.GroupeC(self.tabGroupeC, self.saveEtatGroupeC)
                self.label1.setText("Reader X")
            elif text == "Groupe : D1":
                self.GroupeD(self.tabGroupeD, self.saveEtatGroupeD)
                self.label1.setText("Reader X")
            elif text == "Groupe : E1":
                self.GroupeE(self.tabGroupeE, self.saveEtatGroupeE)
                self.label1.setText("Reader X")
            elif text == "Groupe : B1":
                self.GroupeB(self.tabGroupeB, self.saveEtatGroupeB)
                self.label1.setText("Reader X")
            elif text == "Groupe : A2":
                self.GroupeA(self.tabGroupeA, self.saveEtatGroupeA2)
                self.label1.setText("Vivo")
            elif text == "Groupe : C2":
                self.GroupeC(self.tabGroupeC, self.saveEtatGroupeC2)
                self.label1.setText("Vivo")
            elif text == "Groupe : D2":
                self.GroupeD(self.tabGroupeD, self.saveEtatGroupeD2)
                self.label1.setText("Vivo")
            elif text == "Groupe : E2":
                self.GroupeE(self.tabGroupeE, self.saveEtatGroupeE2)
                self.label1.setText("Vivo")
            elif text == "Groupe : B2":
                self.GroupeB(self.tabGroupeB, self.saveEtatGroupeB2)
                self.label1.setText("Vivo")

        self.optGroupe.currentTextChanged.connect(AffichagePoint)

    def testGroupe(self):
        if self.gp == 0:
            self.SuppGA(self.tabGroupeA)
        elif self.gp == 1:
            self.SuppGB(self.tabGroupeB)
        elif self.gp == 2:
            self.SuppGC(self.tabGroupeC)
        elif self.gp == 3:
            self.SuppGD(self.tabGroupeD)
        elif self.gp == 4:
            self.SuppGE(self.tabGroupeE)
        elif self.gp == 5:
            self.SuppGA(self.tabGroupeA2)
        elif self.gp == 6:
            self.SuppGB(self.tabGroupeB2)
        elif self.gp == 7:
            self.SuppGC(self.tabGroupeC2)
        elif self.gp == 8:
            self.SuppGD(self.tabGroupeD2)
        elif self.gp == 9:
            self.SuppGE(self.tabGroupeE2)

    def AffichageMode(self):
        self.optMode = QComboBox()
        self.optMode.setStyleSheet("QComboBox { background:#FFFFFF; color:#000000; font-size:12px; padding:13px; }")
        for item in self.optionListMode:
            self.optMode.addItem(item)
        self._grid.addWidget(self.optMode, 1, 8, Qt.AlignRight | Qt.AlignTop)

        def Affichage(text):
            if text == "Automatique":
                print("auto")
                self.PlayBouton()
                self.testGroupe()
                self.GroupeA(self.tabGroupeA, self.saveEtatGroupeA)
                self.optGroupe.hide()
            elif text == "Manuel":
                print("manuel")
                self.manuelActive = True
                self.ApparitionGroupe()

        self.GroupeA(self.tabGroupeA, self.saveEtatGroupeA)
        self.optMode.currentTextChanged.connect(Affichage)

    def ModeAutomatique(self):
        self.testGroupe()
        self.GroupeA(self.tabGroupeA, self.saveEtatGroupeA)
        self.robotVariable._init_Position(
            self.robotVariable.position[0], self.robotVariable.position[1],
            self.robotVariable.position[2], self.robotVariable.position[3],
            self.robotVariable.position[4], self.robotVariable.position[5],
            self.robotVariable.coeffx, self.robotVariable.coeffy, self.robotVariable.coeffz
        )
        self.robotVariable.RecupCoordonneeRobot()
        taille = self.robotVariable.size * 2
        self.i = 0
        self.robotVariable.mode = 1
        if self.testposition2 == 0:
            print("auto position")
            self.PositionCentrage()
            self.testposition2 = 1

        for self.i in range(0, taille):
            self.compteur += 1
            try:
                if self.compteur == 1:
                    self.label1.setText("Reader X")
                    try:
                        self.fichier.ReaderX()
                    except Exception:
                        print("error fichier readerx")
                elif self.compteur == 64:
                    self.label1.setText("Vivo")
                    try:
                        self.fichier.Vivo()
                    except Exception:
                        print("error fichier vivo")
                if self.compteur == 64:
                    self.robotVariable._init_Position(
                        self.robotVariable.position2[0], self.robotVariable.position2[1],
                        self.robotVariable.position2[2], self.robotVariable.position[3],
                        self.robotVariable.position[4], self.robotVariable.position[5],
                        self.robotVariable.coeffx, self.robotVariable.coeffy, self.robotVariable.coeffz
                    )
                if self.compteur >= 64:
                    self.i = self.i - 63
                    print(self.i)
                self.robotVariable.Conversion(self.i)
                if self.robotVariable == 2:
                    self.robotVariable.PositionInitiale()
                if self.compteur < 64:
                    self.PopUpMontant()

                if self.test2 == 1:
                    break
                else:
                    self.fichier.GroupeEcriture(self.i)
                    print(self.robotVariable.xRobot, self.robotVariable.yRobot, self.robotVariable.zRobot)
                    if self.robotVariable.variabletest == 2:
                        self.robotVariable.MouvementRobot()

                if self.compteur < 64:
                    if self.i == 10:
                        self.SuppGA(self.tabGroupeA)
                        self.GroupeB(self.tabGroupeB, self.saveEtatGroupeB)
                    elif self.i == 23:
                        self.SuppGB(self.tabGroupeB)
                        self.GroupeC(self.tabGroupeC, self.saveEtatGroupeC)
                    elif self.i == 36:
                        self.SuppGC(self.tabGroupeC)
                        self.GroupeD(self.tabGroupeD, self.saveEtatGroupeD)
                    elif self.i == 49:
                        self.SuppGD(self.tabGroupeD)
                        self.GroupeE(self.tabGroupeE, self.saveEtatGroupeE)
                    elif self.i == 62:
                        self.SuppGE(self.tabGroupeE)
                        self.GroupeA(self.tabGroupeA2, self.saveEtatGroupeA2)
                else:
                    if self.i == 10:
                        self.SuppGA(self.tabGroupeA2)
                        self.GroupeB(self.tabGroupeB2, self.saveEtatGroupeB2)
                    elif self.i == 23:
                        self.SuppGB(self.tabGroupeB2)
                        self.GroupeC(self.tabGroupeC2, self.saveEtatGroupeC2)
                    elif self.i == 36:
                        self.SuppGC(self.tabGroupeC2)
                        self.GroupeD(self.tabGroupeD2, self.saveEtatGroupeD2)
                    elif self.i == 49:
                        self.SuppGD(self.tabGroupeD2)
                        self.GroupeE(self.tabGroupeE2, self.saveEtatGroupeE2)
            except Exception:
                self.PopUpErreurConnexion()
                break

            if self.test2 == 1:
                break
        self.test2 = 0

    def Intercepte(self):
        reply = QMessageBox.question(
            self, "Notice", "Are you sure to close the transaction",
            QMessageBox.Ok | QMessageBox.Cancel
        )
        if reply == QMessageBox.Ok:
            self.test2 = 1
            gc.collect()

    def PopUpErreurConnexion(self):
        self._show_ok_dialog("\n   Erreur de Connexion   \n", w=190, h=120)

    def PopUpErreurFichier(self):
        self._show_ok_dialog("\n   Avez-vous créé le fichier ?   \n", w=300, h=120)

    def PopUpMontant(self):
        confirmed = self._show_ok_cancel_dialog("\n   Taper le Montant   \n", w=200, h=130)
        if not confirmed:
            self.Intercepte()

    def PopUpTransaction(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("")
        dialog.setFixedSize(200, 130)
        dialog.setStyleSheet("background:#0054A4;")
        layout = QVBoxLayout(dialog)
        lbl = QLabel("\n   Transaction :  \n")
        lbl.setStyleSheet("color:#FFFFFF; font-size:14px;")
        lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl)
        btn_layout = QHBoxLayout()
        bpass = QPushButton("  Pass  ")
        bpass.setStyleSheet("QPushButton { background:#00CC00; color:#000000; font-weight:bold; padding:10px 25px; border-radius:6px; }")
        bfail = QPushButton("   Fail   ")
        bfail.setStyleSheet("QPushButton { background:#CC0000; color:#FFFFFF; font-weight:bold; padding:10px 25px; border-radius:6px; }")
        btn_layout.addWidget(bpass)
        btn_layout.addWidget(bfail)
        layout.addLayout(btn_layout)
        bpass.clicked.connect(lambda: self._do_pass(dialog))
        bfail.clicked.connect(lambda: self._do_fail(dialog))
        dialog.exec()

    def _do_pass(self, dialog):
        dialog.accept()
        self.PassTransaction()

    def _do_fail(self, dialog):
        dialog.accept()
        self.FailTransaction()

    def Sontransaction(self):
        trans = self.Verification_transaction()
        if trans is True:
            self.PassTransaction()
        else:
            self.FailTransaction()

    def PassTransaction(self):
        gc.collect()
        try:
            self.fichier.TransactionPass(self.i)
            if self.compteur < 64:
                if self.i >= 0 and self.i < 11:
                    self.tabGroupeA[self.i].setIcon(QIcon(self.photo_pix))
                    self.saveEtatGroupeA[self.i] = 1
                elif self.i >= 11 and self.i < 24:
                    self.tabGroupeB[self.i - 11].setIcon(QIcon(self.photo_pix))
                    self.saveEtatGroupeB[self.i - 11] = 1
                elif self.i >= 24 and self.i < 37:
                    self.tabGroupeC[self.i - 24].setIcon(QIcon(self.photo_pix))
                    self.saveEtatGroupeC[self.i - 24] = 1
                elif self.i >= 37 and self.i < 50:
                    self.tabGroupeD[self.i - 37].setIcon(QIcon(self.photo_pix))
                    self.saveEtatGroupeD[self.i - 37] = 1
                elif self.i >= 50 and self.i < 63:
                    self.tabGroupeE[self.i - 50].setIcon(QIcon(self.photo_pix))
                    self.saveEtatGroupeE[self.i - 50] = 1
            else:
                if self.i >= 0 and self.i < 11:
                    self.tabGroupeA2[self.i].setIcon(QIcon(self.photo_pix))
                    self.saveEtatGroupeA2[self.i] = 1
                elif self.i >= 11 and self.i < 24:
                    self.tabGroupeB2[self.i - 11].setIcon(QIcon(self.photo_pix))
                    self.saveEtatGroupeB2[self.i - 11] = 1
                elif self.i >= 24 and self.i < 37:
                    self.tabGroupeC2[self.i - 24].setIcon(QIcon(self.photo_pix))
                    self.saveEtatGroupeC2[self.i - 24] = 1
                elif self.i >= 37 and self.i < 50:
                    self.tabGroupeD2[self.i - 37].setIcon(QIcon(self.photo_pix))
                    self.saveEtatGroupeD2[self.i - 37] = 1
                elif self.i >= 50 and self.i < 63:
                    self.tabGroupeE2[self.i - 50].setIcon(QIcon(self.photo_pix))
                    self.saveEtatGroupeE2[self.i - 50] = 1
        except Exception:
            self.PopUpErreurFichier()

    def FailTransaction(self):
        gc.collect()
        try:
            self.fichier.TransactionFail(self.i)
            if self.compteur < 64:
                if self.i >= 0 and self.i < 11:
                    self.tabGroupeA[self.i].setIcon(QIcon(self.photo2_pix))
                    self.saveEtatGroupeA[self.i] = 2
                elif self.i >= 11 and self.i < 24:
                    self.tabGroupeB[self.i - 11].setIcon(QIcon(self.photo2_pix))
                    self.saveEtatGroupeB[self.i - 11] = 2
                elif self.i >= 24 and self.i < 37:
                    self.tabGroupeC[self.i - 24].setIcon(QIcon(self.photo2_pix))
                    self.saveEtatGroupeC[self.i - 24] = 2
                elif self.i >= 37 and self.i < 50:
                    self.tabGroupeD[self.i - 37].setIcon(QIcon(self.photo2_pix))
                    self.saveEtatGroupeD[self.i - 37] = 2
                elif self.i >= 50 and self.i < 63:
                    self.tabGroupeE[self.i - 50].setIcon(QIcon(self.photo2_pix))
                    self.saveEtatGroupeE[self.i - 50] = 2
            else:
                if self.i >= 0 and self.i < 11:
                    self.tabGroupeA2[self.i].setIcon(QIcon(self.photo2_pix))
                    self.saveEtatGroupeA2[self.i] = 2
                elif self.i >= 11 and self.i < 24:
                    self.tabGroupeB2[self.i - 11].setIcon(QIcon(self.photo2_pix))
                    self.saveEtatGroupeB2[self.i - 11] = 2
                elif self.i >= 24 and self.i < 37:
                    self.tabGroupeC2[self.i - 24].setIcon(QIcon(self.photo2_pix))
                    self.saveEtatGroupeC2[self.i - 24] = 2
                elif self.i >= 37 and self.i < 50:
                    self.tabGroupeD2[self.i - 37].setIcon(QIcon(self.photo2_pix))
                    self.saveEtatGroupeD2[self.i - 37] = 2
                elif self.i >= 50 and self.i < 63:
                    self.tabGroupeE2[self.i - 50].setIcon(QIcon(self.photo2_pix))
                    self.saveEtatGroupeE2[self.i - 50] = 2
        except Exception:
            self.PopUpErreurFichier()

    def RetourBouton(self):
        self.retourBouton = QPushButton("RETOUR")
        self.retourBouton.setStyleSheet(
            "QPushButton { background:#CC0000; color:#FFFFFF; font-size:16px; font-weight:bold; padding:15px 30px; border-radius:10px; }"
            "QPushButton:pressed { background:#AA0000; }"
        )
        self.retourBouton.clicked.connect(self.RetourMenu)
        self._grid.addWidget(self.retourBouton, 14, 0, 1, 2, Qt.AlignLeft | Qt.AlignBottom)

    def PlayBouton(self):
        self.playBouton = QPushButton("RUN")
        self.playBouton.setStyleSheet(
            "QPushButton { background:#00CC00; color:#000000; font-size:16px; font-weight:bold; padding:15px 30px; border-radius:10px; }"
            "QPushButton:pressed { background:#009900; }"
        )
        self.playBouton.clicked.connect(self.ModeAutomatique)
        self._grid.addWidget(self.playBouton, 14, 7, 1, 2, Qt.AlignRight | Qt.AlignBottom)

    def RetourMenu(self):
        self.windowPlace = self.geometry()
        self.destroy()
        gc.collect()
        self.enum = 0

    # ---- Group creation helpers ----
    def GroupeA(self, tabGroupeA, saveEtatGroupeA):
        tabGroupeA.clear()
        if tabGroupeA is self.tabGroupeA:
            self.gp = 0
        elif tabGroupeA is self.tabGroupeA2:
            self.gp = 5
        positions = [(6,4),(5,6),(2,4),(5,2),(7,2),(9,4),(7,6),(5,5),(5,3),(7,3),(7,5)]
        for idx, (row, col) in enumerate(positions):
            btn = self._make_status_btn(tabGroupeA, idx)
            tabGroupeA.append(btn)
            self._grid.addWidget(btn, row, col, Qt.AlignLeft | Qt.AlignTop)
        self._update_group_icons(tabGroupeA, saveEtatGroupeA)

    def GroupeB(self, tabGroupeB, saveEtatGroupeB):
        tabGroupeB.clear()
        if tabGroupeB is self.tabGroupeB:
            self.gp = 1
        elif tabGroupeB is self.tabGroupeB2:
            self.gp = 6
        positions = [(5,4),(4,6),(3,4),(4,2),(6,2),(7,4),(6,6),(5,7),(2,6),(2,2),(5,1),(8,2),(8,6)]
        for idx, (row, col) in enumerate(positions):
            btn = self._make_status_btn(tabGroupeB, 11 + idx)
            tabGroupeB.append(btn)
            self._grid.addWidget(btn, row, col, Qt.AlignLeft | Qt.AlignTop)
        self._update_group_icons(tabGroupeB, saveEtatGroupeB)

    def GroupeC(self, tabGroupeC, saveEtatGroupeC):
        tabGroupeC.clear()
        if tabGroupeC is self.tabGroupeC:
            self.gp = 2
        elif tabGroupeC is self.tabGroupeC2:
            self.gp = 7
        positions = [(7,4),(7,6),(5,5),(5,3),(7,2),(9,3),(9,5),(5,7),(1,4),(5,1),(9,1),(12,4),(9,7)]
        for idx, (row, col) in enumerate(positions):
            btn = self._make_status_btn(tabGroupeC, 24 + idx)
            tabGroupeC.append(btn)
            self._grid.addWidget(btn, row, col, Qt.AlignLeft | Qt.AlignTop)
        self._update_group_icons(tabGroupeC, saveEtatGroupeC)

    def GroupeD(self, tabGroupeD, saveEtatGroupeD):
        tabGroupeD.clear()
        if tabGroupeD is self.tabGroupeD:
            self.gp = 3
        elif tabGroupeD is self.tabGroupeD2:
            self.gp = 8
        positions = [(5,4),(4,6),(3,4),(4,2),(6,2),(7,4),(6,6),(5,7),(2,6),(2,2),(5,1),(8,2),(8,6)]
        for idx, (row, col) in enumerate(positions):
            btn = self._make_status_btn(tabGroupeD, 37 + idx)
            tabGroupeD.append(btn)
            self._grid.addWidget(btn, row, col, Qt.AlignLeft | Qt.AlignTop)
        self._update_group_icons(tabGroupeD, saveEtatGroupeD)

    def GroupeE(self, tabGroupeE, saveEtatGroupeE):
        tabGroupeE.clear()
        if tabGroupeE is self.tabGroupeE:
            self.gp = 4
        elif tabGroupeE is self.tabGroupeE2:
            self.gp = 9
        positions = [(7,4),(7,6),(5,5),(5,3),(7,2),(9,3),(9,5),(5,7),(1,4),(5,1),(9,1),(12,4),(9,7)]
        for idx, (row, col) in enumerate(positions):
            btn = self._make_status_btn(tabGroupeE, 50 + idx)
            tabGroupeE.append(btn)
            self._grid.addWidget(btn, row, col, Qt.AlignLeft | Qt.AlignTop)
        self._update_group_icons(tabGroupeE, saveEtatGroupeE)

    def SuppGA(self, tabGroupeA):
        for btn in tabGroupeA:
            btn.hide()

    def SuppGB(self, tabGroupeB):
        for btn in tabGroupeB:
            btn.hide()

    def SuppGC(self, tabGroupeC):
        for btn in tabGroupeC:
            btn.hide()

    def SuppGD(self, tabGroupeD):
        for btn in tabGroupeD:
            btn.hide()

    def SuppGE(self, tabGroupeE):
        for btn in tabGroupeE:
            btn.hide()

    def FunctionManuel(self, number):
        if self.manuelActive is True:
            if self.testposition2 == 0:
                self.PositionCentrage()
                print("manuel position")
                self.testposition2 = 1
            try:
                self.i = number
                self.robotVariable.mode = 2
                self.robotVariable.RecupCoordonneeRobot()
                current_groupe = self.optGroupe.currentText()
                if self.robotVariable.variabletest == 2:
                    if ("A2" in current_groupe or "B2" in current_groupe or
                            "C2" in current_groupe or "D2" in current_groupe or "E2" in current_groupe):
                        self.robotVariable._init_Position(
                            self.robotVariable.position2[0], self.robotVariable.position2[1],
                            self.robotVariable.position2[2], self.robotVariable.position[3],
                            self.robotVariable.position[4], self.robotVariable.position[5],
                            self.robotVariable.coeffx, self.robotVariable.coeffy, self.robotVariable.coeffz
                        )
                        self.robotVariable.Conversion(self.i)
                        self.robotVariable.MouvementRobot()
                    elif ("A1" in current_groupe or "B1" in current_groupe or
                            "C1" in current_groupe or "D1" in current_groupe or "E1" in current_groupe):
                        self.PopUpMontant()
                        self.robotVariable._init_Position(
                            self.robotVariable.position[0], self.robotVariable.position[1],
                            self.robotVariable.position[2], self.robotVariable.position[3],
                            self.robotVariable.position[4], self.robotVariable.position[5],
                            self.robotVariable.coeffx, self.robotVariable.coeffy, self.robotVariable.coeffz
                        )
                        self.Record_son()
                        self.robotVariable.Conversion(self.i)
                        self.robotVariable.MouvementRobot()
                else:
                    if ("A2" in current_groupe or "B2" in current_groupe or
                            "C2" in current_groupe or "D2" in current_groupe or "E2" in current_groupe):
                        self.robotVariable._init_Position(
                            self.robotVariable.position2[0], self.robotVariable.position2[1],
                            self.robotVariable.position2[2], self.robotVariable.position[3],
                            self.robotVariable.position[4], self.robotVariable.position[5],
                            self.robotVariable.rX, self.robotVariable.rY, self.robotVariable.rZ
                        )
                        self.robotVariable.Conversion(self.i)
                        print(self.robotVariable.xRobot, self.robotVariable.yRobot, self.robotVariable.zRobot)
                    elif ("A1" in current_groupe or "B1" in current_groupe or
                            "C1" in current_groupe or "D1" in current_groupe or "E1" in current_groupe):
                        self.PopUpMontant()
                        self.robotVariable._init_Position(
                            self.robotVariable.position[0], self.robotVariable.position[1],
                            self.robotVariable.position[2], self.robotVariable.position[3],
                            self.robotVariable.position[4], self.robotVariable.position[5],
                            self.robotVariable.rX, self.robotVariable.rY, self.robotVariable.rZ
                        )
                        self.Record_son()
                        self.robotVariable.Conversion(self.i)
                        print(self.robotVariable.xRobot, self.robotVariable.yRobot, self.robotVariable.zRobot)
                self.Sontransaction()
            except Exception:
                self.PopUpErreurConnexion()
