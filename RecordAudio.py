from scipy.io.wavfile import write
import wavio as wv
import sounddevice as sd
from PartieLecteurPopUp import Popup
from multiprocessing import Pool
 
class Record(Popup):

    def Prem_Ecoute(self):
       
        freq= 44100
        
        duration = 4

        recording = sd.rec(int(duration * freq), 
                        samplerate=freq, channels=2)

        print("début de l'enregistrement")
        sd.wait()
        print("fin de l'enregistrement")
    
        write("./Son/Signalno1.wav", freq, recording)


        wv.write("./Son/Signalno1det.wav", recording, freq, sampwidth=2)






    def Seconde_Ecoute(self):

        freq= 44100


        duration = 4
        recording = sd.rec(int(duration * freq), 
                        samplerate=freq, channels=2)

        print("début de l'enregistrement")

        sd.wait()
        print("fin de l'enregistrement")


        write("./Son/Signalno2.wav", freq, recording)

        wv.write("./Son/Signalno2det.wav", recording, freq, sampwidth=2)
