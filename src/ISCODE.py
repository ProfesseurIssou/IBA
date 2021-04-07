import datetime #Date et heure
import locale   #langage du systeme
import getpass  #le nom d'utilisateur

from ISClexer import Lexer
from ISCparser import Parser
from ISCeval import Eval


class ISCODE:
    def __init__(self):
        #le stockage des variable de l'addon
        self.variables = {
            "_INSTRUCTION_INDEX_":[],           #Liste des index au fur et a mesure des fichier [indexFile1,indexFile2]
            "_INSTRUCTION_FILE_LIST_":[],       #Liste des instruction entre chaque fichier et sous fichier [[instructionListFicher1],[InstructionListFichier2]]
            "_INDENTATION_":0,                  #Pour le condition
            "_INDENTATION_TYPE_":None,          #Le caractere d'indentation (changera automatiquement)
            "_LABEL_":[{}],                     #Liste des fichier, et dictionnaire des label (valeur = ligne du label)
            "_CPATH_":"",                       #Dossier de travail
            "_year_":0,
            "_month_":0,
            "_day_":0,
            "_dayName_":"",
            "_hour_":0,
            "_minute_":0,
            "_second_":0,
            "_lang_":"",
            "_username_":"",
        }
    def reset(self):
        """
        Reinitialisation de l'environnement
        """
        #le stockage des variable de l'addon
        self.variables = {
            "_INSTRUCTION_INDEX_":[],           #Liste des index au fur et a mesure des fichier [indexFile1,indexFile2]
            "_INSTRUCTION_FILE_LIST_":[],       #Liste des instruction entre chaque fichier et sous fichier [[instructionListFicher1],[InstructionListFichier2]]
            "_INDENTATION_":0,                  #Pour le condition
            "_INDENTATION_TYPE_":None,          #Le caractere d'indentation
            "_LABEL_":[{}],                     #Liste des fichier, et dictionnaire des label (valeur = ligne du label)
            "_CPATH_":"",                       #Dossier de travail
            "_year_":0,
            "_month_":0,
            "_day_":0,
            "_dayName_":"",
            "_hour_":0,
            "_minute_":0,
            "_second_":0,
            "_lang_":"",
            "_username_":"",
        }

    def executeIbFile(self,FileName,customVariables:dict=None):
        """
        Execute les instruction d'un fichier .ib
        """
        for customVariable in customVariables.keys():   #Pour chaque variable ajouté
            self.variables[customVariable] = customVariables[customVariable]#On ajoute la variable au variable de l'environnement

        Addon_File = open(self.variables["_CPATH_"]+str(FileName),"r")#On ouvre le fichier demandé
        Addon_Instruction = Addon_File.readlines()                  #On lis toute les lignes du fichier
        Addon_File.close()                                          #On ferme le fichier
        
        self.executeInstructionList(Addon_Instruction)              #On lance l'execution des instructions

    def executeInstructionList(self,InstructionsList):
        """
        Execute une liste d'instruction
        """
        self.variables["_INSTRUCTION_INDEX_"] = [0]     #Liste des index au fur et a mesure des fichier [indexFile1,indexFile2]
        self.variables["_INSTRUCTION_FILE_LIST_"] = [InstructionsList]#Liste des instruction entre chaque fichier et sous fichier [[instructionListFicher1],[InstructionListFichier2]]
        self.variables["_INDENTATION_"] = 0             #Pour le condition
        self.variables["_LABEL_"] = [{}]                #Pour les label du fichier

        while self.variables["_INSTRUCTION_FILE_LIST_"] != []:  #Tant qu'on a pas fini tout les fichier
            Instruction = self.variables["_INSTRUCTION_FILE_LIST_"][-1]         #On prend les instructions du dernier fichier
            Instruction = Instruction[self.variables["_INSTRUCTION_INDEX_"][-1]]#On prend l'instruction de la ligne du fichier actuel

            #Creation du type d'indentation
            if (Instruction[0] == " " or Instruction[0] == "\t") and self.variables["_INDENTATION_TYPE_"] == None:#Si l'instruction est dans une condition (indentation) ET que le type d'indentation n'est pas encore définie
                self.variables["_INDENTATION_TYPE_"] = Instruction[0]
                for x in range(1,len(Instruction)):             #Pour chaque caractere de l'instruction
                    if Instruction[x] == Instruction[0]:            #Si le caractere suivant est le même que le premier caractere
                        self.variables["_INDENTATION_TYPE_"] += Instruction[0]#On ajoute le caractere a l'indentation
                    else:                                           #Sinon
                        break                                           #On quitte la boucle
                        
            #Gestion indentation (si on monte passe l'instruction ou on baisse l'indentation)
            if self.variables["_INDENTATION_TYPE_"] != None:    #Si le type d'indentation est deja definie (si on a deja rencontré une condition)
                if Instruction.count(self.variables["_INDENTATION_TYPE_"]) > self.variables["_INDENTATION_"]:   #Si la ligne est dans une condition dans laquelle on est pas entré
                    if len(self.variables["_INSTRUCTION_FILE_LIST_"][-1]) == self.variables["_INSTRUCTION_INDEX_"][-1]+1:   #Si on a fini le dernier fichier d'instruction
                        del self.variables["_INSTRUCTION_FILE_LIST_"][-1]   #On supprime le dernier fichier de la liste
                        del self.variables["_INSTRUCTION_INDEX_"][-1]       #On supprime la derniere index de l'ancien fichier de la liste
                        del self.variables["_LABEL_"][-1]                   #On supprime les labels de l'ancien fichier
                    if self.variables["_INSTRUCTION_FILE_LIST_"] != []: #Si il reste encore des fichier dans la liste
                        self.variables["_INSTRUCTION_INDEX_"][-1] += 1      #On passe l'index du dernier fichier a +1 (pour ne pas ré executé le goto)
                    continue    #On passe au suivant
                elif Instruction.count(self.variables["_INDENTATION_TYPE_"]) < self.variables["_INDENTATION_"]: #Si on sort d'une condition
                    self.variables["_INDENTATION_"] = Instruction.count(self.variables["_INDENTATION_TYPE_"])       #On passe le nombre d'indentation au nombre de tabulation
                Instruction = Instruction.replace(self.variables["_INDENTATION_TYPE_"],"")  #On retire les indentation
            
            #Clean l'instruction
            if Instruction[-1] == "\n":                                                 #Si il y a un retour a la ligne a la fin de l'instruction
                Instruction = Instruction[:-1]                                              #On supprime le dernier caractere
            if Instruction != "" and Instruction[0] != "#":                 #Si la ligne n'est pas un commentaire ni vide
                self.execute(Instruction)                                       #On execute l'instruction

            #Passage a l'instruction suivant ou retour au fichier parent
            while self.variables["_INSTRUCTION_FILE_LIST_"] != [] and len(self.variables["_INSTRUCTION_FILE_LIST_"][-1]) == self.variables["_INSTRUCTION_INDEX_"][-1]+1:#Tant que la liste n'est pas vide ET pour chaque fichier parents, on est a la derniere instruction
                del self.variables["_INSTRUCTION_FILE_LIST_"][-1]   #On supprime le dernier fichier de la liste
                del self.variables["_INSTRUCTION_INDEX_"][-1]       #On supprime la derniere index de l'ancien fichier de la liste
                del self.variables["_LABEL_"][-1]                   #On supprime les labels de l'ancien fichier
            if self.variables["_INSTRUCTION_FILE_LIST_"] != []: #Si il reste encore des fichier dans la liste
                self.variables["_INSTRUCTION_INDEX_"][-1] += 1      #On passe l'index du dernier fichier a +1 (pour ne pas ré executé le goto)

    def execute(self,Instruction):
        """
        Execute une seul instruction
        """
        ####SET DEFAULT VARIABLES####
        self.variables["_year_"] = datetime.datetime.now().year
        self.variables["_month_"] = datetime.datetime.now().month
        self.variables["_day_"] = datetime.datetime.now().day
        self.variables["_dayName_"] = datetime.datetime.now().strftime("%A")
        self.variables["_hour_"] = datetime.datetime.now().hour
        self.variables["_minute_"] = datetime.datetime.now().minute
        self.variables["_second_"] = datetime.datetime.now().second
        self.variables["_lang_"] = locale.getdefaultlocale()[0]
        self.variables["_username_"] = getpass.getuser()
        #############################

        ####ANALYSE LEXICAL(Lexer)####
        #On decoupe l'instruction pour chaque jeux de caractere (lettre, nombre, egal)
        tokenList = Lexer(Instruction)
        # print(tokenList)
        ####ANALYSE SYNTAXIQUE(Parser)####
        #Verifier la grammaire (SyntaxTree)
        syntaxTree = Parser(tokenList)
        # print(syntaxTree)
        ####EVALUATION####
        self.variables = Eval(syntaxTree,self.variables)