# pyinstaller -y -F --hidden-import pyttsx3.drivers --hidden-import pyttsx3.drivers.sapi5  "D:/projet/projet/IBA (IssouBot Assistant)/src/main.py"

import Lexer, Parser, Eval, Execute
import unidecode #pour les accent
import json,datetime
#pip install SpeechRecognition,PyAudio
import speech_recognition

def listen():
    #Reponse de l'utilisateur
    query = None
    #Tant qu'on a rien recus
    while query == None:
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

def search_addonFile(trigger):
    with open("lib/Default.json") as json_file:
        data = json.load(json_file)
    #on verifie l'existance du trigger
    if trigger in data.keys():
        return data[trigger]
    else:
        return False
def read_addonFile(File_Name):
    Addon_File = open("lib/"+str(File_Name),"r")
    Addon_Instruction = Addon_File.readlines()
    Addon_File.close()
    return Addon_Instruction

def time_(value):
    if value == "ALL":
        return datetime.datetime.now().strftime("%H:%M:%S")
    elif value == "hour":
        return datetime.datetime.now().hour
    elif value == "minute":
        return datetime.datetime.now().minute
    elif value == "second":
        return datetime.datetime.now().second
def date_(value):
    # if value == "ALL":
        # return datetime.datetime.now()
    if value == "year":
        return datetime.datetime.now().year
    elif value == "month":
        return datetime.datetime.now().month
    elif value == "day":
        return datetime.datetime.now().day

def execute_Instruction(Instruction_List,query):
    #le stockage des variable de l'addon
    Addon_Variable = {
        "INSTRUCTION_INDEX":[0],#Liste des index au fur et a mesure des fichier [indexFile1,indexFile2]
        "INSTRUCTION_FILE_LIST":[Instruction_List],#Liste des instruction entre chaque fichier et sous fichier [[instructionListFicher1],[InstructionListFichier2]]
        "%INDENTATION%":0,       #Pour le condition
        "%query%":str(query)    #Ce qu'on a recus
    }
    #Tant qu'on a pas fini tout les fichier
    while Addon_Variable["INSTRUCTION_FILE_LIST"] != []:
        #On definie les date
        Addon_Variable["%year%"] = int(date_("year"))
        Addon_Variable["%month%"] = int(date_("month"))
        Addon_Variable[r"%day%"] = int(date_("day"))
        Addon_Variable[r"%hour%"] = int(time_("hour"))
        Addon_Variable[r"%minute%"] = int(time_("minute"))
        Addon_Variable[r"%second%"] = int(time_("second"))
        #On prend l'instruction actuel du dernier fichier d'instruction
        Instruction = Addon_Variable["INSTRUCTION_FILE_LIST"][-1][Addon_Variable["INSTRUCTION_INDEX"][-1]]
        
        #On verifie si l'indentation correspond
        #Si elle est trop haute (une condition n'est pas passer)
        if Instruction.count("\t") > Addon_Variable["%INDENTATION%"] or Instruction.count("    ") > Addon_Variable["%INDENTATION%"]:
            #Si on a fini le dernier fichier d'instruction
            if len(Addon_Variable["INSTRUCTION_FILE_LIST"][-1]) == Addon_Variable["INSTRUCTION_INDEX"][-1]+1:
                #On enleve le dernier fichier de la liste
                del Addon_Variable["INSTRUCTION_FILE_LIST"][-1]
                #On enleve le dernier index du dernier fichier de la liste
                del Addon_Variable["INSTRUCTION_INDEX"][-1]
            #Si on a encore des fichier
            if Addon_Variable["INSTRUCTION_FILE_LIST"] != []:
                #On augmente de 1 l'index du dernier fichier d'instruction
                Addon_Variable["INSTRUCTION_INDEX"][-1] += 1
            #On passe a la suivante
            continue
        #Sinon Si on est a la de la condition
        elif Instruction.count("\t") < Addon_Variable["%INDENTATION%"]:
            #On baisse l'indentation
            Addon_Variable["%INDENTATION%"] = Instruction.count("\t")
        #On reture les tab et les passage a la ligne de l'instruction
        Instruction = Instruction.replace("\t","").replace("\n","")
        #Si la ligne n'est pas un commentaire
        if Instruction[0] != "#":
            #On genere les tokens de l'instruction
            tokens = Lexer.Gen(Instruction)
            #On separe le sens d'instruction des tokens
            syntaxTree = Parser.parse(tokens)
            #On calcul
            eval = Eval.eval(syntaxTree,Addon_Variable)
            #On execute l'instruction
            Addon_Variable = Execute.execute(eval,Addon_Variable)

        #Si on a fini le dernier fichier d'instruction
        if len(Addon_Variable["INSTRUCTION_FILE_LIST"][-1]) == Addon_Variable["INSTRUCTION_INDEX"][-1]+1:
            #On enleve le dernier fichier de la liste
            del Addon_Variable["INSTRUCTION_FILE_LIST"][-1]
            #On enleve le dernier index du dernier fichier de la liste
            del Addon_Variable["INSTRUCTION_INDEX"][-1]
        #Si on a encore des fichier
        if Addon_Variable["INSTRUCTION_FILE_LIST"] != []:
            #On augmente de 1 l'index du dernier fichier d'instruction
            Addon_Variable["INSTRUCTION_INDEX"][-1] += 1
    return

if __name__ == "__main__":
    while 1:
        #On ecoute
        query = unidecode.unidecode(listen().lower())
        print(query)
        #on cherche pour chaque mot de la query
        for word in query.split(" "):
            File_Name = search_addonFile(word)
            if File_Name == False:
                continue
            else:
                Instructions = read_addonFile(File_Name)
                execute_Instruction(Instructions,query)
                continue