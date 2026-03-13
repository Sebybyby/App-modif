# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 10:03:53 2021

@author: t0247275
"""

import urx
from datetime import datetime
import math 
import time
import csv

titre = "" 
groupe = ""
  #coeeff de X = -0.4831+0.4734 /7.5=-0.00129
  #coeff de Y = -0.07637+0.091128 / 12.99= 0.00126
coeffy = -0.00105624
coeffx = 0.0011356
coeffz = 0.001
positionTopZ = 0.3243651884282409
tab_Coordonnee = []


def creationFichier(ope, antenne2, nomProjet):
     global titre
     titre = nomProjet +".txt"
     print(titre)
     fichier = open(titre,"w")
     nom = "Le nom de l'opérateur est : " + ope
     fichierAntenne = "\nle nom de l'antenne est : " +  antenne2
     fichierProjet = "\nle nom du projet est : " + nomProjet 
     fichier.write (nom)
     fichier.write (fichierAntenne)
     fichier.write (fichierProjet)
     fichier.write ("\n")
class Robot:
    acceleration = 0.1
    vitesse = 1
    def _init_Position (self,x,y,z,rX,rY,rZ,coeffX,coeffY,coeffZ):
        self.x = x
        self.y = y 
        self.z = z
        self.rX = rX
        self.rY = rY
        self.rZ = rZ
        self.coeffX = coeffX
        self.coeffY = coeffY
        self.coeffZ = coeffZ
    def printPosition(self):
        print("x : ", self.x)
        print("y : ", self.y)
        print("z : ", self.z)
        print("rx : ", self.rX)
        print("ry : ", self.rY)
        print("rz : ", self.rZ)

def Menu():
  print("Bienvenue sur le Test combinatoire")
  print("")
  print("1--- Entrer vos informations")
  print("2--- Choisisser votre mode")     
 
def Transaction(fichier,i):
    today = datetime.now()
    ecriture = "\n"+ str(today) +" " +str(tab_Coordonnee[i][0]) +", coordonne z : "+ str(tab_Coordonnee[i][1]) + ", coordonnee r : "+ str(tab_Coordonnee[i][2])+ ", coordonnee phi : "+ str(tab_Coordonnee[i][3])+ " : "    
    fichier.write(ecriture)
    reponse = input("Pass ou Fail : ")
    if(reponse.lower() == "pass" or reponse.lower() == "p"):
        fichier.write("Pass")
    elif(reponse.lower() =="fail" or reponse.lower() == "f") :
        fichier.write("Fail") 
        
def Conversion(position, robot):
    #trouver le x cartesien
    global tab_Coordonnee
    yCart = float(tab_Coordonnee[position][2])*(math.cos(float(tab_Coordonnee[position][3])*math.pi/180))
    xCart = float(tab_Coordonnee[position][2])*(-1*(math.sin(float(tab_Coordonnee[position][3])*math.pi/180)))
    xRobot = yCart*robot.coeffX + robot.x
    yRobot = xCart*robot.coeffY + robot.y
    zRobot = int(tab_Coordonnee[position][1])*robot.coeffZ + robot.z
    return xRobot, yRobot,zRobot

def Montant():
    reponse = input("Tapez le montant : ")
    if(reponse ==" " or reponse ==""):
        etapesuivante = True
        print("true")
    else :
        etapesuivante = False  
    return etapesuivante   

def PrintGroupe():
     print("0 -- Stop")
     print("1 -- groupeA")
     print("2 -- groupeB")
     print("3 -- groupeC")
     print("4 -- groupeD")
     print("5 -- groupeE")

def GroupeAndPosition():
    groupe = input("Choisissez votre groupe : ")
    return groupe
def informationProjet():
   nomOperateur = input("Operateur : ")
   nomProjet = input("nom du projet : ")
   antenne  = input("Antenne : ") 
   return  nomOperateur, nomProjet, antenne

def MouvementRobot(rob, r,positionTopZ,xR,yR,zR ):
    rob.movel((xR, yR, positionTopZ, r.rX, r.rY, r.rZ),r.acceleration ,r.vitesse )
    rob.movel((xR, yR, zR, r.rX, r.rY, r.rZ),r.acceleration ,r.vitesse )
    time.sleep(1)
    rob.movel((xR, yR, positionTopZ, r.rX, r.rY, r.rZ),r.acceleration ,r.vitesse )  
    
def IpAdress():
    fichier = open("IpAdress.txt",'r')
    adress = fichier.readline()
    return adress

### MENU
Menu()
### INITIALISATION DU FICHIER FINAL DE TEST
nomOperateur, nomProjet, antenne  = informationProjet()
creationFichier(nomOperateur, antenne, nomProjet)
 
###recuperation fichier csv   
fichiercsv = csv.reader(open("coordonneeRobot.csv","r"))
for row in fichiercsv:
       tab_Coordonnee.append(row)
size = len(tab_Coordonnee)

###INITIALISATION DU ROBOT
adressIp = IpAdress()
rob = urx.Robot(str(adressIp))
rob.set_tcp((0, 0, 0.1, 0, 0, 0))
rob.set_payload(2, (0, 0, 0.1))
print("Connexion reussie") 
r = Robot()

#x =  [-0.47348364806439347, -0.09, 0.09523096713862443, 0.053361353510762606, -3.1395937679209625, 0.019738170228314263]
### RECUPERATION DE LA POSITION INITIALE 
print("Placer le robot au centre à 0 cm  ")
reponse = input("Position initiale  ok ? ")
if(reponse =="ok" or reponse==" " or reponse =="" ):
    x =  rob.getl()
    r._init_Position(x[0],x[1],x[2],x[3],x[4],x[5],coeffx,coeffy,coeffz)
    r.printPosition()
    menu= input("Mode manuel ou automatique : ")
    
    ## MODE AUTOMATIQUE
    if(menu.lower() == "a" or menu.lower() == "automatique"):
        rob.movel((r.x,r.y,positionTopZ, r.rX, r.rY, r.rZ),r.acceleration ,r.vitesse )
        for i in  range (0,size):
            if groupe != tab_Coordonnee[i][0]:
                print("-------" + tab_Coordonnee[i][0] + "-------")
            if Montant() == True:         
                fichier = open(titre,"a") 
                xR, yR, zR = Conversion(i, r)
                print(xR,yR,zR)
                MouvementRobot(rob, r,positionTopZ,xR,yR,zR )
                Transaction(fichier,i)
                fichier.close()
   ## MODE MANUEL   
    elif(menu.lower() == "manuel" or menu.lower() == "m"):
        rob.movel((r.x,r.y,positionTopZ, r.rX, r.rY, r.rZ),r.acceleration ,r.vitesse )
        while(1):
            PrintGroupe()
            groupe = GroupeAndPosition()
            if (groupe.lower() == "0"):
                    break
            else:
                position = input("Choisissez le point à tester : ")
                for gr in range (0,size):
                    if (groupe.lower() == "0"):
                        break
                    elif(groupe == tab_Coordonnee[gr][0] and position == tab_Coordonnee[gr][4]):
                        if Montant() == True:
                                fichier = open(titre,"a") 
                                xR, yR, zR = Conversion(gr, r)
                                print(xR,yR,zR)
                                MouvementRobot(rob, r,positionTopZ,xR,yR,zR )
                                Transaction(fichier,gr)
                                fichier.close()
                



