# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 09:43:44 2021
Converted from Tkinter to PySide6
@author: t0247275
"""
from PySide6.QtWidgets import (
    QLabel, QPushButton, QComboBox, QLineEdit, QFrame, QHBoxLayout,
    QDialog, QVBoxLayout, QApplication, QMessageBox
)
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QBrush
from PySide6.QtCore import Qt, QSize, Signal

from InterfaceClass import Interface
from InterfaceAfficheClass import InterfaceAffiche
from RobotClass import Robot
from FichierClass import Fichier
from Detection_Transaction import FFT_signal
from PopUpCardChoice import PopUp_NbCard
import gc
import time
import threading
import json


COMBO_STYLE = (
    "QComboBox { background:#FFFFFF; color:#000000; font-size:12px;"
    " padding:6px 10px; border-radius:5px; border:2px solid #CCCCCC; min-width:110px; }"
    "QComboBox::drop-down { border:none; padding-right:4px; }"
    "QComboBox QAbstractItemView {"
    " background:#FFFFFF; color:#000000; border:2px solid #0054A4;"
    " selection-background-color:#0054A4; selection-color:#FFFFFF; }"
)


class Reader(FFT_signal, Interface):
    optionListMode = ["Automatique", "Manuel"]
    optionListCard = []
    optionPositionList = ["Groupe : A", "Groupe : B", "Groupe : C", "Groupe : D", "Groupe : E"]

    _sig_pass_auto    = Signal(int, int)
    _sig_fail_auto    = Signal(int, int)
    _sig_card_text    = Signal(str)
    _sig_group_switch = Signal(int)
    _sig_auto_error   = Signal()
    _sig_auto_finished = Signal()

    def __init__(self):
        Interface.__init__(self)
        with open("cartes.json", "r") as f:
            data = json.load(f)
            self.optionListCard = data.get("cartes", [])
        print("monstre : " + str(self.optionListCard))
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
        for i in range(0, 12):
            self.saveEtatGroupeA.append(0)
        for i in range(0, 13):
            self.saveEtatGroupeB.append(0)
            self.saveEtatGroupeC.append(0)
            self.saveEtatGroupeD.append(0)
            self.saveEtatGroupeE.append(0)

        self.cardSelect = 0
        self.saveEtatByCard = []
        for i in self.optionListCard:
            self.saveEtatByCard.append({
                'A': [0] * 12,
                'B': [0] * 13,
                'C': [0] * 13,
                'D': [0] * 13,
                'E': [0] * 13,
            })

        # Load pixmaps — cercle neutre gris clair créé programmatiquement
        self.rond_pix = QPixmap(54, 54)
        self.rond_pix.fill(Qt.transparent)
        _p = QPainter(self.rond_pix)
        _p.setRenderHint(QPainter.Antialiasing)
        _p.setBrush(QBrush(QColor("#CCCCCC")))
        _p.setPen(Qt.NoPen)
        _p.drawEllipse(0, 0, 54, 54)
        _p.end()
        self.photo_pix = QPixmap("./Image/rondVert.png")
        self.photo2_pix = QPixmap("./Image/rondRouge.png")

        self.robotVariable = Robot.Instance()
        self.fichier = Fichier.Instance()
        self.currentCardLoop = 0
        self._stopAutoFlag = False
        self._group_switch_done = threading.Event()
        self._sig_pass_auto.connect(self._on_pass_auto)
        self._sig_fail_auto.connect(self._on_fail_auto)
        self._sig_card_text.connect(self._on_card_text)
        self._sig_group_switch.connect(self._on_group_switch)
        self._sig_auto_error.connect(self.PopUpErreurConnexion)
        self._sig_auto_finished.connect(self._on_auto_finished)
        self.PlayBouton()
        self._DeposeBouton()
        self.AffichageMode()
        self.AffichageCard()
        self.AfficheReader()
        self.RetourBouton()
        self.ZoneAcceleration()
        self.ZoneTemporisation()
        self.CMDAcceleration = 8
        self.CMDTemporisation = 1
        self.windowPlace = []
        InterfaceAffiche(3)
        self.test2 = 0
        self.gp = 0
        self.i = 0
        self.manuelActive = False
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), weight=1)
        self.grid_rowconfigure(14, weight=2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure((1, 2, 3, 4, 5, 6), weight=2)
        self.OffsetIHM()

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

    def _make_status_btn(self, idx):
        btn = QPushButton()
        btn.setIcon(QIcon(self.rond_pix))
        btn.setIconSize(QSize(50, 50))
        btn.setFixedSize(58, 58)
        btn.setStyleSheet("QPushButton { background:#1B3A6B; border:none; padding:0px; }")
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

    def ApparitionGroupe(self):
        self.playBouton.hide()
        self.optGroupe.setCurrentIndex(0)
        self.optGroupe.show()
        self.testGroupe()
        self.GroupeA()
        try:
            self.fichier.Manuel()
        except Exception:
            self.PopUpErreurFichier()

        def AffichagePoint(text):
            self.testGroupe()
            if text == "Groupe : A":
                self.GroupeA()
            elif text == "Groupe : C":
                self.GroupeC()
            elif text == "Groupe : D":
                self.GroupeD()
            elif text == "Groupe : E":
                self.GroupeE()
            elif text == "Groupe : B":
                self.GroupeB()

        self.optGroupe.currentTextChanged.connect(AffichagePoint)

    def AfficheReader(self):
        from LecteurDB import get_lecteurs
        self.optLecteur = QComboBox()
        self.optLecteur.setStyleSheet(COMBO_STYLE)
        self.optLecteur.blockSignals(True)
        for name in get_lecteurs():
            self.optLecteur.addItem(name)
        self.optLecteur.blockSignals(False)
        self._grid.addWidget(self.optLecteur, 1, 6, Qt.AlignRight | Qt.AlignTop)
        self.optLecteur.currentTextChanged.connect(self._on_reader_change)
        initial_reader = self.optLecteur.currentText()
        if initial_reader:
            self._on_reader_change(initial_reader)

    def _on_reader_change(self, name):
        from LecteurDB import get_lecteur_position
        pos = get_lecteur_position(name)
        if pos is None:
            return
        self.robotVariable._init_Position(
            pos["x"], pos["y"], pos["z"],
            pos["rX"], pos["rY"], pos["rZ"],
            self.robotVariable.coeffx,
            self.robotVariable.coeffy,
            self.robotVariable.coeffz,
        )
        # Synchronise la liste `position` utilisée par ReadersClass.ModeAutomatique
        self.robotVariable.position = [
            pos["x"], pos["y"], pos["z"],
            pos["rX"], pos["rY"], pos["rZ"],
        ]
        self.robotVariable.positionTopZ = pos["topZ"]
        try:
            self.fichier.EcritureLecteur(name)
        except Exception:
            pass
        print(f"Lecteur: {name}, topZ={pos['topZ']}")

    def AffichageCard(self):
        self.optCard = QComboBox()
        self.optCard.setStyleSheet(COMBO_STYLE)
        for item in self.optionListCard:
            self.optCard.addItem(item)
        self._grid.addWidget(self.optCard, 1, 7, Qt.AlignRight | Qt.AlignTop)
        self.optCard.currentTextChanged.connect(self.on_card_change)

    def testGroupe(self):
        if self.gp == 0:
            self.SuppGA()
        elif self.gp == 1:
            self.SuppGB()
        elif self.gp == 2:
            self.SuppGC()
        elif self.gp == 3:
            self.SuppGD()
        elif self.gp == 4:
            self.SuppGE()

    def on_card_change(self, *args):
        try:
            selected_card = self.optCard.currentText()
            card_index = self.optionListCard.index(selected_card)
            self.cardSelect = card_index
            self.saveEtatGroupeA = self.saveEtatByCard[card_index]['A']
            self.saveEtatGroupeB = self.saveEtatByCard[card_index]['B']
            self.saveEtatGroupeC = self.saveEtatByCard[card_index]['C']
            self.saveEtatGroupeD = self.saveEtatByCard[card_index]['D']
            self.saveEtatGroupeE = self.saveEtatByCard[card_index]['E']
            print(f"Carte sélectionnée: {selected_card} (index: {card_index})")
            try:
                self.testGroupe()
                self.GroupeA()
                QApplication.processEvents()
            except Exception:
                pass
        except Exception:
            pass

    def AffichageMode(self):
        self.optMode = QComboBox()
        self.optMode.setStyleSheet(COMBO_STYLE)
        for item in self.optionListMode:
            self.optMode.addItem(item)
        self._grid.addWidget(self.optMode, 1, 8, Qt.AlignRight | Qt.AlignTop)

        # Create optGroupe (hidden by default)
        self.optGroupe = QComboBox()
        self.optGroupe.setStyleSheet(COMBO_STYLE)
        for item in self.optionPositionList:
            self.optGroupe.addItem(item)
        self._grid.addWidget(self.optGroupe, 1, 0, Qt.AlignLeft | Qt.AlignTop)
        self.optGroupe.hide()

        def Affichage(text):
            if text == "Automatique":
                print("auto")
                self.PlayBouton()
                self.testGroupe()
                self.GroupeA()
                self.optGroupe.hide()
            elif text == "Manuel":
                print("manuel")
                self.manuelActive = True
                self.ApparitionGroupe()

        self.GroupeA()
        self.optMode.currentTextChanged.connect(Affichage)

    # ------------------------------------------------------------------
    # DÉPOSE CARTE button
    # ------------------------------------------------------------------
    def _DeposeBouton(self):
        self.deposerCarteBtn = QPushButton("DÉPOSE\nCARTE")
        self.deposerCarteBtn.setFixedSize(140, 55)
        self.deposerCarteBtn.setStyleSheet(
            "QPushButton { background:#FF8800; color:#FFFFFF; font-size:13px;"
            " font-weight:bold; border-radius:12px; }"
            "QPushButton:hover   { background:#FFA033; }"
            "QPushButton:pressed { background:#CC6600; }"
        )
        self.deposerCarteBtn.clicked.connect(self._DeposerCarte)
        self._grid.addWidget(self.deposerCarteBtn, 14, 8, 1, 1, Qt.AlignRight | Qt.AlignVCenter)
        self.deposerCarteBtn.hide()

    def _DeposerCarte(self):
        """Stop automation immediately and return the current card to its slot."""
        self._stopAutoFlag = True
        card_idx = self.currentCardLoop
        def do_pose():
            try:
                self.robotVariable.PoseCarte(card_idx + 1)
            except Exception as e:
                print(f"Erreur dépose carte: {e}")
        threading.Thread(target=do_pose, daemon=True).start()

    # ------------------------------------------------------------------
    # Automation (non-blocking)
    # ------------------------------------------------------------------
    def ModeAutomatique(self):
        """Launch automatic mode in a background thread so the UI stays responsive."""
        self._stopAutoFlag = False
        try:
            self.optMode.setEnabled(False)
            self.optCard.setEnabled(False)
            self.optGroupe.setEnabled(False)
            self.playBouton.hide()
            self.deposerCarteBtn.show()
        except Exception:
            pass

        self.testGroupe()
        self.GroupeA()
        self.robotVariable.mode = 1
        self.robotVariable.RecupCoordonneeRobot()
        self.i = 0

        threading.Thread(target=self._ModeAutomatiqueWorker, daemon=True).start()

    def _ModeAutomatiqueWorker(self):
        """Background thread: runs all robot movements for the automatic test."""
        ErrorOccured = False
        try:
            for cardloop in range(0, len(self.optionListCard)):
                self.currentCardLoop = cardloop

                try:
                    if self._stopAutoFlag:
                        break
                    self.robotVariable.RecuperationCarte(cardloop + 1)
                    print(f"Carte {cardloop} récupérée")
                except Exception:
                    pass

                self._sig_card_text.emit(self.optionListCard[cardloop])
                print(f"\n DÉBUT Test de la carte {cardloop} \n")

                for self.i in range(0, self.robotVariable.size):
                    if self._stopAutoFlag:
                        break
                    try:
                        if self.robotVariable.variabletest == 2:
                            print("robot initial")

                        self.fichier.GroupeEcriture(self.i)
                        self.robotVariable.Conversion(self.i)

                        if self.robotVariable.variabletest == 2:
                            tic = time.perf_counter()

                            t1 = threading.Thread(
                                target=self.robotVariable.MouvementRobotCarte,
                                args=(self._stopAutoFlag, self.CMDAcceleration, self.CMDTemporisation)
                            )
                            t2 = threading.Thread(target=self.Record_son)
                            t1.start()
                            t2.start()
                            t1.join()
                            t2.join()
                            toc = time.perf_counter()
                            print(f"time: {toc - tic:0.4f} seconds")

                        Trans = self.lecture_son()
                        print(Trans)
                        # Trans = True

                        if Trans:
                            self._sig_pass_auto.emit(self.i, cardloop)
                        else:
                            self._sig_fail_auto.emit(self.i, cardloop)

                        # Group switch (grippergrip in worker, UI update on main thread)
                        if self.i in (10, 23, 36, 49):
                            if self.robotVariable.variabletest == 2:
                                self.robotVariable.grippergrip()
                            self._group_switch_done.clear()
                            self._sig_group_switch.emit(self.i)
                            self._group_switch_done.wait(timeout=5.0)
                        elif self.i == 62:
                            print("END Carte")
                            break

                        time.sleep(3)  # delay between test positions

                    except Exception as e:
                        self._sig_auto_error.emit()
                        print(e)
                        ErrorOccured = True
                        break

                    if self._stopAutoFlag:
                        break

                if ErrorOccured or self._stopAutoFlag:
                    break

                print(f"FIN Test de la carte {cardloop}")
                time.sleep(2)

            if not self._stopAutoFlag:
                print("TOUS LES TESTS TERMINÉS")
        finally:
            self._sig_auto_finished.emit()

    # ------------------------------------------------------------------
    # Signal handlers (execute on main thread)
    # ------------------------------------------------------------------
    def _on_card_text(self, text):
        try:
            self.optCard.setCurrentText(text)
            QApplication.processEvents()
        except Exception:
            pass

    def _on_pass_auto(self, i, cardloop):
        try:
            if 0 <= i < 11:
                self.tabGroupeA[i].setIcon(QIcon(self.photo_pix))
                self.saveEtatGroupeA[i] = 1
            elif 11 <= i < 24:
                self.tabGroupeB[i - 11].setIcon(QIcon(self.photo_pix))
                self.saveEtatGroupeB[i - 11] = 1
            elif 24 <= i < 37:
                self.tabGroupeC[i - 24].setIcon(QIcon(self.photo_pix))
                self.saveEtatGroupeC[i - 24] = 1
            elif 37 <= i < 50:
                self.tabGroupeD[i - 37].setIcon(QIcon(self.photo_pix))
                self.saveEtatGroupeD[i - 37] = 1
            elif 50 <= i <= 63:
                self.tabGroupeE[i - 50].setIcon(QIcon(self.photo_pix))
                self.saveEtatGroupeE[i - 50] = 1
            self.fichier.TransactionPass(i, cardloop)
        except Exception:
            self.PopUpErreurFichier()

    def _on_fail_auto(self, i, cardloop):
        try:
            if 0 <= i < 11:
                self.tabGroupeA[i].setIcon(QIcon(self.photo2_pix))
                self.saveEtatGroupeA[i] = 2
            elif 11 <= i < 24:
                self.tabGroupeB[i - 11].setIcon(QIcon(self.photo2_pix))
                self.saveEtatGroupeB[i - 11] = 2
            elif 24 <= i < 37:
                self.tabGroupeC[i - 24].setIcon(QIcon(self.photo2_pix))
                self.saveEtatGroupeC[i - 24] = 2
            elif 37 <= i < 50:
                self.tabGroupeD[i - 37].setIcon(QIcon(self.photo2_pix))
                self.saveEtatGroupeD[i - 37] = 2
            elif 50 <= i <= 63:
                self.tabGroupeE[i - 50].setIcon(QIcon(self.photo2_pix))
                self.saveEtatGroupeE[i - 50] = 2
            self.fichier.TransactionFail(i, cardloop)
        except Exception:
            self.PopUpErreurFichier()

    def _on_group_switch(self, i):
        try:
            if i == 10:
                self.SuppGA()
                self.GroupeB()
            elif i == 23:
                self.SuppGB()
                self.GroupeC()
            elif i == 36:
                self.SuppGC()
                self.GroupeD()
            elif i == 49:
                self.SuppGD()
                self.GroupeE()
        finally:
            self._group_switch_done.set()

    def _on_auto_finished(self):
        try:
            self.optMode.setEnabled(True)
            self.optCard.setEnabled(True)
            self.optGroupe.setEnabled(True)
            self.playBouton.show()
            self.deposerCarteBtn.hide()
        except Exception:
            pass

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

    def close_popup(self, T):
        T.close()

    def PopUpTransaction(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("")
        dialog.setFixedSize(300, 180)
        dialog.setStyleSheet("background:#1B3A6B;")
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
        bexit = QPushButton("   exit   ")
        bexit.setStyleSheet("QPushButton { background:#FFFFFF; color:#000000; padding:3px; border-radius:4px; }")
        btn_layout.addWidget(bpass)
        btn_layout.addWidget(bfail)
        layout.addLayout(btn_layout)
        layout.addWidget(bexit, alignment=Qt.AlignCenter)
        self._trans_dialog = dialog
        bpass.clicked.connect(lambda: self._do_pass_transaction(dialog, self.cardSelect))
        bfail.clicked.connect(lambda: self._do_fail_transaction(dialog, self.cardSelect))
        bexit.clicked.connect(lambda: self._intercepte_dialog(dialog))
        dialog.exec()

    def _do_pass_transaction(self, dialog,cardloop):
        dialog.accept()
        self.PassTransaction(cardloop)

    def _do_fail_transaction(self, dialog, cardloop):
        dialog.accept()
        self.FailTransaction(cardloop)

    def _intercepte_dialog(self, dialog):
        dialog.accept()
        self.Intercepte()

    def PassTransaction(self, cardloop):
        gc.collect()
        try:
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
            elif self.i >= 50 and self.i <= 63:
                self.tabGroupeE[self.i - 50].setIcon(QIcon(self.photo_pix))
                self.saveEtatGroupeE[self.i - 50] = 1
            self.fichier.TransactionPass(self.i,cardloop)
        except Exception:
            self.PopUpErreurFichier()

    def Pass_Transac_Auto(self, cardloop):
        gc.collect()
        try:
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
            elif self.i >= 50 and self.i <= 63:
                self.tabGroupeE[self.i - 50].setIcon(QIcon(self.photo_pix))
                self.saveEtatGroupeE[self.i - 50] = 1
            self.fichier.TransactionPass(self.i, cardloop)
        except Exception:
            self.PopUpErreurFichier()

    def FailTransaction(self, cardloop):
        gc.collect()
        try:
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
            elif self.i >= 50 and self.i <= 63:
                self.tabGroupeE[self.i - 50].setIcon(QIcon(self.photo2_pix))
                self.saveEtatGroupeE[self.i - 50] = 2
            self.fichier.TransactionFail(self.i, cardloop)
        except Exception:
            self.PopUpErreurFichier()

    def Fail_Transac_Auto(self, cardloop):
        gc.collect()
        try:
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
            elif self.i >= 50 and self.i <= 63:
                self.tabGroupeE[self.i - 50].setIcon(QIcon(self.photo2_pix))
                self.saveEtatGroupeE[self.i - 50] = 2
            self.fichier.TransactionFail(self.i, cardloop)
        except Exception:
            self.PopUpErreurFichier()

    def PopUpRecuperationCarte(self):
        confirmed = self._show_ok_cancel_dialog(
            "\n   Prendre la carte dans le socle? :  \n", w=400, h=130
        )
        self.choix = 0 if confirmed else 1
        return self.choix

    def ZoneAcceleration(self):
        FRAME = "QFrame { background:#1B3A6B; border:2px solid #AAAAAA; border-radius:6px; }"
        LBL   = "color:#DDDDDD; font-size:11px; font-weight:bold; background:#1B3A6B; border:none;"
        INP   = "color:#000000; font-size:14px; font-weight:bold; background:#FFFFFF; border-radius:4px;"
        BTN   = "QPushButton { color:#000000; background:#FFFF00; font-size:12px; font-weight:bold; padding:6px 10px; border-radius:5px; } QPushButton:hover { background:#FFE033; } QPushButton:pressed { background:#CCBB00; }"
        accel_frame = QFrame()
        accel_frame.setStyleSheet(FRAME)
        a_layout = QHBoxLayout(accel_frame)
        a_layout.setContentsMargins(8, 4, 8, 4)
        self.AccelValue = QLabel("Vitesse descente\n(m/s²) :")
        self.AccelValue.setStyleSheet(LBL)
        self.AccelEntree = QLineEdit()
        self.AccelEntree.setFixedWidth(45)
        self.AccelEntree.setText("8")
        self.AccelEntree.setStyleSheet(INP)
        self.boutonVitesse = QPushButton("OK")
        self.boutonVitesse.setStyleSheet(BTN)
        self.boutonVitesse.clicked.connect(self.Acceleration)
        a_layout.addWidget(self.AccelValue)
        a_layout.addWidget(self.AccelEntree)
        a_layout.addWidget(self.boutonVitesse)
        self._grid.addWidget(accel_frame, 14, 5, 1, 3, Qt.AlignVCenter)

    def ZoneTemporisation(self):
        FRAME = "QFrame { background:#1B3A6B; border:2px solid #AAAAAA; border-radius:6px; }"
        LBL   = "color:#DDDDDD; font-size:11px; font-weight:bold; background:#1B3A6B; border:none;"
        INP   = "color:#000000; font-size:14px; font-weight:bold; background:#FFFFFF; border-radius:4px;"
        BTN   = "QPushButton { color:#000000; background:#FFFF00; font-size:12px; font-weight:bold; padding:6px 10px; border-radius:5px; } QPushButton:hover { background:#FFE033; } QPushButton:pressed { background:#CCBB00; }"
        tempo_frame = QFrame()
        tempo_frame.setStyleSheet(FRAME)
        t_layout = QHBoxLayout(tempo_frame)
        t_layout.setContentsMargins(8, 4, 8, 4)
        self.TemporisationValue = QLabel("Temps dans\nle champ (s) :")
        self.TemporisationValue.setStyleSheet(LBL)
        self.TempoEntree = QLineEdit()
        self.TempoEntree.setFixedWidth(45)
        self.TempoEntree.setText("1")
        self.TempoEntree.setStyleSheet(INP)
        self.boutonTempo = QPushButton("OK")
        self.boutonTempo.setStyleSheet(BTN)
        self.boutonTempo.clicked.connect(self.Temporisation)
        t_layout.addWidget(self.TemporisationValue)
        t_layout.addWidget(self.TempoEntree)
        t_layout.addWidget(self.boutonTempo)
        self._grid.addWidget(tempo_frame, 14, 2, 1, 3, Qt.AlignVCenter)

    def RetourMenu(self):
        self.windowPlace = self.geometry()
        self.destroy()

        try:
            gc.collect()
            self._stopAutoFlag = True
            self.robotVariable.gripperrelease()
        except Exception as e:
            print(f"Erreur lors de l'arrêt des threads: {e}")
        self.enum = 0
        print(self.enum)

    def RetourBouton(self):
        self.retourBouton = QPushButton("RETOUR")
        self.retourBouton.setFixedSize(140, 55)
        self.retourBouton.setStyleSheet(
            "QPushButton { background:#CC0000; color:#FFFFFF; font-size:17px; font-weight:bold; border-radius:12px; }"
            "QPushButton:hover   { background:#E53333; }"
            "QPushButton:pressed { background:#AA0000; }"
        )
        self.retourBouton.clicked.connect(self.RetourMenu)
        self._grid.addWidget(self.retourBouton, 14, 0, 1, 2, Qt.AlignLeft | Qt.AlignVCenter)

    def PlayBouton(self):
        self.playBouton = QPushButton("RUN")
        self.playBouton.setFixedSize(140, 55)
        self.playBouton.setStyleSheet(
            "QPushButton { background:#00CC00; color:#000000; font-size:17px; font-weight:bold; border-radius:12px; }"
            "QPushButton:hover   { background:#33DD33; }"
            "QPushButton:pressed { background:#009900; }"
        )
        self.playBouton.clicked.connect(self.ModeAutomatique)
        self._grid.addWidget(self.playBouton, 14, 8, 1, 1, Qt.AlignRight | Qt.AlignVCenter)

    def Acceleration(self):
        self.CMDAcceleration = int(self.AccelEntree.text())
        if self.CMDAcceleration > 8:
            self.CMDAcceleration = 8
        print("valeur de l'accélération':" + self.AccelEntree.text() + " m/s²")

    def Temporisation(self):
        self.CMDTemporisation = int(self.TempoEntree.text())
        print("valeur de temporisation:" + self.TempoEntree.text() + " s")

    # --------------------------------------------------------
    # Group A buttons (positions 0-10)
    # --------------------------------------------------------
    def GroupeA(self):
        self.tabGroupeA.clear()
        self.gp = 0
        positions = [(6,4),(5,6),(2,4),(5,2),(7,2),(9,4),(7,6),(5,5),(5,3),(7,3),(7,5)]
        for idx, (row, col) in enumerate(positions):
            btn = self._make_status_btn(idx)
            self.tabGroupeA.append(btn)
            self._grid.addWidget(btn, row, col, Qt.AlignLeft | Qt.AlignTop)
        self._update_group_icons(self.tabGroupeA, self.saveEtatGroupeA)

    def GroupeB(self):
        self.tabGroupeB.clear()
        self.gp = 1
        positions = [(5,4),(4,6),(3,4),(4,2),(6,2),(7,4),(6,6),(5,7),(2,6),(2,2),(5,1),(8,2),(8,6)]
        for idx, (row, col) in enumerate(positions):
            btn = self._make_status_btn(11 + idx)
            self.tabGroupeB.append(btn)
            self._grid.addWidget(btn, row, col, Qt.AlignLeft | Qt.AlignTop)
        self._update_group_icons(self.tabGroupeB, self.saveEtatGroupeB)

    def GroupeC(self):
        self.tabGroupeC.clear()
        self.gp = 2
        positions = [(7,4),(7,6),(5,5),(5,3),(7,2),(9,3),(9,5),(5,7),(1,4),(5,1),(9,1),(12,4),(9,7)]
        for idx, (row, col) in enumerate(positions):
            btn = self._make_status_btn(24 + idx)
            self.tabGroupeC.append(btn)
            self._grid.addWidget(btn, row, col, Qt.AlignLeft | Qt.AlignTop)
        self._update_group_icons(self.tabGroupeC, self.saveEtatGroupeC)

    def GroupeD(self):
        self.tabGroupeD.clear()
        self.gp = 3
        positions = [(5,4),(4,6),(3,4),(4,2),(6,2),(7,4),(6,6),(5,7),(2,6),(2,2),(5,1),(8,2),(8,6)]
        for idx, (row, col) in enumerate(positions):
            btn = self._make_status_btn(37 + idx)
            self.tabGroupeD.append(btn)
            self._grid.addWidget(btn, row, col, Qt.AlignLeft | Qt.AlignTop)
        self._update_group_icons(self.tabGroupeD, self.saveEtatGroupeD)

    def GroupeE(self):
        self.tabGroupeE.clear()
        self.gp = 4
        positions = [(7,4),(7,6),(5,5),(5,3),(7,2),(9,3),(9,5),(5,7),(1,4),(5,1),(9,1),(12,4),(9,7)]
        for idx, (row, col) in enumerate(positions):
            btn = self._make_status_btn(50 + idx)
            self.tabGroupeE.append(btn)
            self._grid.addWidget(btn, row, col, Qt.AlignLeft | Qt.AlignTop)
        self._update_group_icons(self.tabGroupeE, self.saveEtatGroupeE)

    def SuppGA(self):
        for btn in self.tabGroupeA:
            btn.hide()

    def SuppGB(self):
        for btn in self.tabGroupeB:
            btn.hide()

    def SuppGC(self):
        for btn in self.tabGroupeC:
            btn.hide()

    def SuppGD(self):
        for btn in self.tabGroupeD:
            btn.hide()

    def SuppGE(self):
        for btn in self.tabGroupeE:
            btn.hide()

    def FunctionManuel(self, number):
        if self.manuelActive is True:
            try:
                self.robotVariable.RecupCoordonneeRobot()
                self.robotVariable.mode = 2
                self.i = number
                if self.robotVariable.variabletest == 2:
                    print(self.i)
                    self.robotVariable.Conversion(self.i)
                    self.robotVariable.PositionInitiale()
                    self.PopUpMontant()
                    print(self.robotVariable.xRobot, self.robotVariable.yRobot, self.robotVariable.zRobot)
                    self.robotVariable.MouvementRobotCarte(self.CMDAcceleration, self.CMDTemporisation)
                else:
                    self.robotVariable.Conversion(self.i)
                    self.PopUpMontant()
                    print(self.robotVariable.xRobot, self.robotVariable.yRobot, self.robotVariable.zRobot)

                self.PopUpTransaction()
            except Exception:
                self.PopUpErreurConnexion()
