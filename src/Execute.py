#pip install SpeechRecognition,PyAudio
import speech_recognition
import os
import pyttsx3 #Text to speech
engine = pyttsx3.init()#on init le convertisseur text->vocal


def SET(eval,variables):
    #On prend l'instruction, on eleve les espace, on coupe a partir de "=" et on prend le nom de la variable
    variableName = eval[str(len(eval)-1)].value.replace(" ","").split("=")[0]
    #On recupere la valeur de la variable
    variableValue = eval[eval[str(len(eval)-1)].nameNode1]
    #On ajoute la variable
    variables[variableName] = variableValue
    return variables

def PRINT(eval):
    #On affiche le text demandé
    print(eval[str(len(eval)-2)])
    return

def CONDITION(eval,variables):
    #Si la condition est vrai
    if eval[str(len(eval)-2)] == 1:
        #On passe a l'indentation superieur
        variables["%INDENTATION%"]+=1
    return variables

def SPEAK(eval):
    #On lance l'audio
    engine.say(str(eval[str(len(eval)-2)]))
    #On lance est on attend
    engine.runAndWait()
    return
def LISTEN(eval,variables):
    #voir la qualité micro
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        r.adjust_for_ambient_noise(source,0.5)
        r.pause_threshold = 0.5 #temp d'attente d'une commande utilisateur
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio,language="fr-FR")
    except:
        query = "None"
    
    #On prend le resultat audio et on le met dans les variable
    variables[eval['0'].value] = query
    return variables

def EXECUTE(eval):
    filePath = str(eval[str(len(eval)-2)])
    os.system(filePath)
    return

def execute(eval,variables):
    #On recupere le type de l'instruction
    instructionType = eval[str(len(eval)-1)].type
    if instructionType == "SET":
        variables = SET(eval,variables)

    if instructionType == "PRINT":
        PRINT(eval)

    if instructionType == "CONDITION":
        variables = CONDITION(eval,variables)

    if instructionType == "SPEAK":
        SPEAK(eval)
    if instructionType == "LISTEN":
        LISTEN(eval,variables)

    if instructionType == "EXECUTE":
        EXECUTE(eval)
        
    return variables