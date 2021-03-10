#pip install SpeechRecognition,PyAudio
import speech_recognition
import os
import time
import pyttsx3 #Text to speech
import json
from main import read_addonFile
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
def GOTO(eval,variables):
    #On recupere le fichier a charger
    newAddonFile = str(eval[str(len(eval)-1)].value)
    #On ajoute l'index du nouveau fichier (0, premiere ligne donc -1 comme on vas passer a l'instruction suivante)
    variables["INSTRUCTION_INDEX"].append(-1)
    #On ajoute les instruction du nouveau fichier
    variables["INSTRUCTION_FILE_LIST"].append(read_addonFile(newAddonFile))
    return variables
def WAIT(eval):
    #On attend
    time.sleep(float(eval[str(len(eval)-2)]))
    return

def EXECUTE(eval):
    filePath = str(eval[str(len(eval)-2)])
    os.popen(filePath)
    return
    
def OPEN_BROWER(eval):
    browserPath = eval[str(eval[str(len(eval)-1)].nameNode1)]
    mode = eval[str(eval[str(len(eval)-1)].nameNode2)]
    url = eval[str(eval[str(len(eval)-1)].nameNode3)]
    if mode == "PUBLIC":
        os.system('"'+browserPath+"\" "+url)
    else:
        os.system('"'+browserPath+"\" -incognito "+url)
    return

def DB_SAVE(eval):
    key = eval[str(eval[str(len(eval)-1)].nameNode1)]
    value = eval[str(eval[str(len(eval)-1)].nameNode2)]
    #Si la db existe
    if not(os.path.exists("lib/data")):
        db = {}
    else:
        #On charge la db
        with open('lib/data') as json_file:
            db = json.load(json_file)
    db[key] = value
    #On save la db
    with open('lib/data', 'w') as outfile:
        json.dump(db, outfile)
    return
def DB_DEL(eval):
    key = eval[str(eval[str(len(eval)-1)].nameNode1)]
    #Si la db existe
    if not(os.path.exists("lib/data")):
        db = {}
    else:
        #On charge la db
        with open('lib/data') as json_file:
            db = json.load(json_file)
    #Si la key existe
    if key in db.keys():
        del db[key]
    #On save la db
    with open('lib/data', 'w') as outfile:
        json.dump(db, outfile)
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
    if instructionType == "GOTO":
        variables = GOTO(eval,variables)
    if instructionType == "WAIT":
        WAIT(eval)

    if instructionType == "EXECUTE":
        EXECUTE(eval)
    
    if instructionType == "OPEN_BROWSER":
        OPEN_BROWER(eval)
    
    if instructionType == "DB_SAVE":
        DB_SAVE(eval)
    if instructionType == "DB_DEL":
        DB_DEL(eval)

    return variables