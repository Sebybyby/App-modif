from scipy.io.wavfile import write
import wavio as wv
import sounddevice as sd
import numpy as np
from scipy.fft import fft, fftfreq
from numpy import linspace
import matplotlib.pyplot as plt
from scipy.io import wavfile
from RecordAudio import Record
from PySide6.QtWidgets import QMessageBox


class fftsignallecteur(Record):

    def Comparaison_totale(self):
        self.Prem_Ecoute()
        print("Première écoute terminée, Réalisez maintenant la seconde écoute")
        self.message_deuxiemeecoute()
        self.Seconde_Ecoute()
        self.Verification()

    def Verification(self):
        marge_similarite = 15
        toutes_les_valeurs_similaires = []
        dirac = []
        Sum = 0
        Moyenne = 0
        f1 = []
        f2 = []
        f3 = []
        f4 = []
        rate1, data1 = wavfile.read("./Son/Signalno1det.wav")
        rate2, data2 = wavfile.read("./Son/Signalno2det.wav")

        ech_signal1 = self.echantillonage(rate1, data1)
        ech_signal2 = self.echantillonage(rate2, data2)

        Signal1 = self.Calcul_signal_FFT(ech_signal1[0], rate1)
        Signal2 = self.Calcul_signal_FFT(ech_signal2[0], rate2)

        Amp_max1, f1 = self.Balayage(Signal1[1], Signal1[0], Signal1[2])
        Amp_max2, f2 = self.Balayage(Signal2[1], Signal2[0], Signal2[2])

        print(Amp_max1)
        print(Amp_max2)
        print(f1)
        print(f2)

        Compt, liste_frequence = self.Comparaison(f1, f2)
        print("Comp", Compt)
        print("liste frequence:", liste_frequence)

        valeurs_differentes = liste_frequence.copy()

        while valeurs_differentes:
            ref_valeur = valeurs_differentes[0]
            valeurs_similaires = [ref_valeur]

            for valeur in valeurs_differentes[1:]:
                if abs(valeur - ref_valeur) <= marge_similarite:
                    valeurs_similaires.append(valeur)

            toutes_les_valeurs_similaires.append(valeurs_similaires)
            valeurs_differentes = [val for val in valeurs_differentes if val not in valeurs_similaires]

        for i, valeurs_similaires in enumerate(toutes_les_valeurs_similaires):
            print(f"Valeurs similaires à l'itération {i+1} :", valeurs_similaires)

        if len(toutes_les_valeurs_similaires) >= 2:
            Lecteur = True
            print("Lecteur Initialisé")
        else:
            Lecteur = False
            print("Lecteur Non Initialisé")
            QMessageBox.critical(None, "Erreur",
                "Lecteur Non Initialisé, Pas assez de valeurs de fréquences de diracs communes.")

        for z in range(len(toutes_les_valeurs_similaires)):
            Sum = 0
            for p in range(len(toutes_les_valeurs_similaires[z])):
                Sum = (Sum + toutes_les_valeurs_similaires[z][p])
            Moyenne = Sum / len(toutes_les_valeurs_similaires[z])
            dirac.append(Moyenne)
        print("Dirac :", dirac)
        print("Lecteur", Lecteur)
        print("Toutes les valeurs similaires :", toutes_les_valeurs_similaires)
        return dirac

    def Calcul_signal_FFT(self, z, r):
        X = fft(z)
        freq = fftfreq(z.size, d=1 / r)
        N = z.size
        X_abs = abs(X[:N // 2]) * 2.0 / N
        freq_pos = freq[:N // 2]
        return X_abs, freq_pos, N

    def echantillonage(self, rate, data):
        x = data[:, 0]
        t = linspace(0, data.shape[0] / rate, data.shape[0])
        return x, t

    def Balayage(self, freq, ampl, N):
        val_max = 0
        frequence = []
        for i in range(N // 2 - 1):
            if float(freq[i]) > 1000 and float(freq[i]) < 20000:
                if float(ampl[i]) > 50:
                    frequence.append(float(freq[i]))
                num = float(ampl[i])
                if num > val_max:
                    verif = True
                else:
                    verif = False
                if verif is True:
                    val_max = num
        return val_max, frequence

    def Comparaison(self, f, f1):
        n = 0
        compteur = 0
        liste_freq = []
        for i in range(len(f)):
            n = 0
            while n != len(f1):
                if f[i] == f1[n]:
                    compteur = compteur + 1
                    liste_freq.append(f[i])
                n = n + 1
        print(liste_freq)
        return compteur, liste_freq

    def message_deuxiemeecoute(self):
        QMessageBox.information(None, "Nouvelle écoute", "Veuillez préparer une nouvelle écoute.")
