# -*- coding: utf-8 -*-
"""
Reader pour Soft Pos — 6 groupes (A/B/C à 0°, D/E/F à 90°), 3 hauteurs chacun.
  A = même grille que GroupeA Combinatoire (11 pts), Z=0 cm,   rot=0°
  B = même grille que GroupeB Combinatoire (13 pts), Z=0,5 cm, rot=0°
  C = même grille que GroupeC Combinatoire (13 pts), Z=1 cm,   rot=0°
  D = même grille que GroupeA Combinatoire (11 pts), Z=0 cm,   rot=90° droite
  E = même grille que GroupeB Combinatoire (13 pts), Z=0,5 cm, rot=90° droite
  F = même grille que GroupeC Combinatoire (13 pts), Z=1 cm,   rot=90° droite
Utilise RecupCoordonneeRobotSP() + ConversionSP() (coordonneeRobot_SP.csv).
Retourne au menu Soft Pos (enum=9).
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
from SP_LecteurDB import get_sp_lecteurs, get_sp_lecteur_position
import gc
import time
import threading
import json


COMBO_STYLE = (
    "QComboBox { background:#FFFFFF; color:#000000; font-size:12px;"
    " padding:6px 10px; border-radius:5px; border:2px solid #CCCCCC; min-width:110px; }"
    "QComboBox::drop-down { border:none; padding-right:4px; }"
    "QComboBox QAbstractItemView {"
    " background:#FFFFFF; color:#000000; border:2px solid #1B3A6B;"
    " selection-background-color:#1B3A6B; selection-color:#FFFFFF; }"
)

# ── Grilles de boutons (identiques aux groupes Combinatoire correspondants) ──
_POS_A = [                                                      # 11 positions
    (6,4),(5,6),(2,4),(5,2),(7,2),(9,4),(7,6),(5,5),(5,3),(7,3),(7,5)
]
_POS_B = [                                                      # 13 positions
    (5,4),(4,6),(3,4),(4,2),(6,2),(7,4),(6,6),(5,7),(2,6),(2,2),(5,1),(8,2),(8,6)
]
_POS_C = [                                                      # 13 positions
    (7,4),(7,6),(5,5),(5,3),(7,2),(9,3),(9,5),(5,7),(1,4),(5,1),(9,1),(12,4),(9,7)
]

# D/E/F reprennent exactement les mêmes grilles que A/B/C
_GRP_POS = {
    'A': _POS_A, 'B': _POS_B, 'C': _POS_C,
    'D': _POS_A, 'E': _POS_B, 'F': _POS_C,
}
_GRP_SIZE = {g: len(p) for g, p in _GRP_POS.items()}
# A=11, B=13, C=13, D=11, E=13, F=13  → total 74

# Offset de départ et dernier index de chaque groupe
_GRP_OFFSET = {}
_offset = 0
for _g in ('A', 'B', 'C', 'D', 'E', 'F'):
    _GRP_OFFSET[_g] = _offset
    _offset += _GRP_SIZE[_g]
# A:0  B:11  C:24  D:37  E:48  F:61

_GRP_LAST = {g: _GRP_OFFSET[g] + _GRP_SIZE[g] - 1 for g in _GRP_OFFSET}
# A:10  B:23  C:36  D:47  E:60  F:73

_TOTAL = _offset   # 74


class SP_Reader(FFT_signal, Interface):
    optionListMode    = ["Automatique", "Manuel"]
    optionListCard    = []
    optionPositionList = [
        "Groupe : A", "Groupe : B", "Groupe : C",
        "Groupe : D", "Groupe : E", "Groupe : F",
    ]

    _sig_pass_auto          = Signal(int, int)
    _sig_fail_auto          = Signal(int, int)
    _sig_card_text          = Signal(str)
    _sig_group_switch       = Signal(int)
    _sig_auto_error         = Signal()
    _sig_auto_finished      = Signal()
    _sig_gripper_done       = Signal()
    _sig_depose_manuel_done = Signal()

    def __init__(self):
        Interface.__init__(self)
        with open("cartes.json", "r") as f:
            data = json.load(f)
            self.optionListCard = data.get("cartes", [])
        print("monstre : " + str(self.optionListCard))
        self.texteOffset = "null"

        # Tableaux de boutons et états pour chaque groupe
        self.tabGroupeA = [];  self.saveEtatGroupeA = [0] * _GRP_SIZE['A']
        self.tabGroupeB = [];  self.saveEtatGroupeB = [0] * _GRP_SIZE['B']
        self.tabGroupeC = [];  self.saveEtatGroupeC = [0] * _GRP_SIZE['C']
        self.tabGroupeD = [];  self.saveEtatGroupeD = [0] * _GRP_SIZE['D']
        self.tabGroupeE = [];  self.saveEtatGroupeE = [0] * _GRP_SIZE['E']
        self.tabGroupeF = [];  self.saveEtatGroupeF = [0] * _GRP_SIZE['F']

        self.cardSelect = 0
        self.saveEtatByCard = []
        for _ in self.optionListCard:
            self.saveEtatByCard.append({
                g: [0] * _GRP_SIZE[g] for g in ('A', 'B', 'C', 'D', 'E', 'F')
            })

        # Pixmaps
        self.rond_pix = QPixmap(54, 54)
        self.rond_pix.fill(Qt.transparent)
        _p = QPainter(self.rond_pix)
        _p.setRenderHint(QPainter.Antialiasing)
        _p.setBrush(QBrush(QColor("#CCCCCC")))
        _p.setPen(Qt.NoPen)
        _p.drawEllipse(0, 0, 54, 54)
        _p.end()
        self.photo_pix  = QPixmap("./Image/rondVert.png")
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
        self._sig_gripper_done.connect(self._on_gripper_done)
        self._sig_depose_manuel_done.connect(self._on_depose_manuel_done)
        self._move_thread = None
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
        InterfaceAffiche(14)
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

    # ── Helpers internes ────────────────────────────────────────────────
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

    def _grp_of(self, i):
        """Retourne la lettre du groupe ('A'…'F') pour l'index global i."""
        for g in ('A', 'B', 'C', 'D', 'E', 'F'):
            if _GRP_OFFSET[g] <= i <= _GRP_LAST[g]:
                return g
        return None

    def _set_icon_at(self, i, pix):
        g = self._grp_of(i)
        if g is None:
            return
        tab  = getattr(self, f'tabGroupe{g}')
        idx  = i - _GRP_OFFSET[g]
        if 0 <= idx < len(tab):
            tab[idx].setIcon(QIcon(pix))

    def _save_etat_at(self, i, val):
        g = self._grp_of(i)
        if g is None:
            return
        save = getattr(self, f'saveEtatGroupe{g}')
        idx  = i - _GRP_OFFSET[g]
        if 0 <= idx < len(save):
            save[idx] = val

    # ── Apparition / sélection des groupes ──────────────────────────────
    def ApparitionGroupe(self):
        self._stopAutoFlag = False   # ← reset au passage en mode Manuel
        self._set_play_bouton_gripper()
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
            if   text == "Groupe : A": self.GroupeA()
            elif text == "Groupe : B": self.GroupeB()
            elif text == "Groupe : C": self.GroupeC()
            elif text == "Groupe : D": self.GroupeD()
            elif text == "Groupe : E": self.GroupeE()
            elif text == "Groupe : F": self.GroupeF()

        self.optGroupe.currentTextChanged.connect(AffichagePoint)

    def AfficheReader(self):
        """Dropdown lecteur → liste des téléphones Soft Pos (sp_lecteurs.xlsx)."""
        self.optLecteur = QComboBox()
        self.optLecteur.setStyleSheet(COMBO_STYLE)
        self.optLecteur.blockSignals(True)
        for name in get_sp_lecteurs():
            self.optLecteur.addItem(name)
        self.optLecteur.blockSignals(False)
        self._grid.addWidget(self.optLecteur, 1, 6, Qt.AlignRight | Qt.AlignTop)
        self.optLecteur.currentTextChanged.connect(self._on_reader_change)
        initial = self.optLecteur.currentText()
        if initial:
            self._on_reader_change(initial)

    def _on_reader_change(self, name):
        """Positionne le robot sur la position initiale du téléphone sélectionné."""
        pos = get_sp_lecteur_position(name)
        if pos is None:
            return
        # Position 0° (utilisée par groupes A, B, C)
        self.robotVariable._init_Position(
            pos["x"], pos["y"], pos["z"],
            pos["rX"], pos["rY"], pos["rZ"],
            self.robotVariable.coeffx,
            self.robotVariable.coeffy,
            self.robotVariable.coeffz,
        )
        self.robotVariable.position = [
            pos["x"], pos["y"], pos["z"],
            pos["rX"], pos["rY"], pos["rZ"],
        ]
        self.robotVariable.positionTopZ = pos["topZ"]
        # Position 90° — initialisée comme fallback sur la même base.
        # L'utilisateur doit calibrer via "Paramétrage Robot SP" pour
        # que les groupes D/E/F utilisent la vraie rotation 90°.
        if self.robotVariable.x2 == 0.0 and self.robotVariable.y2 == 0.0:
            self.robotVariable._init_Position2(
                pos["x"], pos["y"], pos["z"],
                pos["rX"], pos["rY"], pos["rZ"],
                self.robotVariable.coeffx,
                self.robotVariable.coeffy,
                self.robotVariable.coeffz,
            )
            self.robotVariable.position2 = [
                pos["x"], pos["y"], pos["z"],
                pos["rX"], pos["rY"], pos["rZ"],
            ]
        try:
            self.fichier.EcritureLecteur(name)
        except Exception:
            pass
        print(f"SP Lecteur: {name}, topZ={pos['topZ']}")

    def AffichageCard(self):
        self.optCard = QComboBox()
        self.optCard.setStyleSheet(COMBO_STYLE)
        for item in self.optionListCard:
            self.optCard.addItem(item)
        self._grid.addWidget(self.optCard, 1, 7, Qt.AlignRight | Qt.AlignTop)
        self.optCard.currentTextChanged.connect(self.on_card_change)

    def testGroupe(self):
        handlers = {
            0: self.SuppGA, 1: self.SuppGB, 2: self.SuppGC,
            3: self.SuppGD, 4: self.SuppGE, 5: self.SuppGF,
        }
        if self.gp in handlers:
            handlers[self.gp]()

    def on_card_change(self, *args):
        try:
            selected_card = self.optCard.currentText()
            card_index = self.optionListCard.index(selected_card)
            self.cardSelect = card_index
            for g in ('A', 'B', 'C', 'D', 'E', 'F'):
                setattr(self, f'saveEtatGroupe{g}',
                        self.saveEtatByCard[card_index][g])
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

        self.optGroupe = QComboBox()
        self.optGroupe.setStyleSheet(COMBO_STYLE)
        for item in self.optionPositionList:
            self.optGroupe.addItem(item)
        self._grid.addWidget(self.optGroupe, 1, 0, Qt.AlignLeft | Qt.AlignTop)
        self.optGroupe.hide()

        def Affichage(text):
            if text == "Automatique":
                self.PlayBouton()
                self.testGroupe()
                self.GroupeA()
                self.optGroupe.hide()
            elif text == "Manuel":
                self.manuelActive = True
                self.ApparitionGroupe()

        self.GroupeA()
        self.optMode.currentTextChanged.connect(Affichage)

    # ── Mode Manuel — GRIPPER / DÉPOSE ──────────────────────────────────
    def _set_play_bouton_gripper(self):
        try:
            self.optCard.setEnabled(True)
            self.optMode.setEnabled(True)
            self.optLecteur.setEnabled(True)
        except Exception:
            pass
        self.playBouton.setText("GRIPPER\nCARTE")
        self.playBouton.setStyleSheet(
            "QPushButton { background:#0088CC; color:#FFFFFF; font-size:13px;"
            " font-weight:bold; border-radius:12px; }"
            "QPushButton:hover   { background:#33AADD; }"
            "QPushButton:pressed { background:#0066AA; }"
        )
        try:
            self.playBouton.clicked.disconnect()
        except Exception:
            pass
        self.playBouton.clicked.connect(self._GripperCarteManuel)
        self.playBouton.setEnabled(True)
        self.playBouton.show()

    def _GripperCarteManuel(self):
        card_num = self.cardSelect + 1
        self.playBouton.setEnabled(False)
        def do_grip():
            try:
                self.robotVariable.RecuperationCarte(card_num)
            except Exception as e:
                print(f"Erreur gripper carte: {e}")
            self._sig_gripper_done.emit()
        threading.Thread(target=do_grip, daemon=True).start()

    def _on_gripper_done(self):
        self.optCard.setEnabled(False)
        self.optMode.setEnabled(False)
        self.optLecteur.setEnabled(False)
        self.playBouton.setText("DÉPOSE\nCARTE")
        self.playBouton.setStyleSheet(
            "QPushButton { background:#FF8800; color:#FFFFFF; font-size:13px;"
            " font-weight:bold; border-radius:12px; }"
            "QPushButton:hover   { background:#FFA033; }"
            "QPushButton:pressed { background:#CC6600; }"
        )
        try:
            self.playBouton.clicked.disconnect()
        except Exception:
            pass
        self.playBouton.clicked.connect(self._DeposerCarteManuel)
        self.playBouton.setEnabled(True)

    def _DeposerCarteManuel(self):
        card_num = self.cardSelect + 1
        self.playBouton.setEnabled(False)
        def do_depose():
            try:
                self.robotVariable.PoseCarte(card_num)
            except Exception as e:
                print(f"Erreur dépose carte manuel: {e}")
            self._sig_depose_manuel_done.emit()
        threading.Thread(target=do_depose, daemon=True).start()

    def _on_depose_manuel_done(self):
        self._set_play_bouton_gripper()

    # ── Bouton DÉPOSE CARTE (mode Automatique) ───────────────────────────
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
        self._stopAutoFlag = True
        card_idx = self.currentCardLoop
        move_thread = self._move_thread
        def do_pose():
            if move_thread and move_thread.is_alive():
                move_thread.join()
            try:
                self.robotVariable.PoseCarte(card_idx + 1)
            except Exception as e:
                print(f"Erreur dépose carte: {e}")
        threading.Thread(target=do_pose, daemon=True).start()

    # ── Mode Automatique ─────────────────────────────────────────────────
    def ModeAutomatique(self):
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
        self.robotVariable.RecupCoordonneeRobotSP()
        self.i = 0
        threading.Thread(target=self._ModeAutomatiqueWorker, daemon=True).start()

    def _ModeAutomatiqueWorker(self):
        """Thread de fond : test automatique Soft Pos (74 positions, 6 groupes)."""
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

                if not self.robotVariable.VerifierGripper():
                    print(f"Carte {cardloop} non grippée — arrêt automatique")
                    self._stopAutoFlag = True
                    self._sig_auto_error.emit()
                    break

                self._sig_card_text.emit(self.optionListCard[cardloop])
                print(f"\n DÉBUT Test de la carte {cardloop} \n")

                for self.i in range(0, self.robotVariable.size):
                    if self._stopAutoFlag:
                        break
                    try:
                        self.fichier.GroupeEcriture(self.i)
                        self.robotVariable.ConversionSP(self.i)

                        if self.robotVariable.variabletest == 2:
                            tic = time.perf_counter()
                            t1 = threading.Thread(
                                target=self.robotVariable.MouvementRobotCarte,
                                args=(self._stopAutoFlag, self.CMDAcceleration, self.CMDTemporisation)
                            )
                            t2 = threading.Thread(target=self.Record_son)
                            self._move_thread = t1
                            t1.start(); t2.start()
                            t1.join();  t2.join()
                            self._move_thread = None
                            toc = time.perf_counter()
                            print(f"time: {toc - tic:0.4f} seconds")

                        Trans = self.lecture_son()
                        print(Trans)
                        if Trans:
                            self._sig_pass_auto.emit(self.i, cardloop)
                        else:
                            self._sig_fail_auto.emit(self.i, cardloop)

                        # Changements de groupe A→B→C→D→E (F est le dernier)
                        if self.i in (_GRP_LAST['A'], _GRP_LAST['B'], _GRP_LAST['C'],
                                      _GRP_LAST['D'], _GRP_LAST['E']):
                            self._group_switch_done.clear()
                            self._sig_group_switch.emit(self.i)
                            self._group_switch_done.wait(timeout=5.0)
                        elif self.i == _GRP_LAST['F']:
                            print("END Carte")
                            break

                        time.sleep(3)

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

    # ── Handlers de signaux (thread principal) ───────────────────────────
    def _on_card_text(self, text):
        try:
            self.optCard.setCurrentText(text)
            QApplication.processEvents()
        except Exception:
            pass

    def _on_pass_auto(self, i, cardloop):
        try:
            self._set_icon_at(i, self.photo_pix)
            self._save_etat_at(i, 1)
            self.fichier.TransactionPass(i, cardloop)
        except Exception:
            self.PopUpErreurFichier()

    def _on_fail_auto(self, i, cardloop):
        try:
            self._set_icon_at(i, self.photo2_pix)
            self._save_etat_at(i, 2)
            self.fichier.TransactionFail(i, cardloop)
        except Exception:
            self.PopUpErreurFichier()

    def _on_group_switch(self, i):
        try:
            if   i == _GRP_LAST['A']: self.SuppGA(); self.GroupeB()
            elif i == _GRP_LAST['B']: self.SuppGB(); self.GroupeC()
            elif i == _GRP_LAST['C']: self.SuppGC(); self.GroupeD()
            elif i == _GRP_LAST['D']: self.SuppGD(); self.GroupeE()
            elif i == _GRP_LAST['E']: self.SuppGE(); self.GroupeF()
        finally:
            self._group_switch_done.set()

    def _on_auto_finished(self):
        self._stopAutoFlag = False   # ← reset après fin du test auto
        try:
            self.optMode.setEnabled(True)
            self.optCard.setEnabled(True)
            self.optGroupe.setEnabled(True)
            self.playBouton.show()
            self.deposerCarteBtn.hide()
        except Exception:
            pass

    # ── Pop-ups ──────────────────────────────────────────────────────────
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

    def _do_pass_transaction(self, dialog, cardloop):
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
            self._set_icon_at(self.i, self.photo_pix)
            self._save_etat_at(self.i, 1)
            self.fichier.TransactionPass(self.i, cardloop)
        except Exception:
            self.PopUpErreurFichier()

    def FailTransaction(self, cardloop):
        gc.collect()
        try:
            self._set_icon_at(self.i, self.photo2_pix)
            self._save_etat_at(self.i, 2)
            self.fichier.TransactionFail(self.i, cardloop)
        except Exception:
            self.PopUpErreurFichier()

    def PopUpRecuperationCarte(self):
        confirmed = self._show_ok_cancel_dialog(
            "\n   Prendre la carte dans le socle? :  \n", w=400, h=130
        )
        self.choix = 0 if confirmed else 1
        return self.choix

    # ── Accélération / Temporisation ─────────────────────────────────────
    def ZoneAcceleration(self):
        FRAME = "QFrame { background:#1B3A6B; border:2px solid #AAAAAA; border-radius:6px; }"
        LBL   = "color:#DDDDDD; font-size:11px; font-weight:bold; background:#1B3A6B; border:none;"
        INP   = "color:#000000; font-size:14px; font-weight:bold; background:#FFFFFF; border-radius:4px;"
        BTN   = ("QPushButton { color:#000000; background:#FFFF00; font-size:12px; font-weight:bold;"
                 " padding:6px 10px; border-radius:5px; }"
                 " QPushButton:hover { background:#FFE033; } QPushButton:pressed { background:#CCBB00; }")
        accel_frame = QFrame(); accel_frame.setStyleSheet(FRAME)
        a_layout = QHBoxLayout(accel_frame); a_layout.setContentsMargins(8, 4, 8, 4)
        self.AccelValue = QLabel("Vitesse descente\n(m/s²) :"); self.AccelValue.setStyleSheet(LBL)
        self.AccelEntree = QLineEdit(); self.AccelEntree.setFixedWidth(45)
        self.AccelEntree.setText("8"); self.AccelEntree.setStyleSheet(INP)
        self.boutonVitesse = QPushButton("OK"); self.boutonVitesse.setStyleSheet(BTN)
        self.boutonVitesse.clicked.connect(self.Acceleration)
        a_layout.addWidget(self.AccelValue); a_layout.addWidget(self.AccelEntree); a_layout.addWidget(self.boutonVitesse)
        self._grid.addWidget(accel_frame, 14, 5, 1, 3, Qt.AlignVCenter)

    def ZoneTemporisation(self):
        FRAME = "QFrame { background:#1B3A6B; border:2px solid #AAAAAA; border-radius:6px; }"
        LBL   = "color:#DDDDDD; font-size:11px; font-weight:bold; background:#1B3A6B; border:none;"
        INP   = "color:#000000; font-size:14px; font-weight:bold; background:#FFFFFF; border-radius:4px;"
        BTN   = ("QPushButton { color:#000000; background:#FFFF00; font-size:12px; font-weight:bold;"
                 " padding:6px 10px; border-radius:5px; }"
                 " QPushButton:hover { background:#FFE033; } QPushButton:pressed { background:#CCBB00; }")
        tempo_frame = QFrame(); tempo_frame.setStyleSheet(FRAME)
        t_layout = QHBoxLayout(tempo_frame); t_layout.setContentsMargins(8, 4, 8, 4)
        self.TemporisationValue = QLabel("Temps dans\nle champ (s) :"); self.TemporisationValue.setStyleSheet(LBL)
        self.TempoEntree = QLineEdit(); self.TempoEntree.setFixedWidth(45)
        self.TempoEntree.setText("1"); self.TempoEntree.setStyleSheet(INP)
        self.boutonTempo = QPushButton("OK"); self.boutonTempo.setStyleSheet(BTN)
        self.boutonTempo.clicked.connect(self.Temporisation)
        t_layout.addWidget(self.TemporisationValue); t_layout.addWidget(self.TempoEntree); t_layout.addWidget(self.boutonTempo)
        self._grid.addWidget(tempo_frame, 14, 2, 1, 3, Qt.AlignVCenter)

    def Acceleration(self):
        self.CMDAcceleration = int(self.AccelEntree.text())
        if self.CMDAcceleration > 8:
            self.CMDAcceleration = 8

    def Temporisation(self):
        self.CMDTemporisation = int(self.TempoEntree.text())

    # ── Boutons de navigation ─────────────────────────────────────────────
    def RetourMenu(self):
        self.windowPlace = self.geometry()
        self.destroy()
        try:
            gc.collect()
            self._stopAutoFlag = True
            self.robotVariable.gripperrelease()
        except Exception as e:
            print(f"Erreur lors de l'arrêt des threads: {e}")
        self.enum = 9

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

    # ── Affichage des groupes ─────────────────────────────────────────────
    def _make_groupe(self, grp_key, tab, save, gp_idx):
        tab.clear()
        self.gp = gp_idx
        for idx, (row, col) in enumerate(_GRP_POS[grp_key]):
            btn = self._make_status_btn(_GRP_OFFSET[grp_key] + idx)
            tab.append(btn)
            self._grid.addWidget(btn, row, col, Qt.AlignLeft | Qt.AlignTop)
        self._update_group_icons(tab, save)

    def GroupeA(self): self._make_groupe('A', self.tabGroupeA, self.saveEtatGroupeA, 0)
    def GroupeB(self): self._make_groupe('B', self.tabGroupeB, self.saveEtatGroupeB, 1)
    def GroupeC(self): self._make_groupe('C', self.tabGroupeC, self.saveEtatGroupeC, 2)
    def GroupeD(self): self._make_groupe('D', self.tabGroupeD, self.saveEtatGroupeD, 3)
    def GroupeE(self): self._make_groupe('E', self.tabGroupeE, self.saveEtatGroupeE, 4)
    def GroupeF(self): self._make_groupe('F', self.tabGroupeF, self.saveEtatGroupeF, 5)

    def SuppGA(self):
        for btn in self.tabGroupeA: btn.hide()

    def SuppGB(self):
        for btn in self.tabGroupeB: btn.hide()

    def SuppGC(self):
        for btn in self.tabGroupeC: btn.hide()

    def SuppGD(self):
        for btn in self.tabGroupeD: btn.hide()

    def SuppGE(self):
        for btn in self.tabGroupeE: btn.hide()

    def SuppGF(self):
        for btn in self.tabGroupeF: btn.hide()

    # ── Mode Manuel — clic sur un bouton ─────────────────────────────────
    def FunctionManuel(self, number):
        if self.manuelActive is True:
            try:
                self.robotVariable.RecupCoordonneeRobotSP()
                self.robotVariable.mode = 2
                self.i = number
                if self.robotVariable.variabletest == 2:
                    print(self.i)
                    self.robotVariable.ConversionSP(self.i)
                    self.robotVariable.PositionInitiale()
                    self.PopUpMontant()
                    print(self.robotVariable.xRobot, self.robotVariable.yRobot, self.robotVariable.zRobot)
                    self.robotVariable.MouvementRobotCarte(False, self.CMDAcceleration, self.CMDTemporisation)
                else:
                    self.robotVariable.ConversionSP(self.i)
                    self.PopUpMontant()
                    print(self.robotVariable.xRobot, self.robotVariable.yRobot, self.robotVariable.zRobot)

                self.PopUpTransaction()
            except Exception as e:
                print(f"Erreur en mode Manuel: {e}")
                self.PopUpErreurConnexion()
