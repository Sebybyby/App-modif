# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 09:43:44 2021

@author: t0247275
"""

from InterfaceClass import Interface
import tkinter as tk 
from InterfaceAfficheClass import InterfaceAffiche
from RobotClass import Robot
import tkinter.messagebox
from FichierClass import Fichier
from Detection_Transaction import FFT_signal
import gc
#from reader import feed
import time
import threading



class Reader(FFT_signal,Interface):
    #Creation liste option du mode et le choix du groupe
     optionListMode = ["Automatique","Manuel"]
     optionListCard = ["Card1","Card2","Card3"]
     optionPositionList = ["Groupe : A","Groupe : B","Groupe : C","Groupe : D","Groupe : E"]
     def __init__(self):
        Interface.__init__(self)
        #texte offset
        self.texteOffset = "null"
        #creation des liste de bouton et de sauvegarde d'etat
        self.tabGroupeA=[]
        self.saveEtatGroupeA=[]
        self.tabGroupeB=[]
        self.saveEtatGroupeB=[]
        self.tabGroupeD=[]
        self.saveEtatGroupeD=[]
        self.tabGroupeC=[]
        self.saveEtatGroupeC=[]
        self.tabGroupeE=[]
        self.saveEtatGroupeE=[]
        for i in range(0,12):
            self.saveEtatGroupeA.append(0)
        for i in range(0,13):
            self.saveEtatGroupeB.append(0)
            self.saveEtatGroupeC.append(0)
            self.saveEtatGroupeD.append(0)
            self.saveEtatGroupeE.append(0)
         
         #Ouverture des images des ronds    
        self.rond = tk.PhotoImage(file = "./Image/rondNoir.png")
        self.photo = tk.PhotoImage(file = "./Image/rondVert.png")
        self.photo2 = tk.PhotoImage(file = "./Image/rondRouge.png")
        #self.carte2 = tk.PhotoImage(file = "./Image/carte.png")
        #self.carte = tk.PhotoImage(file = "./Image/carteBleu.png")
        
        self.robotVariable = Robot.Instance()
        self.fichier = Fichier.Instance()
        self.PlayBouton()
        self.AffichageMode()
        self.textGroupe = tk.StringVar(self)
        self.optGroupe = tk.OptionMenu(self,self.textGroupe, *self.optionPositionList)
        self.optCart = tk.OptionMenu(self,self.textGroupe, *self.optionListCard)
        self.RetourBouton()
        #self.BoutonVitesse()
        self.ZoneAcceleration()
        self.ZoneTemporisation()
        #self.BoutonCarte()
        self.CMDAccélération=8
        self.CMDTemporisation=1
        self.windowPlace =[]
        InterfaceAffiche(3) 
        self.test2=0
        self.gp = 0
        self.i =0
        self.manuelActive = False
        #Creation de la grid de configuration
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure((1,2,3,4,5,6,7,8,9,10,11,12,13),weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure((1,2,3,4,5,6), weight=2)
        self.OffsetIHM()
        
     def OffsetIHM(self):

         if (self.robotVariable.offsetX != 0 and self.robotVariable.offsetY == 0 and self.robotVariable.offsetZ == 0): 
             self.texteOffset = "Attention l'offset X est de : " + str(self.robotVariable.offsetX)
             
         if (self.robotVariable.offsetX == 0 and self.robotVariable.offsetY != 0 and self.robotVariable.offsetZ == 0): 
             self.texteOffset = "Attention l'offset Y est de : " + str(self.robotVariable.offsetY)
         
         if (self.robotVariable.offsetX == 0 and self.robotVariable.offsetY == 0 and self.robotVariable.offsetZ != 0): 
             self.texteOffset = "Attention l'offset Z est de : " + str(self.robotVariable.offsetZ)         
        
         if (self.robotVariable.offsetX != 0 and self.robotVariable.offsetY != 0 and self.robotVariable.offsetZ == 0):
             self.texteOffset = "Attention l'offset X est de  : " + str(self.robotVariable.offsetX) + "\n" + "Attention l'offset Y est de : " + str(self.robotVariable.offsetY)   

         if (self.robotVariable.offsetX != 0 and self.robotVariable.offsetY == 0 and self.robotVariable.offsetZ != 0):
             self.texteOffset = "Attention l'offset X est de  : " + str(self.robotVariable.offsetX) + "\n" + "Attention l'offset Z est de : " + str(self.robotVariable.offsetZ)
             
         if (self.robotVariable.offsetX == 0 and self.robotVariable.offsetY != 0 and self.robotVariable.offsetZ != 0):
             self.texteOffset = "Attention l'offset Y est de  : " + str(self.robotVariable.offsetY) + "\n" + "Attention l'offset Z est de : " + str(self.robotVariable.offsetZ)

         if (self.robotVariable.offsetX != 0 and self.robotVariable.offsetY != 0 and self.robotVariable.offsetZ != 0):
             self.texteOffset = "Attention l'offset X est de  : " + str(self.robotVariable.offsetX) + "\n" + "Attention l'offset Y est de : " + str(self.robotVariable.offsetY) + "\n" + "Attention l'offset Z est de : " + str(self.robotVariable.offsetZ)   

         if (self.texteOffset != "null") :
             self.labelOffset = tk.Label(self, text = self.texteOffset, bg = "red",anchor = "center", 
                                             font =("Helvetica", 10))
             self.labelOffset.grid(row = 14, column = 8)
             
             self.attentionPhoto= tk.PhotoImage(file = "./Image/attention.png")
             self.photolabel = tk.Label(self,  image = self.attentionPhoto,borderwidth  = 0,
                     highlightthickness = 0,
                     anchor = "center", relief="flat",
                     bg ='#49A',
                     activebackground ='#49A')
             self.photolabel.grid(row = 14, column = 7)
         
     def ApparitionGroupe(self):
         self.playBouton.grid_forget()
         self.textGroupe.set(self.optionPositionList[0])
         self.optGroupe.config(width=10, font=('Helvetica', 12),anchor = "center",
               bg='#49A',pady = 13, relief = "flat",
               borderwidth=0,activebackground = "#FFFC6B")
         self.optGroupe.grid(row=1,column=0,sticky="NW",padx = 5)
         self.testGroupe()
         self.GroupeA()
         try : 
                  self.fichier.Manuel()
         except : 
                  self.PopUpErreurFichier()         
         def AffichagePoint(*args):
              self.testGroupe()   
              if(self.textGroupe.get() == "Groupe : A"): 
                  self.GroupeA()
              elif(self.textGroupe.get() == "Groupe : C"):
                  self.GroupeC()
              elif (self.textGroupe.get() == "Groupe : D"):
                  self.GroupeD()
              elif (self.textGroupe.get() == "Groupe : E"):
                  self.GroupeE()
              elif (self.textGroupe.get() == "Groupe : B"): 
                  self.GroupeB()
           
         self.textGroupe.trace("w",AffichagePoint)     
         
     def testGroupe(self):
        if (self.gp == 0):
            self.SuppGA()
        elif(self.gp == 1):
            self.SuppGB()
        elif(self.gp == 2):
            self.SuppGC()
        elif(self.gp == 3):
            self.SuppGD()
        elif(self.gp == 4):
            self.SuppGE()    
         
             
     def AffichageMode(self):        
         self.variableMode = tk.StringVar(self)
         self.variableMode.set(self.optionListMode[0])
         self.optMode = tk.OptionMenu(self,self.variableMode, *self.optionListMode)
         self.optMode.config(width=10, font=('Helvetica', 12),anchor = "center",bg='#49A',pady = 13, relief = "flat",
                             borderwidth=0,activebackground ="#FFFC6B" )
         self.optMode.grid(row=1,column=8,sticky="NE")  
         
         def Affichage(*args):
            if(self.variableMode.get() == "Automatique"):
                print("auto")
                self.PlayBouton()
                self.testGroupe()   
                self.GroupeA()
                self.optGroupe.grid_forget() 
            elif (self.variableMode.get() == "Manuel"):
                print("manuel")  
                self.manuelActive = True
                self.ApparitionGroupe()
         self.GroupeA()
         self.variableMode.trace("w",Affichage)
         
     def ModeAutomatique(self):
        self.testGroupe()
        self.GroupeA()
        self.robotVariable.mode = 1
        #self.recupere= self.PopUpRecuperationCarte()
        #if self.recupere==0:
        #    self.robotVariable.RecuperationCarte()
        self.robotVariable.RecupCoordonneeRobot()
        self.i =0
        cardloop = 0
        while(cardloop<3) :
            cardloop +=1
            print("loop"+str(cardloop))
            for self.i in  range (0,self.robotVariable.size):
                try:
                    self.robotVariable.Conversion(self.i)
                    if self.robotVariable.variabletest == 2 :
                        self.robotVariable.PositionInitiale()
                    
                    # self.PopUpMontant()
                    
                    
                    if self.test2 == 1:
                        break
                    else :
                        self.fichier.GroupeEcriture(self.i)
                        print(self.robotVariable.xRobot,self.robotVariable.yRobot,self.robotVariable.zRobot)
                        if self.robotVariable.variabletest == 2 :
                            tic = time.perf_counter()
                            self.robotVariable.MouvementRobotMontant()#Déplacement robot pour qu'il appuie sur 9 (ReaderX)
                            time.sleep(1)#temps d'attente mis dans le patch afin de calmer le robot pour éviter qu'il bug, a enlever quand il sera réparé
                            
                            # self.robotVariable.MouvementRobotCarte(self.CMDAccélération,self.CMDTemporisation)#Robot revient au dessus de la zone sans contact et descend
                            running = threading.Event()
                            running.set()
                            thread1 = threading.Thread(target=self.robotVariable.MouvementRobotCarte, args=(self.CMDAccélération, self.CMDTemporisation))
                            thread2 = threading.Thread(target=self.Record_son)

                            # Lancez les threads
                            try:
                                thread1.start()
                                thread2.start()

                                running.clear()
                                print("thread clear")
                                thread1.join()
                                thread2.join()
                            except Exception as e:
                                print(f"Erreur lors de l'exécution des threads: {e}")
                            finally:
                                running.clear()
                                print("Threads terminés et événement clear")
                            print("accélération: ",self.CMDAccélération)#Affichage de la vitesse de la déscente
                            toc = time.perf_counter()
                            print(f"time: {toc - tic:0.4f} seconds")#Affichage du temps du cycle
                        Trans=self.lecture_son()# Lecture du son afin de déterminer s'il y a eu paiement ou non 
                        print(Trans)#Affichage du résultat, True(Paiement effectué), False(Paiement Non effectué)

                        #  self.PopUpTransaction() #Précédente version ou on devait dire soi-même s'il y avait transaction ou non 
                        
                    if Trans== True:
                        self.Pass_Transac_Auto() #Transaction Pass si on a donc nos bonnes valeurs de dirac
                        self.update()
                        
                    else:
                        self.Fail_Transac_Auto() # sinon Transaction Fail
                        self.update()
                    if(self.i==10): #Changement de position
                        self.SuppGA()
                        self.GroupeB()
                    elif(self.i==23):
                        self.SuppGB()
                        self.GroupeC()
                    elif(self.i==36):
                        self.SuppGC()
                        self.GroupeD()
                    elif(self.i==49):
                        self.SuppGD()
                        self.GroupeE()
                    elif (self.i == 62):
                        print("END")
                        break
                    
                except Exception as e:
                        self.PopUpErreurConnexion()#S'il n'arrive pas a faire ce qu'il y a au dessus il nous met un message d'erreur
                        print(e)
                        break
                
                if self.test2 == 1:
                        break       
            self.test2=0
        
     def Intercepte(self):
        if tkinter.messagebox.askokcancel("Notice", "Are you sure to close the transaction"):
           # close the application
           self.test.destroy()
           self.test2=1
           gc.collect()
           
     def destroyPop(self):
         self.test.destroy()
         gc.collect()        
         
     def PopUpErreurConnexion(self):
         self.message = "\n   Erreur de Connexion   \n"
         self.test = tk.Toplevel(bg = '#49A')
         self.test.geometry("190x120+300+300")
         self.test.focus_force()
         def callback(event)  :
            self.test.destroy()  
            gc.collect()
         self.test.resizable(width=0, height=0)
         self.text = tk.Label(self.test, text=self.message, font=("Century Gothic (Body)", 14),bg ='#49A')
         self.text.pack(side = "top")
         self.B1 = tk.Button(self.test, text="Ok",bg ='#49A',padx = 20,
                             pady = 5, command =lambda: self.destroyPop())
         self.B1.pack()
         self.test.bind('<Return>', callback) 
         
     def PopUpErreurFichier(self):
         self.message = "\n   Avez-vous créé le fichier ?   \n"
         self.test = tk.Toplevel(bg = '#49A')
         self.test.geometry("300x120+200+250")
         self.test.focus_force()
         self.test.resizable(width=0, height=0)
         
         def callback(event)  :
            self.Intercepte()  
        
         self.text = tk.Label(self.test, text=self.message, font=("Century Gothic (Body)", 14),bg ='#49A')
         self.text.pack(side = "top")
         self.B1 = tk.Button(self.test, text="Ok",bg ='#49A',padx = 30,
                             pady = 10, command =lambda: self.Intercepte())
         self.B1.pack(side = "bottom")
         self.test.bind('<Return>', callback) 
         self.wait_window(self.test)  
         
         
     def PopUpMontant(self):
         #self.protocole("WM_DELETE_WINDOW")
         self.message = "\n   Taper le Montant   \n"
         self.test = tk.Toplevel(bg ='#49A')
         self.test.geometry("200x130+300+300")
         self.test.resizable(width=0, height=0)
         self.test.focus_force()
         self.text = tk.Label(self.test, text=self.message, font=("Century Gothic (Body)", 14),bg ='#49A')
         self.text.pack(side = "top")
         def callback(event)  :
            self.test.destroy()
            gc.collect()
            
         def callbackReturn(event)  :
             self.Intercepte()   
            
         self.B1 = tk.Button(self.test, text="   Ok   ",bg ='#49A',padx = 25,
                             pady = 10, command =lambda: self.destroyPop())
         self.B1.pack(side = "left",padx = 5,pady =2)
         self.B2 = tk.Button(self.test, text="Annuler",bg ='#49A',padx = 25,
                             pady = 10, command =lambda: self.Intercepte())
         self.B2.pack(side = "right", padx = 5,pady =2)
         self.test.bind('<Cancel>', callbackReturn)
         self.test.bind('<Return>', callback)
         
         self.wait_window(self.test)

    
    # #  def PopUpPass(self):
        
    # #     self.test = tk.Toplevel(bg ='#49A')
    # #     self.test.geometry("400x130+200+250")
    # #     self.test.resizable(width=0, height=0)
    # #     self.test.focus_force()
    # #     self.t = tk.Label(self.test, text="Transaction Pass", font=("Century Gothic (Body)", 14),bg ='#49A')
    # #     self.t.pack(side = "top")
    # #     # time.sleep(1)

    # #     self.test.after(3000, lambda: self.close_popup())

    #  def PopUpFail(self):
        
    #     self.test = tk.Toplevel(bg ='#49A')
    #     self.test.geometry("400x130+200+250")
    #     self.test.resizable(width=0, height=0)
    #     self.test.focus_force()
    #     self.t = tk.Label(self.test, text="Transaction Fail", font=("Century Gothic (Body)", 14),bg ='#49A')
    #     self.t.pack(side = "top")
    #         # Simulation d'une tâche longue avec after()
    #     self.test.mainloop()
    #     self.test.after(3000, lambda: self.close_popup())

    
     def close_popup(self,T):
         T.destroy()

     def PopUpTransaction(self):
        self.message = "\n   Transaction :  \n"
        self.test = tk.Toplevel(bg = '#49A')
        self.test.geometry("300x180+300+300")
        self.test.resizable(width=0, height=0)
        self.test.focus_force()
        self.protocol("WM_DELETE_WINDOW")
        def callbackPass(event)  :
            self.PassTransaction()
            gc.collect()
        def callbackFail(event)  :
             self.FailTransaction()  
        def callbackReturn(event)  :
            self.Intercepte()   
            
        self.text = tk.Label(self.test, text=self.message, font=('Helvetica', 14),bg ='#49A')
        self.text.pack(side = "top")
        self.BPass = tk.Button(self.test, text="  Pass  ",bg ='#49A',padx = 25,
                             pady = 10, command =lambda: self.PassTransaction())
        self.BPass.pack(side = "left",padx = 5,pady =2)
        
        self.BFail = tk.Button(self.test, text="   Fail   ",bg ='#49A',padx = 25,
                             pady = 10, command =lambda: self.FailTransaction())
        self.BFail.pack(side = "right", padx = 5,pady =2)
        
        self.BExit = tk.Button(self.test, text="   exit   ",bg ='#49A',command =lambda: self.Intercepte())
        self.BExit.pack(side = "bottom", padx = 3,pady =2)
        
        self.test.bind('<Left>', callbackPass) 
        self.test.bind('<Right>', callbackFail) 
        self.test.bind('<Cancel>', callbackReturn)
         
        self.wait_window(self.test)

     def PassTransaction(self) :
         self.test.destroy()

         gc.collect()
         try: 
             
             if(self.i>=0 and self.i<11):
                 self.tabGroupeA[self.i].configure(image = self.photo)
                 self.saveEtatGroupeA[self.i]=1
             elif(self.i>=11 and self.i <24):
                 self.tabGroupeB[self.i-11].configure(image = self.photo)
                 self.saveEtatGroupeB[self.i-11]=1
             elif(self.i>=24 and self.i<37):
                 self.tabGroupeC[self.i-24].configure(image = self.photo)
                 self.saveEtatGroupeC[self.i-24]=1
             elif(self.i>=37 and self.i<50):
                 self.tabGroupeD[self.i-37].configure(image = self.photo)
                 self.saveEtatGroupeD[self.i-37]=1
             elif(self.i>=50 and self.i<=63):
                 self.tabGroupeE[self.i-50].configure(image = self.photo)
                 self.saveEtatGroupeE[self.i-50]=1
             self.fichier.TransactionPass(self.i)
         except :
             self.PopUpErreurFichier()
             
     def Pass_Transac_Auto(self):
        #  self.test.destroy()
        #  self.PopUpPass()
         gc.collect()
         try: 
             
             if(self.i>=0 and self.i<11):
                 self.tabGroupeA[self.i].configure(image = self.photo)
                 self.saveEtatGroupeA[self.i]=1
             elif(self.i>=11 and self.i <24):
                 self.tabGroupeB[self.i-11].configure(image = self.photo)
                 self.saveEtatGroupeB[self.i-11]=1
             elif(self.i>=24 and self.i<37):
                 self.tabGroupeC[self.i-24].configure(image = self.photo)
                 self.saveEtatGroupeC[self.i-24]=1
             elif(self.i>=37 and self.i<50):
                 self.tabGroupeD[self.i-37].configure(image = self.photo)
                 self.saveEtatGroupeD[self.i-37]=1
             elif(self.i>=50 and self.i<=63):
                 self.tabGroupeE[self.i-50].configure(image = self.photo)
                 self.saveEtatGroupeE[self.i-50]=1
             self.fichier.TransactionPass(self.i)
         except :
             self.PopUpErreurFichier()
             

     def FailTransaction(self) :
         self.test.destroy()

         gc.collect()
         try :      
             
             if(self.i>=0 and self.i <11):
                  self.tabGroupeA[self.i].configure(image = self.photo2)
                  self.saveEtatGroupeA[self.i]=2
             elif(self.i>=11 and self.i <24):
                 self.tabGroupeB[self.i-11].configure(image = self.photo2) 
                 self.saveEtatGroupeB[self.i-11]=2
             elif(self.i>=24 and self.i<37):
                 self.tabGroupeC[self.i-24].configure(image = self.photo2)
                 self.saveEtatGroupeC[self.i-24]=2
             elif(self.i>=37 and self.i<50):
                 self.tabGroupeD[self.i-37].configure(image = self.photo2)
                 self.saveEtatGroupeD[self.i-37]=2
             elif(self.i>=50 and self.i<=63):
                 self.tabGroupeE[self.i-50].configure(image = self.photo2)
                 self.saveEtatGroupeE[self.i-50]=2
             self.fichier.TransactionFail(self.i)
         except:
             self.PopUpErreurFichier()

     def Fail_Transac_Auto(self) :

         gc.collect()
         try :      
             
             if(self.i>=0 and self.i <11):
                  self.tabGroupeA[self.i].configure(image = self.photo2)
                  self.saveEtatGroupeA[self.i]=2
             elif(self.i>=11 and self.i <24):
                 self.tabGroupeB[self.i-11].configure(image = self.photo2) 
                 self.saveEtatGroupeB[self.i-11]=2
             elif(self.i>=24 and self.i<37):
                 self.tabGroupeC[self.i-24].configure(image = self.photo2)
                 self.saveEtatGroupeC[self.i-24]=2
             elif(self.i>=37 and self.i<50):
                 self.tabGroupeD[self.i-37].configure(image = self.photo2)
                 self.saveEtatGroupeD[self.i-37]=2
             elif(self.i>=50 and self.i<=63):
                 self.tabGroupeE[self.i-50].configure(image = self.photo2)
                 self.saveEtatGroupeE[self.i-50]=2
             self.fichier.TransactionFail(self.i)
         except:
             self.PopUpErreurFichier()
     def PopUpRecuperationCarte(self):
        self.message = "\n   Prendre la carte dans le socle? :  \n"
        self.test = tk.Toplevel(bg = '#49A')
        self.test.geometry("400x130+300+300")
        self.test.resizable(width=0, height=0)
        self.test.focus_force()
        self.protocol("WM_DELETE_WINDOW")
        self.choix=0
        
        def callbackOUI()  :
            
            self.test.destroy()
            gc.collect()
            self.choix=0
        def callbackNON()  :
            self.choix=1
            self.test.destroy()
            gc.collect()
          
        self.text = tk.Label(self.test, text=self.message, font=('Helvetica', 14),bg ='#49A')
        self.text.pack(side = "top")
        self.BOui = tk.Button(self.test, text="  Oui  ",bg ='#49A',padx = 25,
                             pady = 10,command =lambda: callbackOUI())
        self.BOui.pack(side = "left",padx = 5,pady =2)
        self.BOui = tk.Button(self.test, text="   Non   ",bg ='#49A',padx = 25,
                             pady = 10,command =lambda: callbackNON())
        self.BOui.pack(side = "right", padx = 5,pady =2)
         
        self.wait_window(self.test)
        #self.test.bind('<Right>', callbackNON)
        #self.test.bind('<Left>', callbackOUI) 
        return self.choix
        
     def RetourBouton(self):
        self.retourPhoto= tk.PhotoImage(file = "./Image/retourTest.png")
        self.retourBouton =tk.Button( self, image = self.retourPhoto, anchor = "center",relief="flat", bg = '#49A',
                                             command=lambda: self.RetourMenu())
        self.retourBouton.grid(row=0,column=8,sticky='ne')
     
     def PlayBouton(self):
        self.playPhoto= tk.PhotoImage(file = "./Image/play.png")
        self.playBouton =tk.Button( self, image = self.playPhoto, anchor = "center", relief="flat",
                                             bg = '#49A',command=lambda: self.ModeAutomatique())
        self.playBouton.grid(row=1,column=0,sticky="NE")
          

     def ZoneAcceleration(self):
         AccelerationEntree = tk.Frame(self, bg ='#49A',relief = 'groove',bd = 4)
         AccelerationEntree.grid(row=14,column= 6, columnspan = 4, padx = 10, pady = 5)
         self.accelerationValue = tk.Label(AccelerationEntree,
                              text="accélération (m/s):",
                              font =("Helvetica", 10, "bold"),
                              padx=10,
                              pady = 10,
                              fg ='#242874',
                              justify = "center",
                              bg ='#49A'
                              )
         self.accelerationValue.grid(row=14,column=6,sticky='e',padx = 5, pady = 5)
         self.AccelEntree = tk.Entry(AccelerationEntree,width =5, justify="center",font=('Helvetica', 15,"bold"),fg ='#242874', selectborderwidth = 10)
         self.AccelEntree.insert(8,"8")
         self.AccelEntree.grid(row=15, column=6,sticky='w',padx =5, pady = 5)
         
         self.boutonVitesse = tk.Button(AccelerationEntree,
               text = "entrer",
               font = ('Helvetica', 12,"bold"),
               anchor = "e",
               fg = '#49A',
               padx = 5,
               pady = 5,
               bg = "#FFFC6B",
               command=lambda: self.Acceleration()
               )
         self.boutonVitesse.grid(row=15,column=6,sticky="e")
     def ZoneTemporisation(self):
         TemporisationEntree = tk.Frame(self, bg ='#49A',relief = 'groove',bd = 4)
         TemporisationEntree.grid(row=14,column= 0, columnspan = 2, padx = 5, pady = 5)
         self.TemporisationValue = tk.Label(TemporisationEntree,
                              text="Temps dans le champ (s):",
                              font =("Helvetica", 10, "bold"),
                              padx=5,
                              pady = 5,
                              fg ='#242874',
                              justify = "left",
                              bg ='#49A'
                              )
         self.TemporisationValue.grid(row=14,column=0,sticky='NE',padx = 5, pady = 5)
         self.TempoEntree = tk.Entry(TemporisationEntree,width =5, justify="center",font=('Helvetica', 15,"bold"),fg ='#242874', selectborderwidth = 10)
         self.TempoEntree.insert(8,"1")
         self.TempoEntree.grid(row=15, column=0,sticky='w',padx =5, pady = 5)
         
         self.boutonTempo = tk.Button(TemporisationEntree,
               text = "entrer",
               font = ('Helvetica', 12,"bold"),
               anchor = "e",
               fg = '#49A',
               padx = 5,
               pady = 5,
               bg = "#FFFC6B",
               command=lambda: self.Temporisation()
               )
         self.boutonTempo.grid(row=15,column=0,sticky="e")

     def RetourMenu(self):
        self.windowPlace = self.geometry()
        self.destroy()
        gc.collect()
        self.enum = 0 
     def Acceleration(self):
         self.CMDAccélération=int(self.AccelEntree.get())
         if self.CMDAccélération>8:
             self.CMDAccélération=8
         print("valeur de l'accélération':"+self.AccelEntree.get()+" m/s²")  
         
     def Temporisation(self):
        self.CMDTemporisation=int(self.TempoEntree.get())
        print("valeur de temporisation:"+self.TempoEntree.get()+" s")
     def GroupeA(self):
         self.tabGroupeA.clear()
         self.gp = 0 
         self.tabGroupeA.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  fg='#49A',activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(0)
                  ))
         self.tabGroupeA[len(self.tabGroupeA) - 1].grid(row=6,column=4,sticky='WN')
         self.tabGroupeA.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(1)
                  ))
         self.tabGroupeA[len(self.tabGroupeA) - 1].grid(row=5,column=6,sticky='WN')
         
         self.tabGroupeA.append(tk.Button(self,
                 image = self.rond,
                 borderwidth  = 0,
                 highlightthickness = 0,
                 relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(2)
                  ))
         self.tabGroupeA[len(self.tabGroupeA) - 1].grid(row=2,column=4,sticky='WN')
          
         self.tabGroupeA.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                 bg ='#49A',
                 activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(3)
                  ))
         self.tabGroupeA[len(self.tabGroupeA) - 1].grid(row=5,column=2,sticky='WN')
        
         self.tabGroupeA.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(4)
                  ))
         self.tabGroupeA[len(self.tabGroupeA) - 1].grid(row=7,column=2,sticky='WN')
         
         self.tabGroupeA.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(5)
                  ))
         self.tabGroupeA[len(self.tabGroupeA) - 1].grid(row=9,column=4,sticky='WN')
         
         self.tabGroupeA.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                 bg ='#49A',
                 activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(6)
                  ))
         self.tabGroupeA[len(self.tabGroupeA) - 1].grid(row=7,column=6,sticky='WN')
        
         self.tabGroupeA.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                 bg ='#49A',
                 activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(7)
                  ))
         self.tabGroupeA[len(self.tabGroupeA) - 1].grid(row=5,column=5,sticky='WN')
         
         self.tabGroupeA.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(8)
                  ))
         self.tabGroupeA[len(self.tabGroupeA) - 1].grid(row=5,column=3,sticky='WN')
        
         self.tabGroupeA.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(9)
                  ))
         self.tabGroupeA[len(self.tabGroupeA) - 1].grid(row=7,column=3,sticky='WN')
         self.tabGroupeA.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(10)
                  ))
         self.tabGroupeA[len(self.tabGroupeA) - 1].grid(row=7,column=5,sticky='WN')
         for i in range(0,len(self.tabGroupeA)):
             if(self.saveEtatGroupeA[i]==0):
                 self.tabGroupeA[i].configure(image = self.rond)
             elif (self.saveEtatGroupeA[i]==2):
                 self.tabGroupeA[i].configure(image = self.photo2)
             elif (self.saveEtatGroupeA[i]==1):
                 self.tabGroupeA[i].configure(image = self.photo)
                   
     def GroupeB(self):
       self.tabGroupeB.clear()
       self.gp = 1 
       
       self.tabGroupeB.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(11)
                  ))
       self.tabGroupeB[len(self.tabGroupeB) - 1].grid(row=5,column=4,sticky='WN')
       
       self.tabGroupeB.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(12)
                  ))
       self.tabGroupeB[len(self.tabGroupeB) - 1].grid(row=4,column=6,sticky='WN')
     
       self.tabGroupeB.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(13)
                  ))
       self.tabGroupeB[len(self.tabGroupeB) - 1].grid(row=3,column=4,sticky='WN')
      
       self.tabGroupeB.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(14)
                  ))
       self.tabGroupeB[len(self.tabGroupeB) - 1].grid(row=4,column=2,sticky='WN')
       
       self.tabGroupeB.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(15)
                  ))
       self.tabGroupeB[len(self.tabGroupeB) - 1].grid(row=6,column=2,sticky='WN')
       
       self.tabGroupeB.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(16)
                  ))
       self.tabGroupeB[len(self.tabGroupeB) - 1].grid(row=7,column=4,sticky='WN')
     
       self.tabGroupeB.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(17)
                  ))
       self.tabGroupeB[len(self.tabGroupeB) - 1].grid(row=6,column=6,sticky='WN') 
      
       self.tabGroupeB.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  activebackground ='#49A',
                  bg ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(18)
                  ))
       self.tabGroupeB[len(self.tabGroupeB) - 1].grid(row=5,column=7,sticky='WN')

       self.tabGroupeB.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(19)
                  ))
       self.tabGroupeB[len(self.tabGroupeB) - 1].grid(row=2,column=6,sticky='WN')

       self.tabGroupeB.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(20)
                  ))
       self.tabGroupeB[len(self.tabGroupeB) - 1].grid(row=2,column=2,sticky='WN')

       self.tabGroupeB.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(21)
                  ))
       self.tabGroupeB[len(self.tabGroupeB) - 1].grid(row=5,column=1,sticky='WN')
      
       self.tabGroupeB.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(22)
                  ))
       self.tabGroupeB[len(self.tabGroupeB) - 1].grid(row=8,column=2,sticky='WN')
      
       self.tabGroupeB.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  activebackground ='#49A',
                  bg ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(23)
                  ))
       self.tabGroupeB[len(self.tabGroupeB) - 1].grid(row=8,column=6,sticky='WN')
       
       for i in range(0,len(self.tabGroupeB)):
             if(self.saveEtatGroupeB[i]==0):
                 self.tabGroupeB[i].configure(image = self.rond)
             elif (self.saveEtatGroupeB[i]==2):
                 self.tabGroupeB[i].configure(image = self.photo2)
             elif (self.saveEtatGroupeB[i]==1):
                 self.tabGroupeB[i].configure(image = self.photo)
       
     def GroupeD(self):
       self.tabGroupeD.clear()
       self.gp = 3 
       self.tabGroupeD.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(37)
                  ))
       self.tabGroupeD[len(self.tabGroupeD) - 1].grid(row=5,column=4,sticky='WN')
       
       self.tabGroupeD.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(38)
                  ))
       self.tabGroupeD[len(self.tabGroupeD) - 1].grid(row=4,column=6,sticky='WN')
     
       self.tabGroupeD.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(39)
                  ))
       self.tabGroupeD[len(self.tabGroupeD) - 1].grid(row=3,column=4,sticky='WN')
      
       self.tabGroupeD.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(40)
                  ))
       self.tabGroupeD[len(self.tabGroupeD) - 1].grid(row=4,column=2,sticky='WN')
       
       self.tabGroupeD.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(41)
                  ))
       self.tabGroupeD[len(self.tabGroupeD) - 1].grid(row=6,column=2,sticky='WN')
       
       self.tabGroupeD.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(42)
                  ))
       self.tabGroupeD[len(self.tabGroupeD) - 1].grid(row=7,column=4,sticky='WN')
     
       self.tabGroupeD.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(43)
                  ))
       self.tabGroupeD[len(self.tabGroupeD) - 1].grid(row=6,column=6,sticky='WN') 
      
       self.tabGroupeD.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(44)
                  ))
       self.tabGroupeD[len(self.tabGroupeD) - 1].grid(row=5,column=7,sticky='WN')

       self.tabGroupeD.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(45)
                  ))
       self.tabGroupeD[len(self.tabGroupeD) - 1].grid(row=2,column=6,sticky='WN')

       self.tabGroupeD.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(46)
                  ))
       self.tabGroupeD[len(self.tabGroupeD) - 1].grid(row=2,column=2,sticky='WN')

       self.tabGroupeD.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(47)
                  ))
       self.tabGroupeD[len(self.tabGroupeD) - 1].grid(row=5,column=1,sticky='WN')
      
       self.tabGroupeD.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                 activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(48)
                  ))
       self.tabGroupeD[len(self.tabGroupeD) - 1].grid(row=8,column=2,sticky='WN')
      
       self.tabGroupeD.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(49)
                  ))
       self.tabGroupeD[len(self.tabGroupeD) - 1].grid(row=8,column=6,sticky='WN')
       
       for i in range(0,len(self.tabGroupeD)):
             if(self.saveEtatGroupeD[i]==0):
                 self.tabGroupeD[i].configure(image = self.rond)
             elif (self.saveEtatGroupeD[i]==2):
                 self.tabGroupeD[i].configure(image = self.photo2)
             elif (self.saveEtatGroupeD[i]==1):
                 self.tabGroupeD[i].configure(image = self.photo)
      
     def GroupeC(self):
      self.tabGroupeC.clear() 
      self.gp = 2 
      self.tabGroupeC.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(24)
                  ))
      self.tabGroupeC[len(self.tabGroupeC) - 1].grid(row=7,column=4,sticky='WN')
      
      self.tabGroupeC.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(25)
                  ))
      self.tabGroupeC[len(self.tabGroupeC) - 1].grid(row=7,column=6,sticky='WN')
          
      self.tabGroupeC.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(26)
                  ))
      self.tabGroupeC[len(self.tabGroupeC) - 1].grid(row=5,column=5,sticky='WN')
      
      self.tabGroupeC.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(27)
                  ))
      self.tabGroupeC[len(self.tabGroupeC) - 1].grid(row=5,column=3,sticky='WN')
      
      self.tabGroupeC.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(28)
                  ))
      self.tabGroupeC[len(self.tabGroupeC) - 1].grid(row=7,column=2,sticky='WN')
      
      self.tabGroupeC.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(29)
                  ))
      self.tabGroupeC[len(self.tabGroupeC) - 1].grid(row=9,column=3,sticky='WN')
      
      self.tabGroupeC.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  activebackground ='#49A',
                  anchor='center',
                  bg ='#49A',
                  command=lambda: self.FunctionManuel(30)
                  ))
      self.tabGroupeC[len(self.tabGroupeC) - 1].grid(row=9,column=5,sticky='WN')
      
      self.tabGroupeC.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  activebackground ='#49A',
                  anchor='center',
                  bg ='#49A',
                  command=lambda: self.FunctionManuel(31)
                  ))
      self.tabGroupeC[len(self.tabGroupeC) - 1].grid(row=5,column=7,sticky='WN')

      self.tabGroupeC.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(32)
                  ))
      self.tabGroupeC[len(self.tabGroupeC) - 1].grid(row=1,column=4,sticky='WN')

      self.tabGroupeC.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(33)
                  ))
      self.tabGroupeC[len(self.tabGroupeC) - 1].grid(row=5,column=1,sticky='WN')

      self.tabGroupeC.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(34)
                  ))
      self.tabGroupeC[len(self.tabGroupeC) - 1].grid(row=9,column=1,sticky='WN')
      
      self.tabGroupeC.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(35)
                  ))
      self.tabGroupeC[len(self.tabGroupeC) - 1].grid(row=12,column=4,sticky='WN')
      
      self.tabGroupeC.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(36)
                  ))
      self.tabGroupeC[len(self.tabGroupeC) - 1].grid(row=9,column=7,sticky='WN')
      
      for i in range(0,len(self.tabGroupeC)):
             if(self.saveEtatGroupeC[i]==0):
                 self.tabGroupeC[i].configure(image = self.rond)
             elif (self.saveEtatGroupeC[i]==2):
                 self.tabGroupeC[i].configure(image = self.photo2)
             elif (self.saveEtatGroupeC[i]==1):
                 self.tabGroupeC[i].configure(image = self.photo)
                 
     def GroupeE(self):
      self.tabGroupeE.clear() 
      self.gp = 4 
      self.tabGroupeE.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(50)
                  ))
      self.tabGroupeE[len(self.tabGroupeE) - 1].grid(row=7,column=4,sticky='WN')
      
      self.tabGroupeE.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(51)
                  ))
      self.tabGroupeE[len(self.tabGroupeE) - 1].grid(row=7,column=6,sticky='WN')
          
      self.tabGroupeE.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(52)
                  ))
      self.tabGroupeE[len(self.tabGroupeE) - 1].grid(row=5,column=5,sticky='WN')
      
      self.tabGroupeE.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(53)
                  ))
      self.tabGroupeE[len(self.tabGroupeE) - 1].grid(row=5,column=3,sticky='WN')
      
      self.tabGroupeE.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(54)
                  ))
      self.tabGroupeE[len(self.tabGroupeE) - 1].grid(row=7,column=2,sticky='WN')
      
      self.tabGroupeE.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(55)
                  ))
      self.tabGroupeE[len(self.tabGroupeE) - 1].grid(row=9,column=3,sticky='WN')
      
      self.tabGroupeE.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(56)
                  ))
      self.tabGroupeE[len(self.tabGroupeE) - 1].grid(row=9,column=5,sticky='WN')
      
      self.tabGroupeE.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(57)
                  ))
      self.tabGroupeE[len(self.tabGroupeE) - 1].grid(row=5,column=7,sticky='WN')

      self.tabGroupeE.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  bg ='#49A',
                  activebackground ='#49A',
                  anchor='center',
                  command=lambda: self.FunctionManuel(58)
                  ))
      self.tabGroupeE[len(self.tabGroupeE) - 1].grid(row=1,column=4,sticky='WN')

      self.tabGroupeE.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  activebackground ='#49A',
                  anchor='center',
                  bg ='#49A',
                  command=lambda: self.FunctionManuel(59)
                  ))
      self.tabGroupeE[len(self.tabGroupeE) - 1].grid(row=5,column=1,sticky='WN')

      self.tabGroupeE.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  activebackground ='#49A',
                  anchor='center',
                  bg ='#49A',
                  command=lambda: self.FunctionManuel(60)
                  ))
      self.tabGroupeE[len(self.tabGroupeE) - 1].grid(row=9,column=1,sticky='WN')
      
      self.tabGroupeE.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  font =("Century Gothic (Body)", 14),
                  activebackground ='#49A',
                  anchor='center',
                  bg ='#49A',
                  command=lambda: self.FunctionManuel(61)
                  ))
      self.tabGroupeE[len(self.tabGroupeE) - 1].grid(row=12,column=4,sticky='WN')
      
      self.tabGroupeE.append(tk.Button(self,
                  image = self.rond,
                  borderwidth  = 0,
                  highlightthickness = 0,
                  relief="flat",
                  font =("Century Gothic (Body)", 14),
                  activebackground ='#49A',
                  anchor='center',
                  bg ='#49A',
                  command=lambda: self.FunctionManuel(62)
                  ))
      self.tabGroupeE[len(self.tabGroupeE) - 1].grid(row=9,column=7,sticky='WN') 
      
      for i in range(0,len(self.tabGroupeE)):
             if(self.saveEtatGroupeE[i]==0):
                 self.tabGroupeE[i].configure(image = self.rond)
             elif (self.saveEtatGroupeE[i]==2):
                 self.tabGroupeE[i].configure(image = self.photo2)
             elif (self.saveEtatGroupeE[i]==1):
                 self.tabGroupeE[i].configure(image = self.photo)
    
     def SuppGA(self): 
        for i in  range (0,len(self.tabGroupeA)):   
            self.tabGroupeA[i].grid_forget()               
     def SuppGB(self):      
        for i in  range (0,len(self.tabGroupeB)):   
            self.tabGroupeB[i].grid_forget()      
     def SuppGC(self):      
        for i in  range (0,len(self.tabGroupeC)):   
            self.tabGroupeC[i].grid_forget()  
     def SuppGD(self):  
        for i in  range (0,len(self.tabGroupeD)):   
            self.tabGroupeD[i].grid_forget()       
     def SuppGE(self):      
        for i in  range (0,len(self.tabGroupeE)):   
            self.tabGroupeE[i].grid_forget()
            
     """def RecuperationCarte(self):
        if (self.carteBouton['text']== "1"):
            
            self.carteBouton.configure(image = self.carte)
            self.carteBouton.configure(text = "2")
            self.robotVariable.RecuperationCarte()
        elif (self.carteBouton['text']== "2"):
            self.robotVariable.PoseCarte()
            self.carteBouton.configure(image = self.carte2)
            self.carteBouton.configure(text = "1")
            
     def BoutonCarte(self):
         
         self.carteBouton = tk.Button(self,
                  image = self.carte2,
                  borderwidth=3,
                  text = "1",
                  highlightthickness = 0,
                  relief="raised",
                  anchor="center",
                  activebackground ='#49A',
                  bg ='#49A',
                  command=lambda: self.RecuperationCarte()
                  )
         self.carteBouton.grid(row=14,column=0, padx = 5, pady = 5)"""

            
     def FunctionManuel(self,number):
         if self.manuelActive == True : 
             try:
                 self.robotVariable.RecupCoordonneeRobot()
                 self.robotVariable.mode = 2
                 self.i = number
                 if self.robotVariable.variabletest == 2 :
                     print(self.i)
                     self.robotVariable.Conversion(self.i)
                     self.robotVariable.PositionInitiale() 
                     self.PopUpMontant()
                     print(self.robotVariable.xRobot,self.robotVariable.yRobot,self.robotVariable.zRobot)
                     self.robotVariable.MouvementRobotCarte(self.CMDAccélération,self.CMDTemporisation)
                 else :
                    self.robotVariable.Conversion(self.i)
                    self.PopUpMontant()
                    print(self.robotVariable.xRobot,self.robotVariable.yRobot,self.robotVariable.zRobot)
                      
                 self.PopUpTransaction()
             except:
                self.PopUpErreurConnexion()
        
            