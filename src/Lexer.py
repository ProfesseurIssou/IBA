#Faire par regex (pour les string principalement)
tokenType = {
    "LETTER":[
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z"
    ],
    "NUMBER":[
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "."
    ],
    "PLUS":[
        "+"
    ],
    "MINUS":[
        "-"
    ],
    "MUL":[
        "*"
    ],
    "DIV":[
        "/"
    ],
    "EGAL":[
        "="
    ],
    "SPACE":[
        " "
    ],
    "PERCENT":[
        "%"
    ],
    "STRING_DELIMITER":[
        "'",
        '"'
    ],
    "PARENTHESIS_OPEN":[
        "("
    ],
    "PARENTHESIS_CLOSE":[
        ")"
    ]
}

keywords = {
    "VARIABLE":[
        ["PERCENT","LETTER","PERCENT"]
    ],
    "STRING":[
        ["STRING_DELIMITER","LETTER","STRING_DELIMITER"],
        ["STRING_DELIMITER","NUMBER","STRING_DELIMITER"],
        ["STRING_DELIMITER","SPACE","STRING_DELIMITER"]
    ],
    "CONDITION":[
        [["LETTER","if"],"SPACE"]
    ],
    "PRINT":[
        [["LETTER","print"],"SPACE"]
    ],
    "SET":[
        ["VARIABLE","EGAL"],
        ["VARIABLE","SPACE","EGAL"]
    ]
}
#NOMBRE NEGATIF

def identifier(charact):
    """
    Identification du type de token
    """
    #Pour chaque type de token
    for token in tokenType.keys():
        #Si le charactere correspond a l'un des trigger du type de token
        if charact in tokenType[token]:
            return token

def keywordChecker(tokens_list):
    """
    Verifie et remplace les differents tokens par un keyword
    """
    #Les tokens verifier
    tokens = []
    #Tant qu'il reste des tokens
    while tokens_list != []:
        #Les tokens en cour d'analyse
        testToken = []
        #Si un keyword a ete trouve
        keywordFound = False
        #Pour chaque token
        for token in tokens_list:
            #On ajoute le token a la liste de test
            testToken.append(token)
            #Pour chaque keyword
            for keyword in keywords.keys():
                #Pour chaque forme du keyword
                for keywordForm in keywords[keyword]:
                    #Si la taille des token et du keywords correspondent
                    if len(keywordForm) == len(testToken):
                        #Le keyword pourais correspondre
                        keywordFound = True
                        #Pour chaque partie du keyword
                        for pos,keywordPart in enumerate(keywordForm):
                            #Si le keywordPart est une liste
                            if type(keywordPart) == list:
                                #Si le type ou la valeur ne correspond pas
                                if keywordPart[0] != testToken[pos][0] or keywordPart[1] != testToken[pos][1]:
                                    #On dit que ce n'est pas le bon keyword
                                    keywordFound = False
                            #Sinon
                            else:
                                #Si le type ne correspond pas
                                if keywordPart != testToken[pos][0]:
                                    #On dit que ce n'est pas le bon keyword
                                    keywordFound = False
                    #Si on keyword a ete trouver
                    if keywordFound:
                        #On ne regarde pas les autre forme de keyword
                        break
                #Si on keyword a ete trouver
                if keywordFound:
                    #On ne regarde pas les autre keyword
                    break
            #Si on keyword a ete trouver
            if keywordFound:
                #On n'ajoute pas d'autre token
                break
        #Si on keyword a ete trouver
        if keywordFound:
            #On ajoute le nouveau keyword a la liste
            tokens.append([keyword,""])
            #On ajoute sa valeur
            #Pour chaque token composant le keyword
            for token in testToken:
                #On ajoute sa valeur a la valeur du keyword
                tokens[-1][1] += token[1]
                #On supprime le token de token_list
                del tokens_list[0]
        #Sinon
        else:
            #On ajoute le premier token tel quel dans la liste
            tokens.append(tokens_list[0])
            #On supprime le token
            del tokens_list[0]
    return tokens

def Gen(instruction):
    """
    Generation des tokens de l'instruction
    """
    #Liste des token [[type,value],...]
    tokens = []
    #Token lors du traitement
    tokenType = ""
    #Pour chaque caractere de l'instruction
    for charact in instruction:
        #On recupere le type
        tokenType = identifier(charact)
        #Si la liste des token n'est pas vide ET que l'ancien type est le meme
        if tokens != [] and tokenType == tokens[-1][0]:
            #On ajoute la valeur a l'ancien type
            tokens[-1][1] += charact
        #Sinon
        else:
            #On ajoute le nouveau type et sa valeur
            tokens.append([tokenType,charact])
    #On check les keyword
    tokens = keywordChecker(tokens)
    #On check une seconde fois
    tokens = keywordChecker(tokens)
    return tokens