# import required libraries
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
from scipy.fft import fft,fftfreq
from numpy import linspace 
import matplotlib.pyplot as plt
from scipy.io import wavfile
from FichierConfigLecteur import FichierReader

class FFT_signal(FichierReader):
    def __init__(self):

        self.val_max=0
        self.val_max2=0
        self.val_max3=0
        self.verif=False
    
    def Record_son(self):
        # Fréquence de capture 
        freq = 44100
        # DUREE D'ENREGISTREMENT
        duration = 6
        
        
        # DEBUT DU RECORD AUDIO 
        recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
        print("début de l'enregistrement")
        # ON ATTEND LE TEMPS DE DURATION
        sd.wait()
        print("fin de l'enregistrement")

        # ECRITURE D'UN FICHIER WAV RECORD 0
        write("./Son/recording0.wav", freq, recording)

        # ECRITURE D'UN FICHIER WAV RECORD 1
        wv.write("./Son/recording1.wav", recording, freq, sampwidth=2)

    def lecture_son(self):
        # LECTURE DU FICHIER
        rate, data = wavfile.read('./Son/recording1.wav')

        x = data[:, 0]  
        # cREATION D'INSTANCE D'ECHANTILLONAGE
        t = linspace(0, data.shape[0]/rate, data.shape[0])

        # TRACE D'ECHANTILLONAGE
        # plt.subplot(2,1,1)
        # plt.plot(t, x, label="Signal échantillonné")

        # plt.xlabel(r"$t$ (s)")
        # plt.ylabel(r"Amplitude")
        # plt.title(r"Signal sonore")

        # plt.grid()

        # CALCUL FFT
        X = fft(x)  # TRANSFORMEE DE FOURRIER
        freq = fftfreq(x.size, d=1/rate)  # FREQUENCE DE LA TF

        # CALCUL DU NOMBRE D'ECHANTILLONS
        N = x.size

        # On prend la valeur absolue de l'amplitude uniquement pour les fréquences positives et normalisation
        X_abs = abs(X[:N//2])*2.0/N
        # On garde uniquement les fréquences positives
        freq_pos = freq[:N//2]
        # plt.subplot(2,1,2)
        # plt.plot(freq_pos, X_abs, label="Amplitude absolue")
        # plt.xlim(0, 7000)  # On réduit la plage des fréquences à la zone utile
        # plt.xlabel(r"Fréquence (Hz)")
        # plt.ylabel(r"Amplitude $|self.X(f)|$")
        # plt.title("Transformée de Fourier ")
        # plt.grid()
        # AFIN DE VERIFICATION VOUS POUVEZ ENLEVER PLT.SHOW DU FORMAT COMMENTAIRE CELA VOUS DONNERA LE GRAPH DE LA FFT DU SIGNAL
        #plt.show() 
        print (N)
        print(freq_pos,X_abs)
        transaction=self.Verification_transaction(N,freq_pos,X_abs)
        return transaction


    def Verification_transaction(self,N,freq_pos,X_abs):
        # ON BALAYE LES POINTS PAR FREQUENCE
        val_max=0
        val_max2=0
        val_max3=0
        nb_dir,D1,D2,D3= self.ValueSave()
        for i in range(N//2-1):

            # ON ENCADRE LES FREQUENCE QUE L'ON SOUHAITE POUR BALAYER L'AMPLITUDE ET NOUS DONNER LA VALEUR MAX 
            
            # DU DIRAC DE CE SON, ON FAIT CA SUR 2 DIRAC si on en a que 2.


            if float(freq_pos[i])>D1-20 and float(freq_pos[i])<D1+20:
                num=X_abs[i]
                if num>val_max:
                    verif=True
                else:
                    verif=False
                if verif == True:
                    val_max=num
                    print(val_max)
            if float(freq_pos[i])>D2-20 and float(freq_pos[i])<D2+20:
                num=X_abs[i]
                if num>val_max2:
                    verif2=True
                else:
                    verif2=False
                if verif2 == True:
                    val_max2=num
                    print(val_max2)
                        #  ON VERIFIE ICI QUE L'ON A BIEN UNE TRANSACTION EN VERIFIANT QUE L'AMPLITUDE DE NOS 2 DIRAC SONT AU DESSUS DE LA PIRE VALEUR
                print(val_max)
                
            
            
        # if nb_dir==2 :    
        print(val_max)
        if val_max>17 and val_max2>12 : 
            print("Paiement Effectué")
            print(val_max,val_max2,val_max3)
            #VARIABLE DONNANT LE RESULTAT SI NOTRE TRANSACTION EST FAITE OU NON 
            Transaction=True
            
        else:
            print("Paiement Non-Effectué")
            print(val_max,val_max2,val_max3)
            Transaction=False
        

        return Transaction
    

            
    
            

        # #  ON VERIFIE ICI QUE L'ON A BIEN UNE TRANSACTION EN VERIFIANT QUE L'AMPLITUDE DE NOS 3 DIRAC SONT AU DESSUS DE LA PIRE VALEUR
        # print(val_max)
        # if val_max>50 and val_max2>25 and val_max3>10:
        #     print("Paiement Effectué")
        #     print(val_max,val_max2,val_max3)
        #     #VARIABLE DONNANT LE RESULTAT SI NOTRE TRANSACTION EST FAITE OU NON 
        #     Transaction=True
            
        # else:
        #     print("Paiement Non-Effectué")
        #     print(val_max,val_max2,val_max3)
        #     Transaction=False
        # return Transaction

