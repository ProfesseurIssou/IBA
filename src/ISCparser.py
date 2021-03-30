#pip install SpeechRecognition,PyAudio
import speech_recognition
import os
import time
import pyttsx3 #Text to speech
import json
engine = pyttsx3.init()#on init le convertisseur text->vocal

#Token a ignoré
IGNORE = [
    "TokSpace",
    "TokColon"
]

class Node:
    def __init__(self,tokenList):
        self.NodeRule = None        #La regle du noeud actuel
        self.Value = None           #Valeur du noeud
        self.SubNodeList = []       #Liste des sous noeud
        self.scanType(tokenList)    #On scan la liste des token pour faire des sous noeud
        return

    def scanType(self,tokenList):   #On verifie quel type de noeud sa sera (print, add, speak, ...)
        # print(tokenList)

        instructionsList = {    #LISTE DES INSTRUCTION AVEC LEUR FONCTION DE TRAITEMENT
            #Instruction qui execute
            "TokPrint":self.PRINT,
            "TokAssign":self.SET,
            "TokIf":self.IF,
            "TokSpeak":self.SPEAK,
            "TokGoto":self.GOTO,
            "TokWait":self.WAIT,
            "TokExecute":self.RUN,
            "TokOpenBrowser":self.OPENBROWSER,
            "TokDbSave":self.DBSAVE,
            "TokDbDel":self.DBDEL,

            #Condition
            "TokEqual":self.EQUAL,
            "TokNotEqual":self.NOTEQUAL,
            "TokLessEqual":self.LESSEQUAL,
            "TokGreaterEqual":self.GREATEREGAL,
            "TokLess":self.LESS,
            "TokGreater":self.GREATER,
            "TokAnd":self.AND,
            "TokOr":self.OR,
            "TokNot":self.NOT,
            "TokIn":self.IN,

            #Operateur
            "TokPlus":self.ADD,
            "TokMinus":self.SUB,
            "TokStar":self.MUL,
            "TokSlash":self.DIV,

            #Instruction qui retourne une valeur
            "TokListen":self.LISTEN,
            "TokToStr":self.TOSTR,
            "TokToFloat":self.TOFLOAT,
            "TokToInt":self.TOINT,
            "TokType":self.TYPE,
            "TokLen":self.LENGTH,
            "TokDbLoad":self.DBLOAD,
            "TokDbExist":self.DBEXIST,

            #Priority
            "TokOpenParen":self.PRIORITY,

            #Liste
            "TokOpenBrace":self.LISTDATA,
            "TokOpenBracket":self.LISTSELECTOR,

            #Type de données
            "TokFalse":self.FALSE,
            "TokTrue":self.TRUE,
            "TokNone":self.NONE,
            "TokNegativeNumber":self.NEGNUMBER,
            "TokInt":self.INT,
            "TokFloat":self.FLOAT,
            "TokString":self.STRING,
            "TokVariable":self.VARIABLE,
            "TokStrType":self.STRTYPE,
            "TokIntType":self.INTTYPE,
            "TokFloatType":self.FLOATTYPE,
            "TokBoolType":self.BOOLTYPE,
            "TokListType":self.LISTTYPE,
        }

        #Pour eviter de prendre des instruction dans des sous priorité, on compte le nombre de parenthese (que si notre regle actuel n'est pas celle des parenthese)
        nbSubParenthesis = 0                #Nombre de sous parenthese
        nbSubBrace = 0                      #Nombre de sous accolade (pour les listes)
        nbSubBracket = 0                    #Nombre de sous crochet (pour les selecteur de listes)
        resetScan = False                   #Permet de recommencer les priorités si on a trouver quelque chose
        while tokenList != []:              #Tant qu'il nous reste des token a traiter
            resetScan = False                   #Nouveau scan depuis le début
            for instruction in instructionsList.keys():#Pour chaque instruction
                nbSubParenthesis = 0                #On remet le compteur du nombre de parenthese a 0
                nbSubBrace = 0                      #On remet le compteur du nombre d'accolade a 0
                for x,tok in enumerate(tokenList):      #Pour chaque token de la liste
                    if instruction != 'TokOpenParen' and tok[0] == "TokOpenParen":#Si on est pas la regle sur les priorité par parenthese et que le token actuel est une ouverture de parenthese
                        nbSubParenthesis += 1                   #On augmente de 1 le nombre de sous parenthese
                    if tok[0] == "TokCloseParen":           #Si le token actuel est une fermeture de parenthese
                        nbSubParenthesis -= 1                   #On baisse de 1 le nombre de sous parenthese
                    if instruction != 'TokOpenBrace' and tok[0] == "TokOpenBrace":#Si on est pas la regle sur les priorité par accolade(liste) et que le token actuel est une ouverture d'accolade
                        nbSubBrace += 1                         #On augmente de 1 le nombre de sous accolade
                    if tok[0] == "TokCloseBrace":           #Si le token actuel est une fermeture d'accolade
                        nbSubBrace -= 1                         #On baisse de 1 le nombre de sous accolade
                    if instruction != 'TokOpenBracket' and tok[0] == "TokOpenBracket":#Si on est pas la regle sur les priorité par crochet(selecteur liste) et que le token actuel est une ouverture de crochet
                        nbSubBracket += 1                         #On augmente de 1 le nombre de sous crochet
                    if tok[0] == "TokCloseBracket":           #Si le token actuel est une fermeture de crochet
                        nbSubBracket -= 1                         #On baisse de 1 le nombre de sous crochet
                    if instruction == tok[0] and nbSubParenthesis == 0 and nbSubBrace == 0 and nbSubBracket == 0:#Si le token correspond ET qu'on est pas dans une sous priorité ET qu'on est pas dans une valeur de liste ET qu'on n'est pas dans un selecteur de liste
                        tokenList = instructionsList[instruction](tokenList,x)#On appelle sa fonction de traitement (qui va aussi supprimer les tokens qu'elle a utiliser pour traiter le reste)
                        resetScan = True                        #On a trouvé une instruction
                        break                                   #On veux recommencer le scan
                if resetScan:                               #Si on a trouvé une instruction
                    break                                       #On veux recommencer le scan
        return


    #####INSTRUCTION QUI EXECUTE#####
    def PRINT(self,tokenList,tokPos):
        self.NodeRule = "PRINT"             #On definie le noeud actuel comme un print
        subNodeTokens = tokenList[2:-1]     #On prend les tokens entre parenthese pour le sous noeud
        self.SubNodeList.append(Node(subNodeTokens))#On cree un sous noeud avec les tokens pour le sous noeud
        return []                           #On efface tout les token car il n'est pas cense en rester
    def SET(self,tokenList,tokPos):
        self.NodeRule = "SET"               #On definie le noeud actuel comme un set
        self.Value = tokenList[0][1]        #On prend la variable dans le quel il faut stoquer l'info
        subNodeTokens = tokenList[2:]       #On prend les tokens apres le =
        self.SubNodeList.append(Node(subNodeTokens))#On cree un sous noeud avec les tokens pour le sous noeud
        return []                           #On efface tout les token car il n'est pas cense en rester
    def IF(self,tokenList,tokPos):
        self.NodeRule = "IF"                #On definie le noeud actuel comme une condition
        subNodeTokens = tokenList[1:]       #On prend les tokens apres if
        self.SubNodeList.append(Node(subNodeTokens))#On cree un sous noeud avec les tokens pour le sous noeud
        return []                           #On efface tout les token car il n'est pas cense en rester
    def SPEAK(self,tokenList,tokPos):
        self.NodeRule = "SPEAK"             #On definie le noeud actuel comme un speak
        subNodeTokens = tokenList[2:-1]     #On prend les tokens entre les parenthese
        self.SubNodeList.append(Node(subNodeTokens))#On cree un sous noeud avec les tokens pour le sous noeud
        return []                           #On efface tout les token car il n'est pas cense en rester
    def GOTO(self,tokenList,tokPos):
        self.NodeRule = "GOTO"              #On definie le noeud actuel comme un goto
        subNodeTokens = tokenList[2:-1]     #On prend les tokens entre les parenthese
        self.SubNodeList.append(Node(subNodeTokens))#On cree un sous noeud avec les tokens pour le sous noeud
        return []                           #On efface tout les token car il n'est pas cense en rester
    def WAIT(self,tokenList,tokPos):
        self.NodeRule = "WAIT"              #On definie le noeud actuel
        subNodeTokens = tokenList[2:-1]     #On prend les tokens entre les parenthese
        self.SubNodeList.append(Node(subNodeTokens))#On cree un sous noeud avec les tokens pour le sous noeud
        return []                           #On efface tout les token car il n'est pas cense en rester
    def RUN(self,tokenList,tokPos):
        self.NodeRule = "RUN"               #On definie le noeud actuel
        subNodeTokens = tokenList[2:-1]     #On prend les tokens entre les parenthese
        self.SubNodeList.append(Node(subNodeTokens))#On cree un sous noeud avec les tokens pour le sous noeud
        return []                           #On efface tout les token car il n'est pas cense en rester
    def OPENBROWSER(self,tokenList,tokPos):
        self.NodeRule = "OPENBROWSER"       #On definie le noeud actuel
        subNodeTokens = tokenList[2:-1]     #On prend le contenue entre les parenthese

        #On separe par la virgule
        nbSubBrace = 0                                  #Nombre de sous accolade
        nbSubBracket = 0                                #Nombre de sous crochet
        nbSubParenthesis = 0                            #Nombre de sous parenthese
        firstPos = 0                                    #Position du premier token de la partie (entre les virgule)
        for x,token in enumerate(subNodeTokens):        #Pour chaque token de la liste des sous tokens
            if token[0] == "TokOpenBrace":                  #Si le token actuel est une ouverture d'accolade
                nbSubBrace += 1                                 #On ajoute 1 au nombre d'accolade
            if token[0] == "TokCloseBrace":                 #Si le token actuel est une fermeture d'accolade
                nbSubBrace -= 1                                 #On retire 1 au nombre d'accolade
            if token[0] == "TokOpenBracket":                #Si le token actuel est une ouverture de crochet
                nbSubBracket += 1                               #On ajoute 1 au nombre de crochet
            if token[0] == "TokCloseBracket":               #Si le token actuel est une fermeture de crochet
                nbSubBracket -= 1                               #On retire 1 au nombre de crochet
            if token[0] == "TokOpenParen":                  #Si le token actuel est une ouverture de parenthese
                nbSubParenthesis += 1                           #On ajoute 1 au nombre de parenthese
            if token[0] == "TokCloseParen":                 #Si le token actuel est une fermeture de parenthese
                nbSubParenthesis -= 1                           #On retire 1 au nombre de parenthese
            if token[0] == "TokComma" and nbSubBrace == 0 and nbSubBracket == 0 and nbSubParenthesis == 0:#Si le token actuel est une virgule ET qu'on n'est pas dans une sous liste ET qu'on n'est pas dans un selecteur de liste ET qu'on n'est pas dans une sous parenthese
                self.SubNodeList.append(Node(subNodeTokens[firstPos:x]))#On cree le noeud du contenue entre les virgule
                firstPos = x+1                                   #On se place apres la virgule pour la prochaine partie

        self.SubNodeList.append(Node(subNodeTokens[firstPos:]))#On cree un sous noeud avec les tokens pour le sous noeud
        return []                           #On efface tout les token car il n'est pas cense en rester
    def DBSAVE(self,tokenList,tokPos):
        self.NodeRule = "DBSAVE"            #On definie le noeud actuel
        subNodeTokens = tokenList[2:-1]     #On prend le contenue entre les parenthese

        #On separe par la virgule
        nbSubBrace = 0                                  #Nombre de sous accolade
        nbSubBracket = 0                                #Nombre de sous crochet
        nbSubParenthesis = 0                            #Nombre de sous parenthese
        firstPos = 0                                    #Position du premier token de la partie (entre les virgule)
        for x,token in enumerate(subNodeTokens):        #Pour chaque token de la liste des sous tokens
            if token[0] == "TokOpenBrace":                  #Si le token actuel est une ouverture d'accolade
                nbSubBrace += 1                                 #On ajoute 1 au nombre d'accolade
            if token[0] == "TokCloseBrace":                 #Si le token actuel est une fermeture d'accolade
                nbSubBrace -= 1                                 #On retire 1 au nombre d'accolade
            if token[0] == "TokOpenBracket":                #Si le token actuel est une ouverture de crochet
                nbSubBracket += 1                               #On ajoute 1 au nombre de crochet
            if token[0] == "TokCloseBracket":               #Si le token actuel est une fermeture de crochet
                nbSubBracket -= 1                               #On retire 1 au nombre de crochet
            if token[0] == "TokOpenParen":                  #Si le token actuel est une ouverture de parenthese
                nbSubParenthesis += 1                           #On ajoute 1 au nombre de parenthese
            if token[0] == "TokCloseParen":                 #Si le token actuel est une fermeture de parenthese
                nbSubParenthesis -= 1                           #On retire 1 au nombre de parenthese
            if token[0] == "TokComma" and nbSubBrace == 0 and nbSubBracket == 0 and nbSubParenthesis == 0:#Si le token actuel est une virgule ET qu'on n'est pas dans une sous liste ET qu'on n'est pas dans un selecteur de liste ET qu'on n'est pas dans une sous parenthese
                self.SubNodeList.append(Node(subNodeTokens[firstPos:x]))#On cree le noeud du contenue entre les virgule
                firstPos = x+1                                   #On se place apres la virgule pour la prochaine partie

        self.SubNodeList.append(Node(subNodeTokens[firstPos:]))#On cree un sous noeud avec les tokens pour le sous noeud
        return []                           #On efface tout les token car il n'est pas cense en rester
    def DBDEL(self,tokenList,tokPos):
        self.NodeRule = "DBDEL"             #On definie le noeud actuel
        subNodeTokens = tokenList[2:-1]     #On prend les tokens entre les parenthese
        self.SubNodeList.append(Node(subNodeTokens))#On cree un sous noeud avec les tokens pour le sous noeud
        return []                           #On efface tout les token car il n'est pas cense en rester
    #################################

    #####OPERATEUR#####
    def ADD(self,tokenList,tokPos):
        self.NodeRule = "ADD"                           #On definie la regle du noeud actuel
        subNodeTokens1 = tokenList[:tokPos]             #On prend la premiere partie de l'operation
        subNodeTokens2 = tokenList[tokPos+1:]           #On prend la deuxieme partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens1))   #On cree le noeud de la premiere partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens2))   #On cree le noeud de la deuxieme partie de l'operation
        return []  
    def SUB(self,tokenList,tokPos):
        self.NodeRule = "SUB"                           #On definie la regle du noeud actuel
        subNodeTokens1 = tokenList[:tokPos]             #On prend la premiere partie de l'operation
        subNodeTokens2 = tokenList[tokPos+1:]           #On prend la deuxieme partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens1))   #On cree le noeud de la premiere partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens2))   #On cree le noeud de la deuxieme partie de l'operation
        return []  
    def MUL(self,tokenList,tokPos):
        self.NodeRule = "MUL"                           #On definie la regle du noeud actuel
        subNodeTokens1 = tokenList[:tokPos]             #On prend la premiere partie de l'operation
        subNodeTokens2 = tokenList[tokPos+1:]           #On prend la deuxieme partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens1))   #On cree le noeud de la premiere partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens2))   #On cree le noeud de la deuxieme partie de l'operation
        return []                                       #On vide tout car il n'est pas censer rester de token
    def DIV(self,tokenList,tokPos):
        self.NodeRule = "DIV"                           #On definie la regle du noeud actuel
        subNodeTokens1 = tokenList[:tokPos]             #On prend la premiere partie de l'operation
        subNodeTokens2 = tokenList[tokPos+1:]           #On prend la deuxieme partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens1))   #On cree le noeud de la premiere partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens2))   #On cree le noeud de la deuxieme partie de l'operation
        return []                                       #On vide tout car il n'est pas censer rester de token
    ###################

    #####CONDITION#####
    def EQUAL(self,tokenList,tokPos):
        self.NodeRule = "EQUAL"                         #On definie la regle du noeud actuel
        subNodeTokens1 = tokenList[:tokPos]             #On prend la premiere partie de l'operation
        subNodeTokens2 = tokenList[tokPos+1:]           #On prend la deuxieme partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens1))   #On cree le noeud de la premiere partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens2))   #On cree le noeud de la deuxieme partie de l'operation
        return []  
    def NOTEQUAL(self,tokenList,tokPos):
        self.NodeRule = "NOTEQUAL"                      #On definie la regle du noeud actuel
        subNodeTokens1 = tokenList[:tokPos]             #On prend la premiere partie de l'operation
        subNodeTokens2 = tokenList[tokPos+1:]           #On prend la deuxieme partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens1))   #On cree le noeud de la premiere partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens2))   #On cree le noeud de la deuxieme partie de l'operation
        return []  
    def LESSEQUAL(self,tokenList,tokPos):
        self.NodeRule = "LESSEQUAL"                     #On definie la regle du noeud actuel
        subNodeTokens1 = tokenList[:tokPos]             #On prend la premiere partie de l'operation
        subNodeTokens2 = tokenList[tokPos+1:]           #On prend la deuxieme partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens1))   #On cree le noeud de la premiere partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens2))   #On cree le noeud de la deuxieme partie de l'operation
        return []  
    def GREATEREGAL(self,tokenList,tokPos):
        self.NodeRule = "GREATEREGAL"                   #On definie la regle du noeud actuel
        subNodeTokens1 = tokenList[:tokPos]             #On prend la premiere partie de l'operation
        subNodeTokens2 = tokenList[tokPos+1:]           #On prend la deuxieme partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens1))   #On cree le noeud de la premiere partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens2))   #On cree le noeud de la deuxieme partie de l'operation
        return []  
    def LESS(self,tokenList,tokPos):
        self.NodeRule = "LESS"                          #On definie la regle du noeud actuel
        subNodeTokens1 = tokenList[:tokPos]             #On prend la premiere partie de l'operation
        subNodeTokens2 = tokenList[tokPos+1:]           #On prend la deuxieme partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens1))   #On cree le noeud de la premiere partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens2))   #On cree le noeud de la deuxieme partie de l'operation
        return []  
    def GREATER(self,tokenList,tokPos):
        self.NodeRule = "GREATER"                       #On definie la regle du noeud actuel
        subNodeTokens1 = tokenList[:tokPos]             #On prend la premiere partie de l'operation
        subNodeTokens2 = tokenList[tokPos+1:]           #On prend la deuxieme partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens1))   #On cree le noeud de la premiere partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens2))   #On cree le noeud de la deuxieme partie de l'operation
        return []  
    def AND(self,tokenList,tokPos):
        self.NodeRule = "AND"                           #On definie la regle du noeud actuel
        subNodeTokens1 = tokenList[:tokPos]             #On prend la premiere partie de l'operation
        subNodeTokens2 = tokenList[tokPos+1:]           #On prend la deuxieme partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens1))   #On cree le noeud de la premiere partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens2))   #On cree le noeud de la deuxieme partie de l'operation
        return []  
    def OR(self,tokenList,tokPos):
        self.NodeRule = "OR"                            #On definie la regle du noeud actuel
        subNodeTokens1 = tokenList[:tokPos]             #On prend la premiere partie de l'operation
        subNodeTokens2 = tokenList[tokPos+1:]           #On prend la deuxieme partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens1))   #On cree le noeud de la premiere partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens2))   #On cree le noeud de la deuxieme partie de l'operation
        return []  
    def NOT(self,tokenList,tokPos):
        self.NodeRule = "NOT"                           #On definie la regle du noeud actuel
        #On recherhe la fermeture de parenthese
        nbSubParenthesis = 0                            #Nombre de sous parenthese (on commence a la position de la premiere parenthese dans la liste des tokens pour ne pas compté l'ouverture de la principale, quand cette variable arrive a -1, c'est que c'est cette parenthese)
        posCloseParen = tokPos+1                        #Position de la fermeture de parenthese actuel
        while nbSubParenthesis != -1:                   #Tant qu'on n'a pas trouver la fermeture de parenthese
            posCloseParen += 1                              #Position suivante
            if tokenList[posCloseParen][0]=="TokOpenParen": #Si il y a une sous parenthese
                nbSubParenthesis += 1                           #On attend une fermeture en plus
            if tokenList[posCloseParen][0]=="TokCloseParen":#Si il y a une fermeture d'une parenthese
                nbSubParenthesis -= 1                           #On ferme la parenthese actuel
        subNodeTokens = tokenList[2:posCloseParen]      #On prend le contenue entre les parenthese
        self.SubNodeList.append(Node(subNodeTokens))    #On cree le noeud du contenue de la parenthese
        return []  
    def IN(self,tokenList,tokPos):
        self.NodeRule = "IN"                            #On definie la regle du noeud actuel
        subNodeTokens1 = tokenList[:tokPos]             #On prend la premiere partie de l'operation
        subNodeTokens2 = tokenList[tokPos+1:]           #On prend la deuxieme partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens1))   #On cree le noeud de la premiere partie de l'operation
        self.SubNodeList.append(Node(subNodeTokens2))   #On cree le noeud de la deuxieme partie de l'operation
        return []  
    ###################

    #####INSTRUCTION QUI RETOURNE UNE VALEUR#####
    def LISTEN(self,tokenList,tokPos):
        self.NodeRule = "LISTEN"                #On definie le noeud actuel comme une ecoute
        return []
    def TOSTR(self,tokenList,tokPos):
        self.NodeRule = "TOSTR"                 #On definie le noeud actuel comme un toStr
        #On recherhe la fermeture de parenthese
        nbSubParenthesis = 0                            #Nombre de sous parenthese (on commence a la position de la premiere parenthese dans la liste des tokens pour ne pas compté l'ouverture de la principale, quand cette variable arrive a -1, c'est que c'est cette parenthese)
        posCloseParen = tokPos+1                        #Position de la fermeture de parenthese actuel
        while nbSubParenthesis != -1:                   #Tant qu'on n'a pas trouver la fermeture de parenthese
            posCloseParen += 1                              #Position suivante
            if tokenList[posCloseParen][0]=="TokOpenParen": #Si il y a une sous parenthese
                nbSubParenthesis += 1                           #On attend une fermeture en plus
            if tokenList[posCloseParen][0]=="TokCloseParen":#Si il y a une fermeture d'une parenthese
                nbSubParenthesis -= 1                           #On ferme la parenthese actuel
        subNodeTokens = tokenList[tokPos+2:posCloseParen]#On prend le contenue entre les parenthese
        self.SubNodeList.append(Node(subNodeTokens))    #On cree le noeud du contenue de la parenthese
        return tokenList[:tokPos]+tokenList[posCloseParen+1:]#On retourne tout les tokens qui reste avant et apres la fermeture de parenthese
    def TOFLOAT(self,tokenList,tokPos):
        self.NodeRule = "TOFLOAT"               #On definie le noeud actuel comme un toFloat
        #On recherhe la fermeture de parenthese
        nbSubParenthesis = 0                            #Nombre de sous parenthese (on commence a la position de la premiere parenthese dans la liste des tokens pour ne pas compté l'ouverture de la principale, quand cette variable arrive a -1, c'est que c'est cette parenthese)
        posCloseParen = tokPos+1                        #Position de la fermeture de parenthese actuel
        while nbSubParenthesis != -1:                   #Tant qu'on n'a pas trouver la fermeture de parenthese
            posCloseParen += 1                              #Position suivante
            if tokenList[posCloseParen][0]=="TokOpenParen": #Si il y a une sous parenthese
                nbSubParenthesis += 1                           #On attend une fermeture en plus
            if tokenList[posCloseParen][0]=="TokCloseParen":#Si il y a une fermeture d'une parenthese
                nbSubParenthesis -= 1                           #On ferme la parenthese actuel
        subNodeTokens = tokenList[tokPos+2:posCloseParen]#On prend le contenue entre les parenthese
        self.SubNodeList.append(Node(subNodeTokens))    #On cree le noeud du contenue de la parenthese
        return tokenList[:tokPos]+tokenList[posCloseParen+1:]#On retourne tout les tokens qui reste avant et apres la fermeture de parenthese
    def TOINT(self,tokenList,tokPos):
        self.NodeRule = "TOINT"                 #On definie le noeud actuel comme un toInt
        #On recherhe la fermeture de parenthese
        nbSubParenthesis = 0                            #Nombre de sous parenthese (on commence a la position de la premiere parenthese dans la liste des tokens pour ne pas compté l'ouverture de la principale, quand cette variable arrive a -1, c'est que c'est cette parenthese)
        posCloseParen = tokPos+1                        #Position de la fermeture de parenthese actuel
        while nbSubParenthesis != -1:                   #Tant qu'on n'a pas trouver la fermeture de parenthese
            posCloseParen += 1                              #Position suivante
            if tokenList[posCloseParen][0]=="TokOpenParen": #Si il y a une sous parenthese
                nbSubParenthesis += 1                           #On attend une fermeture en plus
            if tokenList[posCloseParen][0]=="TokCloseParen":#Si il y a une fermeture d'une parenthese
                nbSubParenthesis -= 1                           #On ferme la parenthese actuel
        subNodeTokens = tokenList[tokPos+2:posCloseParen]#On prend le contenue entre les parenthese
        self.SubNodeList.append(Node(subNodeTokens))    #On cree le noeud du contenue de la parenthese
        return tokenList[:tokPos]+tokenList[posCloseParen+1:]#On retourne tout les tokens qui reste avant et apres la fermeture de parenthese
    def TYPE(self,tokenList,tokPos):
        self.NodeRule = "TYPE"                  #On definie le noeud actuel comme un type de variable
        #On recherhe la fermeture de parenthese
        nbSubParenthesis = 0                            #Nombre de sous parenthese (on commence a la position de la premiere parenthese dans la liste des tokens pour ne pas compté l'ouverture de la principale, quand cette variable arrive a -1, c'est que c'est cette parenthese)
        posCloseParen = tokPos+1                        #Position de la fermeture de parenthese actuel
        while nbSubParenthesis != -1:                   #Tant qu'on n'a pas trouver la fermeture de parenthese
            posCloseParen += 1                              #Position suivante
            if tokenList[posCloseParen][0]=="TokOpenParen": #Si il y a une sous parenthese
                nbSubParenthesis += 1                           #On attend une fermeture en plus
            if tokenList[posCloseParen][0]=="TokCloseParen":#Si il y a une fermeture d'une parenthese
                nbSubParenthesis -= 1                           #On ferme la parenthese actuel
        subNodeTokens = tokenList[tokPos+2:posCloseParen]#On prend le contenue entre les parenthese
        self.SubNodeList.append(Node(subNodeTokens))    #On cree le noeud du contenue de la parenthese
        return tokenList[:tokPos]+tokenList[posCloseParen+1:]#On retourne tout les tokens qui reste avant et apres la fermeture de parenthese
    def LENGTH(self,tokenList,tokPos):
        self.NodeRule = "LENGTH"                #On definie le noeud actuel
        #On recherhe la fermeture de parenthese
        nbSubParenthesis = 0                            #Nombre de sous parenthese (on commence a la position de la premiere parenthese dans la liste des tokens pour ne pas compté l'ouverture de la principale, quand cette variable arrive a -1, c'est que c'est cette parenthese)
        posCloseParen = tokPos+1                        #Position de la fermeture de parenthese actuel
        while nbSubParenthesis != -1:                   #Tant qu'on n'a pas trouver la fermeture de parenthese
            posCloseParen += 1                              #Position suivante
            if tokenList[posCloseParen][0]=="TokOpenParen": #Si il y a une sous parenthese
                nbSubParenthesis += 1                           #On attend une fermeture en plus
            if tokenList[posCloseParen][0]=="TokCloseParen":#Si il y a une fermeture d'une parenthese
                nbSubParenthesis -= 1                           #On ferme la parenthese actuel
        subNodeTokens = tokenList[tokPos+2:posCloseParen]#On prend le contenue entre les parenthese
        self.SubNodeList.append(Node(subNodeTokens))    #On cree le noeud du contenue de la parenthese
        return tokenList[:tokPos]+tokenList[posCloseParen+1:]#On retourne tout les tokens qui reste avant et apres la fermeture de parenthese
    def DBLOAD(self,tokenList,tokPos):
        self.NodeRule = "DBLOAD"                #On definie le noeud actuel comme un chargement de valeur
        #On recherhe la fermeture de parenthese
        nbSubParenthesis = 0                            #Nombre de sous parenthese (on commence a la position de la premiere parenthese dans la liste des tokens pour ne pas compté l'ouverture de la principale, quand cette variable arrive a -1, c'est que c'est cette parenthese)
        posCloseParen = tokPos+1                        #Position de la fermeture de parenthese actuel
        while nbSubParenthesis != -1:                   #Tant qu'on n'a pas trouver la fermeture de parenthese
            posCloseParen += 1                              #Position suivante
            if tokenList[posCloseParen][0]=="TokOpenParen": #Si il y a une sous parenthese
                nbSubParenthesis += 1                           #On attend une fermeture en plus
            if tokenList[posCloseParen][0]=="TokCloseParen":#Si il y a une fermeture d'une parenthese
                nbSubParenthesis -= 1                           #On ferme la parenthese actuel
        subNodeTokens = tokenList[tokPos+2:posCloseParen]#On prend le contenue entre les parenthese
        self.SubNodeList.append(Node(subNodeTokens))    #On cree le noeud du contenue de la parenthese
        return tokenList[:tokPos]+tokenList[posCloseParen+1:]#On retourne tout les tokens qui reste avant et apres la fermeture de parenthese
    def DBEXIST(self,tokenList,tokPos):
        self.NodeRule = "DBEXIST"                   #On definie le noeud actuel comme un check de valeur
        #On recherhe la fermeture de parenthese
        nbSubParenthesis = 0                            #Nombre de sous parenthese (on commence a la position de la premiere parenthese dans la liste des tokens pour ne pas compté l'ouverture de la principale, quand cette variable arrive a -1, c'est que c'est cette parenthese)
        posCloseParen = tokPos+1                        #Position de la fermeture de parenthese actuel
        while nbSubParenthesis != -1:                   #Tant qu'on n'a pas trouver la fermeture de parenthese
            posCloseParen += 1                              #Position suivante
            if tokenList[posCloseParen][0]=="TokOpenParen": #Si il y a une sous parenthese
                nbSubParenthesis += 1                           #On attend une fermeture en plus
            if tokenList[posCloseParen][0]=="TokCloseParen":#Si il y a une fermeture d'une parenthese
                nbSubParenthesis -= 1                           #On ferme la parenthese actuel
        subNodeTokens = tokenList[tokPos+2:posCloseParen]#On prend le contenue entre les parenthese
        self.SubNodeList.append(Node(subNodeTokens))    #On cree le noeud du contenue de la parenthese
        return tokenList[:tokPos]+tokenList[posCloseParen+1:]#On retourne tout les tokens qui reste avant et apres la fermeture de parenthese
    #############################################

    #####PRIORITY#####
    def PRIORITY(self,tokenList,tokPos):
        self.NodeRule = "PRIORITY"                      #On definie la regle du noeud actuel
        #On recherhe la fermeture de parenthese
        nbSubParenthesis = 0                            #Nombre de sous parenthese (on commence a 1 dans la liste des tokens pour ne pas compté l'ouverture de la principale, quand cette variable arrive a -1, c'est que c'est cette parenthese)
        posCloseParen = tokPos+0                        #Position de la fermeture de parenthese actuel
        while nbSubParenthesis != -1:                   #Tant qu'on n'a pas trouver la fermeture de parenthese
            posCloseParen += 1                              #Position suivante
            if tokenList[posCloseParen][0]=="TokOpenParen": #Si il y a une sous parenthese
                nbSubParenthesis += 1                           #On attend une fermeture en plus
            if tokenList[posCloseParen][0]=="TokCloseParen":#Si il y a une fermeture d'une parenthese
                nbSubParenthesis -= 1                           #On ferme la parenthese actuel
        subNodeTokens = tokenList[tokPos+1:posCloseParen]#On prend le contenue entre les parenthese
        self.SubNodeList.append(Node(subNodeTokens))    #On cree le noeud du contenue de la parenthese
        return tokenList[:tokPos]+tokenList[posCloseParen+1:]#On retourne tout les tokens qui reste apres la fermeture de parenthese
    ##################

    #####LIST#####
    def LISTDATA(self,tokenList,tokPos):
        self.NodeRule = "LISTDATA"                      #On definie la regle du noeud actuel
        #On recherhe la fermeture d'accolade
        nbSubBrace = 0                                  #Nombre de sous accolade (on commence a 1 dans la liste des tokens pour ne pas compté l'ouverture de la principale, quand cette variable arrive a -1, c'est que c'est cette parenthese)
        posCloseBrace = tokPos+0                        #Position de la fermeture d'accolade actuel
        while nbSubBrace != -1:                         #Tant qu'on n'a pas trouver la fermeture d'accolade
            posCloseBrace += 1                              #Position suivante
            if tokenList[posCloseBrace][0]=="TokOpenBrace": #Si il y a une sous accolade
                nbSubBrace += 1                                 #On attend une fermeture en plus
            if tokenList[posCloseBrace][0]=="TokCloseBrace":#Si il y a une fermeture d'une accolade
                nbSubBrace -= 1                                 #On ferme l'accolade actuel
        subNodeTokens = tokenList[tokPos+1:posCloseBrace]#On prend le contenue entre les accolades

        #On separe par la virgule
        nbSubBrace = 0                                  #Nombre de sous accolade
        nbSubBracket = 0                                #Nombre de sous crochet
        nbSubParenthesis = 0                            #Nombre de sous parenthese
        firstPos = 0                                    #Position du premier token de la partie (entre les virgule)
        for x,token in enumerate(subNodeTokens):        #Pour chaque token de la liste des sous tokens
            if token[0] == "TokOpenBrace":                  #Si le token actuel est une ouverture d'accolade
                nbSubBrace += 1                                 #On ajoute 1 au nombre d'accolade
            if token[0] == "TokCloseBrace":                 #Si le token actuel est une fermeture d'accolade
                nbSubBrace -= 1                                 #On retire 1 au nombre d'accolade
            if token[0] == "TokOpenBracket":                #Si le token actuel est une ouverture de crochet
                nbSubBracket += 1                               #On ajoute 1 au nombre de crochet
            if token[0] == "TokCloseBracket":               #Si le token actuel est une fermeture de crochet
                nbSubBracket -= 1                               #On retire 1 au nombre de crochet
            if token[0] == "TokOpenParen":                  #Si le token actuel est une ouverture de parenthese
                nbSubParenthesis += 1                           #On ajoute 1 au nombre de parenthese
            if token[0] == "TokCloseParen":                 #Si le token actuel est une fermeture de parenthese
                nbSubParenthesis -= 1                           #On retire 1 au nombre de parenthese
            if token[0] == "TokComma" and nbSubBrace == 0 and nbSubBracket == 0 and nbSubParenthesis == 0:#Si le token actuel est une virgule ET qu'on n'est pas dans une sous liste ET qu'on n'est pas dans un selecteur de liste ET qu'on n'est pas dans une sous parenthese
                self.SubNodeList.append(Node(subNodeTokens[firstPos:x]))#On cree le noeud du contenue entre les virgule
                firstPos = x+1                                   #On se place apres la virgule pour la prochaine partie
            
        self.SubNodeList.append(Node(subNodeTokens[firstPos:]))#On cree le noeud du contenue de la derniere partie
        return tokenList[:tokPos]+tokenList[posCloseBrace+1:]#On retourne tout les tokens qui reste apres la fermeture de parenthese
    def LISTSELECTOR(self,tokenList,tokPos):
        self.NodeRule = "LISTSELECTOR"                  #On definie la regle du noeud actuel
        #On recherhe la fermeture de crochet
        nbSubBracket = 0                                #Nombre de sous crochet (on commence a 1 dans la liste des tokens pour ne pas compté l'ouverture de la principale, quand cette variable arrive a -1, c'est que c'est cette parenthese)
        posCloseBracket = tokPos+0                      #Position de la fermeture de crochet actuel
        while nbSubBracket != -1:                         #Tant qu'on n'a pas trouver la fermeture de crochet
            posCloseBracket += 1                                #Position suivante
            if tokenList[posCloseBracket][0]=="TokOpenBracket": #Si il y a une sous crochet
                nbSubBracket += 1                                   #On attend une fermeture en plus
            if tokenList[posCloseBracket][0]=="TokCloseBracket":#Si il y a une fermeture d'une crochet
                nbSubBracket -= 1                                   #On ferme le crochet actuel
        subNodeTokens = tokenList[tokPos+1:posCloseBracket]#On prend le contenue entre les crochets
        self.SubNodeList.append(Node(subNodeTokens))#On cree le noeud du contenue de la derniere partie
        self.value = tokenList[0][1]                    #On enregistre le nom de la variable où chercher le contenue
        return tokenList[:tokPos-1]+tokenList[posCloseBracket+1:]#On retourne tout les tokens qui reste apres la fermeture de crochet
    ##############

    #####TYPE DE DONNEES#####
    def FALSE(self,tokenList,tokPos):
        self.NodeRule = "FALSE"                         #On definie la regle du noeud actuel
        self.Value = False                              #On definie la valeur bool False
        return []                                       #On vide car il n'est pas censer rester de tokens
    def TRUE(self,tokenList,tokPos):
        self.NodeRule = "TRUE"                          #On definie la regle du noeud actuel
        self.Value = True                               #On definie la valeur bool True
        return []                                       #On vide car il n'est pas censer rester de tokens
    def NONE(self,tokenList,tokPos):
        self.NodeRule = "NONE"                          #On definie la regle du noeud actuel
        self.Value = None                               #On definie la valeur du none
        return []                                       #On vide car il n'est pas censer rester de tokens
    def NEGNUMBER(self,tokenList,tokPos):
        self.NodeRule = "NEGNUMBER"                     #On definie la regle du noeud actuel
        self.Value = float(tokenList[0][1])             #On definie la valeur du nombre negatif
        return []                                       #On vide car il n'est pas censer rester de tokens
    def INT(self,tokenList,tokPos):
        self.NodeRule = "INT"                           #On definie la regle du noeud actuel
        self.Value = int(tokenList[0][1])               #On definie la valeur de l'int
        return []                                       #On vide car il n'est pas censer rester de tokens
    def FLOAT(self,tokenList,tokPos):
        self.NodeRule = "FLOAT"                         #On definie la regle du noeud actuel
        self.Value = float(tokenList[0][1])             #On definie la valeur du float
        return []                                       #On vide car il n'est pas censer rester de tokens
    def STRING(self,tokenList,tokPos):
        self.NodeRule = "STRING"                        #On definie la regle du noeud actuel
        self.Value = str(tokenList[0][1])[1:-1]         #On definie la valeur du string en enlevent les guillemet
        return []                                       #On vide car il n'est pas censer rester de tokens
    def VARIABLE(self,tokenList,tokPos):
        self.NodeRule = "VARIABLE"                      #On definie la regle du noeud actuel (ICI c'est une valeur exploitable qu'on definira lors de l'eval)
        self.Value = str(tokenList[0][1])               #On definie le nom de la variable a récuperer
        return []                                       #On vide car il n'est pas censer rester de tokens
    def STRTYPE(self,tokenList,tokPos):
        self.NodeRule = "STRTYPE"                       #On definie la regle du noeud actuel (ICI c'est une valeur exploitable qu'on definira lors de l'eval)
        self.Value = str                                #On definie le nom de la variable a récuperer
        return []                                       #On vide car il n'est pas censer rester de tokens
    def INTTYPE(self,tokenList,tokPos):
        self.NodeRule = "INTTYPE"                       #On definie la regle du noeud actuel (ICI c'est une valeur exploitable qu'on definira lors de l'eval)
        self.Value = int                                #On definie le nom de la variable a récuperer
        return []                                       #On vide car il n'est pas censer rester de tokens
    def FLOATTYPE(self,tokenList,tokPos):
        self.NodeRule = "FLOATTYPE"                     #On definie la regle du noeud actuel (ICI c'est une valeur exploitable qu'on definira lors de l'eval)
        self.Value = float                              #On definie le nom de la variable a récuperer
        return []                                       #On vide car il n'est pas censer rester de tokens
    def BOOLTYPE(self,tokenList,tokPos):
        self.NodeRule = "BOOLTYPE"                      #On definie la regle du noeud actuel (ICI c'est une valeur exploitable qu'on definira lors de l'eval)
        self.Value = bool                               #On definie le nom de la variable a récuperer
        return []                                       #On vide car il n'est pas censer rester de tokens
    def LISTTYPE(self,tokenList,tokPos):
        self.NodeRule = "LISTTYPE"                      #On definie la regle du noeud actuel (ICI c'est une valeur exploitable qu'on definira lors de l'eval)
        self.Value = list                               #On definie le nom de la variable a récuperer
        return []                                       #On vide car il n'est pas censer rester de tokens
    #########################


    #####EXECUTE ALL NODE (EVAL)#####
    def execute(self,variables):
        for x,subNode in enumerate(self.SubNodeList):   #Pour chaque sous noeud
            if type(subNode) == Node:                       #Si le sous noeud est encore un noeud et pas une valeur exploitable
                self.SubNodeList[x] = subNode.execute(variables)#On lance le calcul des noeuds inferieur

        
        if self.NodeRule == "FALSE":        #Si notre noeud est une valeur False
            return False                        #On retourne la valeur False
        if self.NodeRule == "TRUE":         #Si notre noeud est une valeur True
            return True                         #On retourne la valeur True
        if self.NodeRule == "NONE":         #Si notre noeud est une valeur none
            return None                         #On retourne la valeur none
        if self.NodeRule == "NEGNUMBER":    #Si notre noeud est une valeur negative
            return self.Value                   #On retourne la valeur negative
        if self.NodeRule == "INT":          #Si notre noeud est une valeur int
            return self.Value                   #On retourne la valeur int
        if self.NodeRule == "FLOAT":        #Si notre noeud est une valeur float
            return self.Value                   #On retourne la valeur float
        if self.NodeRule == "STRING":       #Si notre noeud est une valeur string
            return self.Value                   #On retourne la valeur string
        if self.NodeRule == "VARIABLE":     #Si notre noeud est une variable
            return variables[self.Value]        #On retourne la valeur de la variable
        if self.NodeRule == "STRTYPE":      #Si notre noeud est un type string
            return str                      #On retourne le type string
        if self.NodeRule == "INTTYPE":      #Si notre noeud est un type int
            return int                          #On retourne le type int
        if self.NodeRule == "FLOATTYPE":    #Si notre noeud est un type float
            return float                        #On retourne le type float
        if self.NodeRule == "BOOLTYPE":     #Si notre noeud est un type bool
            return bool                         #On retourne le type bool
        if self.NodeRule == "LISTTYPE":     #Si notre noeud est un type list
            return list                         #On retourne le type list

        if self.NodeRule == "PRIORITY":     #Si notre noeud est une priorité
            return self.SubNodeList[0]          #On retourne la valeur du sous noeud

        if self.NodeRule == "LISTDATA":     #Si notre noeud est une liste
            returnList = []                     #Liste de valeur de chaque partie de la liste
            for part in self.SubNodeList:       #Pour chaque partie de la liste (sous noeud)
                returnList.append(part)             #On ajoute la partie a la liste de retour
            return returnList                   #On retourne la liste de valeur
        if self.NodeRule == "LISTSELECTOR": #Si notre noeud est un selecteur de liste
            index = self.SubNodeList[0]         #On recupere l'index a aller chercher
            value = variables[self.value][index] #On recupere la valeur a retourné
            return value                        #On retourne la valeur

        if self.NodeRule == "LISTEN":       #Si notre noeud est une ecoute
            return listen()                     #On retourne la valeur de l'ecoute
        if self.NodeRule == "TOSTR":        #Si notre noeud est un changement de type vers str
            return str(self.SubNodeList[0])     #On retourne la valeur du sous noeud en str
        if self.NodeRule == "TOFLOAT":      #Si notre noeud est un changement de type vers str
            return float(self.SubNodeList[0])   #On retourne la valeur du sous noeud en str
        if self.NodeRule == "TOINT":        #Si notre noeud est un changement de type vers str
            return int(self.SubNodeList[0])     #On retourne la valeur du sous noeud en str
        if self.NodeRule == "TYPE":         #Si notre noeud est un type de variable
            return type(self.SubNodeList[0])    #On retourne la valeur du type du sous noeud
        if self.NodeRule == "LENGTH":       #Si notre noeud est une longueur de la données
            return len(self.SubNodeList[0])     #On retourne la longueur de la données du sous noeud
        if self.NodeRule == "DBLOAD":       #Si notre noeud est un chargement de données depuis la db
            with open('lib/data') as json_file:
                db = json.load(json_file)
            return db[self.SubNodeList[0]]
        if self.NodeRule == "DBEXIST":      #Si notre noeud est une verification si il existe une clé dans la db
            with open('lib/data') as json_file:
                db = json.load(json_file)
            return self.SubNodeList[0] in db.keys()

        if self.NodeRule == "ADD":          #Si notre noeud est une addition
            return self.SubNodeList[0] + self.SubNodeList[1]#On retourne la valeur de l'addition des deux sous noeuds
        if self.NodeRule == "SUB":          #Si notre noeud est une soustraction
            return self.SubNodeList[0] - self.SubNodeList[1]#On retourne la valeur de la soustraction des deux sous noeuds
        if self.NodeRule == "MUL":          #Si notre noeud est une multiplication
            return self.SubNodeList[0] * self.SubNodeList[1]#On retourne la valeur de la multiplication des deux sous noeuds
        if self.NodeRule == "DIV":          #Si notre noeud est une division
            return self.SubNodeList[0] / self.SubNodeList[1]#On retourne la valeur de la division des deux sous noeuds

        if self.NodeRule == "EQUAL":        #Si notre noeud est une condition EQUAL
            return self.SubNodeList[0] == self.SubNodeList[1]#On retourne la condition du EQUAL
        if self.NodeRule == "NOTEQUAL":     #Si notre noeud est une condition NOTEQUAL
            return self.SubNodeList[0] != self.SubNodeList[1]#On retourne la condition du NOTEQUAL
        if self.NodeRule == "LESSEQUAL":    #Si notre noeud est une condition LESSEQUAL
            return self.SubNodeList[0] <= self.SubNodeList[1]#On retourne la condition du LESSEQUAL
        if self.NodeRule == "GREATEREGAL":  #Si notre noeud est une condition GREATEREGAL
            return self.SubNodeList[0] >= self.SubNodeList[1]#On retourne la condition du GREATEREGAL
        if self.NodeRule == "LESS":         #Si notre noeud est une condition LESS
            return self.SubNodeList[0] < self.SubNodeList[1]#On retourne la condition du LESS
        if self.NodeRule == "GREATER":      #Si notre noeud est une condition GREATER
            return self.SubNodeList[0] > self.SubNodeList[1]#On retourne la condition du GREATER
        if self.NodeRule == "AND":          #Si notre noeud est une condition AND
            return self.SubNodeList[0] and self.SubNodeList[1]#On retourne la condition du AND
        if self.NodeRule == "OR":           #Si notre noeud est une condition OR
            return self.SubNodeList[0] or self.SubNodeList[1]#On retourne la condition du OR
        if self.NodeRule == "NOT":          #Si notre noeud est une condition NOT
            return not(self.SubNodeList[0])     #On retourne la condition du NOT
        if self.NodeRule == "IN":           #Si notre noeud est une condition IN
            return self.SubNodeList[0] in self.SubNodeList[1]#On retourne la condition du IN

        if self.NodeRule == "PRINT":        #Si notre noeud est un affichage
            print(self.SubNodeList[0])          #On affiche la valeur du sous noeud
        if self.NodeRule == "SET":          #Si notre noeud est un assignement
            variables[self.Value] = self.SubNodeList[0]#On definie la valeur de la variable
        if self.NodeRule == "IF":           #Si notre noeud est une condition
            if self.SubNodeList[0] == True:     #Si la condition retourne True
                variables["_INDENTATION_"] += 1     #On entre dans la condition (indentation +1)
        if self.NodeRule == "SPEAK":        #Si notre noeud est un speak
            #On lance l'audio
            engine.say(str(self.SubNodeList[0]))#On speak le contenue entre parenthese
            #On lance est on attend
            engine.runAndWait()
        if self.NodeRule == "GOTO":         #Si notre noeud est un goto
            newAddonFile = str(self.SubNodeList[0]) #On recupere le nom du fichier a charger
            variables["_INSTRUCTION_INDEX_"].append(-1) #On ajoute l'index du nouveau fichier (0, premiere ligne donc -1 comme on vas passer a l'instruction suivante)
            variables["_INSTRUCTION_FILE_LIST_"].append(ReadAddonFile(newAddonFile))#On recupere et on ajoute les instruction du nouveau fichier
        if self.NodeRule == "WAIT":         #Si notre noeud est un WAIT
            time.sleep(float(self.SubNodeList[0]))#On recupere le temp d'attente
        if self.NodeRule == "RUN":          #Si notre noeud est un RUN
            os.popen(self.SubNodeList[0])       #On execute le fichier
        if self.NodeRule == "OPENBROWSER":  #Si notre noeud est une ouverture de page web
            browserPath = self.SubNodeList[0]   #On recupere le lien du navigateur
            mode = self.SubNodeList[1]          #On recupere le mode (publique ou privé)
            url = self.SubNodeList[2]           #On recupere le lien
            if mode == "PUBLIC":
                os.system('"'+browserPath+"\" "+url)
            else:
                os.system('"'+browserPath+"\" -incognito "+url)
        if self.NodeRule == "DBSAVE":       #Si notre noeud est une sauvegarde dans la db
            key = self.SubNodeList[0]           #On recupere la clé
            value = self.SubNodeList[1]         #On recupere la valeur
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
        if self.NodeRule == "DBDEL":        #Si notre noeud est une suppresion dans la db
            key = self.SubNodeList[0]          #On recupere la clé a supprimer
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
        return variables
    #################################

def Parser(tokenList):
    """
    Verifie et remplace les differents tokens et keyword selon la syntax
    """
    #On retire tout les tokens a ignoré
    tokens = ClearTokens(tokenList)

    ###MISE EN PLACE DU SYNTAXTREE
    syntaxTree = Node(tokens)
    return syntaxTree

def ClearTokens(oldTokens):
    """
    Retire tout les tokens ignoré
    """
    #Nouveau tokens
    tokens = []
    #Pour chaque token
    for token in oldTokens:
        #Si le token n'est pas ignoré
        if not(token[0] in IGNORE):
            #On ajoute le token a la nouvelle liste
            tokens.append(token)
    return tokens


def ReadAddonFile(File_Name):
    Addon_File = open("lib/"+str(File_Name),"r")
    Addon_Instruction = Addon_File.readlines()
    Addon_File.close()
    return Addon_Instruction

def listen():
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
    return query