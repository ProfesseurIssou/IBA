# pyinstaller -y -F --hidden-import pyttsx3.drivers --hidden-import pyttsx3.drivers.sapi5  "D:/projet/projet/IBA (IssouBot Assistant)/src/main.py"

import unidecode        #pour les caractere special
#pip install SpeechRecognition,PyAudio
import speech_recognition
import ISCODE

def listen():
    query = None            #Reponse de l'utilisateur
    while query == None:    #Tant qu'on a rien recus
        #voir la qualité micro
        r = speech_recognition.Recognizer()
        with speech_recognition.Microphone() as source:
            r.adjust_for_ambient_noise(source,0.5)
            r.pause_threshold = 0.5 #temp d'attente d'une commande utilisateur
            audio = r.listen(source)
        try:
            query = r.recognize_google(audio,language="fr-FR")
        except:
            query = None
    return query


if __name__ == "__main__":
    env = ISCODE.ISCODE()           #On cree l'environnement
    while 1:                        #Boucle infinie
        env.reset()                     #On reinitialise l'environement
        query = unidecode.unidecode(listen().lower())   #On ecoute, on enleve les caractere special
        env.executeIbFile("config.ib",{"_CPATH_":"lib/","query":query})#On lance l'execution de config.ib en mettant une variable supplementaire (query) et en changeant le dossier de travail