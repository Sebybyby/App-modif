# -*- coding: utf-8 -*-
"""
Created on Wed May  5 14:16:04 2021
Converted from Tkinter to PySide6 (popup methods)
@author: t0247275
"""
import urx
import time
import csv
import math
import gc
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from Detection_Transaction import FFT_signal
from Gripper import EPick


class Robot(FFT_signal):

    instance = None

    def __init__(self):
        self.coeffy = -0.00105624
        self.coeffx = 0.0011356
        self.coeffz = 0.00
        self.positionTopZ = 0.5025886995214306
        self.positionTopZLane5000 = 0.399821937815115
        self.positionTopZmove5000 = 0.5025886995214306
        self.vitesse = 1
        self.acceleration = 8
        self.temporisation = 1
        self.accelerationslow = 0.2
        self.tab_Coordonnee = []
        self.variabletest = 2
        self.mode = 0
        self.Parametre()
        self.variableconnexion = 0

    def ConnexionRobot(self):
        try:
            if self.variabletest == 2:
                self.robot = urx.Robot(self.adressIp)
                self.robot.set_tcp((0, 0, 0, 0, 0, 0))
                self.robot.set_payload(0, (0, 0, 0.2))
                self.variableconnexion = 1
            else:
                print(self.adressIp)
            self.message = "\n   Connexion réussie   \n"
            self.PopUpConnexion(self.message)
            print("Connexion reussie")
        except Exception:
            self.message = "\n   Connexion interrompue ...   \n"
            self.PopUpConnexion(self.message)
            print("Connexion Failed")

    def _popup(self, title, message):
        BG = "#0054A4"
        dialog = QDialog()
        dialog.setWindowTitle(title)
        dialog.setFixedSize(400, 150)
        dialog.setStyleSheet(f"background:{BG};")
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        lbl = QLabel(message)
        lbl.setStyleSheet(
            "color:#FFFFFF; font-size:14px; font-weight:bold;"
            " background:transparent; border:none;"
        )
        lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl)
        btn = QPushButton("Ok")
        btn.setStyleSheet(
            "QPushButton { background:#FFFF00; color:#000000; font-size:13px;"
            " font-weight:bold; padding:6px 28px; border-radius:6px; }"
            "QPushButton:hover    { background:#FFE033; }"
            "QPushButton:pressed  { background:#CCBB00; }"
        )
        btn.clicked.connect(dialog.accept)
        layout.addWidget(btn, alignment=Qt.AlignCenter)
        dialog.exec()

    def PopUpConnexion(self, message):
        self._popup("Connexion", message)

    def PopUpPilotage(self):
        self._popup(
            "Erreur",
            "\n   Impossible de piloter le robot,\n   Vérifier la connexion...   \n"
        )

    def _init_Position(self, x, y, z, rX, rY, rZ, coeffX, coeffY, coeffZ):
        self.x = x
        self.y = y
        self.z = z
        self.rX = rX
        self.rY = rY
        self.rZ = rZ
        self.coeffX = coeffX
        self.coeffY = coeffY
        self.coeffZ = coeffZ

    def Parametre(self):
        try:
            tab_Coordonnee = []
            fichiercsv = csv.reader(open("./Parametres/Parameters.csv", "r"))
            for row in fichiercsv:
                tab_Coordonnee.append(row)
            self.adressIp = str(tab_Coordonnee[1][0])
            self.second = int(tab_Coordonnee[1][1])
            self.offsetX = float(tab_Coordonnee[1][2])
            self.offsetY = float(tab_Coordonnee[1][3])
            self.offsetZ = float(tab_Coordonnee[1][4])
            print(tab_Coordonnee[1][0])
            print(tab_Coordonnee[1][1])
            print(tab_Coordonnee[1][2])
            print(tab_Coordonnee[1][3])
            print(tab_Coordonnee[1][4])
        except IOError:
            print("cannot open the document")

    def printPosition(self):
        print("x : ", self.x)
        print("y : ", self.y)
        print("z : ", self.z)
        print("rx : ", self.rX)
        print("ry : ", self.rY)
        print("rz : ", self.rZ)

    def _init_Position2(self, x, y, z, rX, rY, rZ, coeffX, coeffY, coeffZ):
        self.x2 = x
        self.y2 = y
        self.z2 = z
        self.rX2 = rX
        self.rY2 = rY
        self.rZ2 = rZ
        self.coeffX2 = coeffX
        self.coeffY2 = coeffY
        self.coeffZ2 = coeffZ

    def Position0(self, i=None):
        """Position0() pour Combinatoire, Position0(1) et Position0(2) pour Soft Pos."""
        if i is None or i == 1:
            try:
                if self.variabletest == 2:
                    self.position = self.robot.getl()
                else:
                    self.position = [-0.47348364806439347, -0.09, 0.09523096713862443, 0.053361353510762606, -3.1395937679209625, 0.019738170228314263]
                self._init_Position(self.position[0], self.position[1], self.position[2],
                                    self.position[3], self.position[4], self.position[5],
                                    self.coeffx, self.coeffy, self.coeffz)
                self.printPosition()
                self.positionTopZ = self.z + 0.2
                print(str(self.positionTopZ))
            except Exception:
                self.PopUpPilotage()
        elif i == 2:
            try:
                if self.variabletest == 2:
                    self.position2 = self.robot.getl()
                else:
                    self.position2 = [-0.5, -0.7, 0.09523096713862443, 0.053361353510762606, -3.1395937679209625, 0.019738170228314263]
                self._init_Position2(self.position2[0], self.position2[1], self.position2[2],
                                     self.position2[3], self.position2[4], self.position2[5],
                                     self.coeffx, self.coeffy, self.coeffz)
                self.printPosition()
                self.positionTopZ = self.z2 + 0.2
                print(str(self.positionTopZ))
            except Exception:
                self.PopUpPilotage()

    # ------------------------------------------------------------------
    # Soft Pos device-specific positions
    # ------------------------------------------------------------------
    def Position0_IphoneSE(self):
        try:
            self.position = [-0.4535050711611319, 0.09746050997975206, 0.1628971910211756, -2.231798624387687, 2.2085533882615613, 0.012635744971039179]
            self._init_Position(self.position[0], self.position[1], self.position[2],
                                self.position[3], self.position[4], self.position[5],
                                self.coeffx, self.coeffy, self.coeffz)
            self.printPosition()
            self.positionTopZ = self.positionTopZLane5000
            self.position2 = [-0.45408824567380146, 0.09656793975421983, 0.16323226305320296, -3.136105813603413, 0.0059658915165634605, 0.005768539699730032]
            self._init_Position2(self.position2[0], self.position2[1], self.position2[2],
                                 self.position2[3], self.position2[4], self.position2[5],
                                 self.coeffx, self.coeffy, self.coeffz)
        except Exception:
            self.PopUpPilotage()

    def Position0_Iphone13(self):
        try:
            self.position = [-0.4530451975084202, 0.09109465497697321, 0.1623321775801928, -2.231812791929215, 2.20836277121875, 0.012548477860910717]
            self._init_Position(self.position[0], self.position[1], self.position[2],
                                self.position[3], self.position[4], self.position[5],
                                self.coeffx, self.coeffy, self.coeffz)
            self.printPosition()
            self.positionTopZ = self.positionTopZLane5000
            self.position2 = [-0.4538908590863759, 0.09090008082226783, 0.16183671129054125, -3.1363434639231946, 0.006183962859561696, 0.005655463797290936]
            self._init_Position2(self.position2[0], self.position2[1], self.position2[2],
                                 self.position2[3], self.position2[4], self.position2[5],
                                 self.coeffx, self.coeffy, self.coeffz)
        except Exception:
            self.PopUpPilotage()

    def Position0_SMGA34(self):
        try:
            self.position = [-0.43754267515397605, 0.05571605275012892, 0.16325538725581454, -2.2287899201722428, 2.211582666496985, 0.012739503012607888]
            self._init_Position(self.position[0], self.position[1], self.position[2],
                                self.position[3], self.position[4], self.position[5],
                                self.coeffx, self.coeffy, self.coeffz)
            self.printPosition()
            self.positionTopZ = self.positionTopZLane5000
            self.position2 = [-0.43779197300937156, 0.05566809081256038, 0.16167988293558122, 3.1329901684251853, 0.0028653314360108876, -0.012570467835896559]
            self._init_Position2(self.position2[0], self.position2[1], self.position2[2],
                                 self.position2[3], self.position2[4], self.position2[5],
                                 self.coeffx, self.coeffy, self.coeffz)
        except Exception:
            self.PopUpPilotage()

    def Position0_SMGS23(self):
        try:
            self.position = [-0.44212966228298567, 0.0018719860483787305, 0.16401135259168176, -2.2120128473028395, 2.2282316325468523, 0.012707245680119298]
            self._init_Position(self.position[0], self.position[1], self.position[2],
                                self.position[3], self.position[4], self.position[5],
                                self.coeffx, self.coeffy, self.coeffz)
            self.printPosition()
            self.positionTopZ = self.positionTopZLane5000
            self.position2 = [-0.44176411513420955, 0.0022479175451404973, 0.16358788873429445, -3.135959481027172, 0.045686366661383225, 0.005780244466567337]
            self._init_Position2(self.position2[0], self.position2[1], self.position2[2],
                                 self.position2[3], self.position2[4], self.position2[5],
                                 self.coeffx, self.coeffy, self.coeffz)
        except Exception:
            self.PopUpPilotage()

    def Position0_SMGA15(self):
        try:
            self.position = [-0.4386549445573203, 0.0774494613480611, 0.16674799989871197, -2.2162006686819176, 2.22500596381785, 0.016132300618970388]
            self._init_Position(self.position[0], self.position[1], self.position[2],
                                self.position[3], self.position[4], self.position[5],
                                self.coeffx, self.coeffy, self.coeffz)
            self.printPosition()
            self.positionTopZ = self.positionTopZLane5000
            self.position2 = [-0.4386549445573203, 0.0774494613480611, 0.16674799989871197, -3.138866554360482, 0.008480000512478247, 0.005342468975323949]
            self._init_Position2(self.position2[0], self.position2[1], self.position2[2],
                                 self.position2[3], self.position2[4], self.position2[5],
                                 self.coeffx, self.coeffy, self.coeffz)
        except Exception:
            self.PopUpPilotage()

    def Position0_Redmi13C(self):
        try:
            self.position = [-0.4342770051859024, 0.07549404718371988, 0.1650135223170027, 2.2089024541654294, -2.2273135015530854, 0.0029808527696273787]
            self._init_Position(self.position[0], self.position[1], self.position[2],
                                self.position[3], self.position[4], self.position[5],
                                self.coeffx, self.coeffy, self.coeffz)
            self.printPosition()
            self.positionTopZ = self.positionTopZLane5000
            self.position2 = [-0.436409377609138, 0.07550437596445046, 0.16412244591054673, -3.133896533207, 0.014809890234206468, -0.022259412887109645]
            self._init_Position2(self.position2[0], self.position2[1], self.position2[2],
                                 self.position2[3], self.position2[4], self.position2[5],
                                 self.coeffx, self.coeffy, self.coeffz)
        except Exception:
            self.PopUpPilotage()

    def Position0_Lane5000(self):
        try:
            self.position = [-0.4547756256699072, 0.09449841328596138, 0.21046844075096408, -2.2162304932532844, 2.2250713469998527, 0.01629001438342314]
            self._init_Position(self.position[0], self.position[1], self.position[2],
                                self.position[3], self.position[4], self.position[5],
                                self.coeffx, self.coeffy, self.coeffz)
            self.printPosition()
            self.positionTopZ = self.positionTopZLane5000
        except Exception:
            self.PopUpPilotage()

    def Position0_Move5000(self):
        try:
            self.position = [-0.4540141593144729, 0.031580682143320125, 0.30871004420187936, -2.2037218160115697, 2.2372876043326744, 0.01616534026994103]
            self._init_Position(self.position[0], self.position[1], self.position[2],
                                self.position[3], self.position[4], self.position[5],
                                self.coeffx, self.coeffy, self.coeffz)
            self.printPosition()
            self.positionTopZ = self.positionTopZmove5000
        except Exception:
            self.PopUpPilotage()

    def RecupCoordonneeRobot(self):
        self.tab_Coordonnee = []  # reset to prevent accumulation across calls
        fichiercsv = csv.reader(open("./Parametres/coordonneeRobot.csv", "r"))
        for row in fichiercsv:
            self.tab_Coordonnee.append(row)
        self.size = len(self.tab_Coordonnee)

    def Position02(self):
        try:
            if self.variabletest == 2:
                self.position2 = self.robot.getl()
            else:
                self.position2 = [-0.5, -0.7, 0.09523096713862443, 0.053361353510762606, -3.1395937679209625, 0.019738170228314263]
        except Exception:
            self.PopUpPilotage()

    def Conversion(self, position):
        yCart = float(self.tab_Coordonnee[position][2]) * (math.cos(float(self.tab_Coordonnee[position][3]) * math.pi / 180))
        xCart = float(self.tab_Coordonnee[position][2]) * (-1 * (math.sin(float(self.tab_Coordonnee[position][3]) * math.pi / 180)))
        self.xRobot = 0.001 * yCart + self.x + self.offsetX
        self.yRobot = -0.001 * xCart + self.y + self.offsetY
        if int(self.tab_Coordonnee[position][1]) == 0:
            self.zRobot = int(self.tab_Coordonnee[position][1]) * 0.001 + self.z + self.offsetZ
        else:
            self.zRobot = int(self.tab_Coordonnee[position][1]) * 0.001 + self.z - 0.0002 + self.offsetZ

    def MouvementRobotCarte(self, stop_flag, acceleration, temporisation):
        try:
            if stop_flag == True:
                print("Mouvement robot interrompu."+ str(stop_flag))
                return
            else : 
                self.robot.movel((self.xRobot, self.yRobot, self.positionTopZ, self.rX, self.rY, self.rZ), 0.2, 0.7)
                time.sleep(1)
                self.robot.movel((self.xRobot, self.yRobot, self.zRobot, self.rX, self.rY, self.rZ), acceleration, self.vitesse)
                time.sleep(temporisation)
                self.robot.movel((self.xRobot, self.yRobot, self.positionTopZ, self.rX, self.rY, self.rZ), acceleration, self.vitesse)
        except Exception:
            self.PopUpPilotage()

    def MouvementRobotMontant(self):
        vitesse2 = 0.5
        if self.position[1] == 0.09449841328596138:
            time.sleep(1)
            self.robot.movel((-0.4315791275634944, -0.16133090844476536, 0.41380485683636675, -2.2162354236801853, 2.2250625819872774, 0.01628214370241088), 0.2, vitesse2)
            self.robot.movel((-0.4315791275634944, -0.16133090844476536, 0.222137207059000698, -2.2162354236801853, 2.2250625819872774, 0.01628214370241088), self.accelerationslow, vitesse2)
            self.robot.movel((-0.4315791275634944, -0.16133090844476536, 0.23262444765244614, -2.2162354236801853, 2.2250625819872774, 0.01628214370241088), self.accelerationslow, vitesse2)
            self.robot.movel((-0.4315785138212975, -0.1869261331144906, 0.23262444765244614, -2.216029543324794, 2.2250841429943393, 0.016298191448406028), self.accelerationslow, vitesse2)
            self.robot.movel((-0.4315785138212975, -0.1869261331144906, 0.22123720705900069, -2.216029543324794, 2.2250841429943393, 0.016298191448406028), self.accelerationslow, vitesse2)
            self.robot.movel((-0.4315785138212975, -0.1869261331144906, 0.41380485683636675, -2.216029543324794, 2.2250841429943393, 0.016298191448406028), 0.2, vitesse2)
        else:
            self.robot.movel((-0.4532214332501294, -0.20112162034351463, 0.5025886995214306, -2.2037616705480647, 2.2372602832282618, 0.0161330441706863), self.accelerationslow, vitesse2)
            time.sleep(1)
            self.robot.movel((-0.4485990847923728, -0.2635451641705367, 0.18102813663304132, -2.0576661442063964, 2.0492912513854242, 0.33926291075538806), self.accelerationslow, vitesse2)
            self.robot.movel((-0.448617058333297, -0.2561425024492807, 0.181028609424272, -2.0575849523618777, 2.0494075106899214, 0.3392445457381048), self.accelerationslow, vitesse2)
            self.robot.movel((-0.4485990847923728, -0.2635451641705367, 0.18102813663304132, -2.0576661442063964, 2.0492912513854242, 0.33926291075538806), self.accelerationslow, vitesse2)
            self.robot.movel((-0.4323441181576404, -0.2696716900524826, 0.17160591520964105, -2.0578656793530192, 2.049239251717908, 0.3393001802963028), self.accelerationslow, vitesse2)
            self.robot.movel((-0.43237106061908415, -0.2628730063282291, 0.17160744467289216, -2.0577920851826694, 2.0493297109211017, 0.3392942723486183), self.accelerationslow, vitesse2)
            self.robot.movel((-0.4342965889859803, -0.20744303481551365, 0.5025886995214306, -2.2036678015491087, 2.237216151562037, 0.016140534468574996), self.accelerationslow, vitesse2)

    def PositionInitiale(self):
        self.robot.movel((self.xRobot, self.yRobot, self.positionTopZ, self.rX, self.rY, self.rZ), self.accelerationslow, self.vitesse)
    def RecuperationCarte1(self):
        print("je récupère la carte 1")
        self.robot.movel((-0.5746890201638996, -0.2878173389286983,self.positionTopZ , -2.216029543324794,2.2250841429943393,0.016298191448406028),self.accelerationslow ,self.vitesse )
        self.robot.movel((-0.5746890201638996, -0.2878173389286983, 0.14929612204562506, -2.216029543324794,2.2250841429943393,0.016298191448406028),self.accelerationslow ,self.vitesse )
        gripper = EPick(port="COM3")
        time.sleep(2)
        gripper.grip()
        time.sleep(1)
        gripper.close()

    def RecuperationCarte2(self):
        print("je récupère la carte 2")
        self.robot.movel((-0.46283148174191185, -0.289002778324476,self.positionTopZ , -2.216029543324794,2.2250841429943393,0.016298191448406028),self.accelerationslow ,self.vitesse )
        self.robot.movel((-0.46283148174191185, -0.289002778324476, 0.14648870998357674, -2.216029543324794,2.2250841429943393,0.016298191448406028),self.accelerationslow ,self.vitesse )
        gripper = EPick(port="COM3")
        time.sleep(2)
        gripper.grip()
        time.sleep(1)
        gripper.close()

    def RecuperationCarte3(self):
        print("je récupère la carte 3")
        self.robot.movel((-0.35150736034982666, -0.289002778324476,self.positionTopZ , -2.216029543324794,2.2250841429943393,0.016298191448406028),self.accelerationslow ,self.vitesse )
        self.robot.movel((-0.35150736034982666, -0.289002778324476, 0.14648870998357674, -2.216029543324794,2.2250841429943393,0.016298191448406028),self.accelerationslow ,self.vitesse )
        gripper = EPick(port="COM3")
        time.sleep(2)
        gripper.grip()
        time.sleep(1)
        gripper.close()
    def RecuperationCarte(self, numCarte):
        if numCarte == 1:
            self.RecuperationCarte1()
        elif numCarte == 2:
            self.RecuperationCarte2()
        elif numCarte == 3:
            self.RecuperationCarte3()        

    def PoseCarte1(self):
        print("je pose la carte 1")
        if self.variabletest == 2:

            self.robot.movel((-0.5746890201638996,-0.2878173389286983,self.positionTopZ , -2.216029543324794,2.2250841429943393,0.016298191448406028),self.accelerationslow ,self.vitesse )
            self.robot.movel((-0.5746890201638996, -0.2878173389286983, 0.14929612204562506, -2.216029543324794,2.2250841429943393,0.016298191448406028),self.accelerationslow ,self.vitesse )
            time.sleep(2)
            gripper = EPick(port="COM3")
            gripper.release()
            time.sleep(1)
            gripper.close()
        self.robot.movel((-0.5746890201638996,-0.2878173389286983,self.positionTopZ , -2.216029543324794,2.2250841429943393,0.016298191448406028),self.accelerationslow ,self.vitesse )

    def PoseCarte2(self):
        print("je pose la carte 2")

        self.robot.movel((-0.46283148174191185, -0.289002778324476,self.positionTopZ , -2.216029543324794,2.2250841429943393,0.016298191448406028),self.accelerationslow ,self.vitesse )
        self.robot.movel((-0.46283148174191185, -0.289002778324476, 0.14648870998357674, -2.216029543324794,2.2250841429943393,0.016298191448406028),self.accelerationslow ,self.vitesse )
        time.sleep(2)
        gripper = EPick(port="COM3")
        gripper.release()
        time.sleep(1)
        gripper.close()
        self.robot.movel((-0.46283148174191185, -0.289002778324476,self.positionTopZ , -2.216029543324794,2.2250841429943393,0.016298191448406028),self.accelerationslow ,self.vitesse )

    def PoseCarte3(self):
        print("je pose la carte 3")
        
        self.robot.movel((-0.35150736034982666, -0.289002778324476,self.positionTopZ , -2.216029543324794,2.2250841429943393,0.016298191448406028),self.accelerationslow ,self.vitesse )
        self.robot.movel((-0.35150736034982666, -0.289002778324476, 0.14648870998357674, -2.216029543324794,2.2250841429943393,0.016298191448406028),self.accelerationslow ,self.vitesse )
        time.sleep(2)
        gripper = EPick(port="COM3")
        gripper.release()
        time.sleep(1)
        gripper.close()
        self.robot.movel((-0.35150736034982666, -0.289002778324476,self.positionTopZ , -2.216029543324794,2.2250841429943393,0.016298191448406028),self.accelerationslow ,self.vitesse )
    def PoseCarte(self, numCarte):
        if numCarte == 1:
            self.PoseCarte1()
        elif numCarte == 2:
            self.PoseCarte2()
        elif numCarte == 3:
            self.PoseCarte3()
            
    def grippergrip(self):
        gripper = EPick("COM3")
        gripper.grip()
        time.sleep(1)
        gripper.close()
    
    def gripperrelease(self):
        gripper = EPick("COM3")
        gripper.release()
        time.sleep(1)
        gripper.close()

    def Close (self):
        self.gripperrelease()

        self.robot.close()
    @staticmethod
    def Instance():
        if Robot.instance is None:
            Robot.instance = Robot()
        return Robot.instance
