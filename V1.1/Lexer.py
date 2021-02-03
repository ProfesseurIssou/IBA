import re

tokenType = {
    "VARIABLE":"%[a-zA-Z0-9]{,}%",
    "STRING":"[\"|\'].+[\"|\']",
    "LETTER":"[a-zA-Z]+",
    "NUMBER":"[0-9\.]+",
    "PLUS":"[+]",
    "MINUS":"[-]",
    "MUL":"[*]",
    "DIV":"[/]",
    "EGAL":"[=]",
    "SPACE":"[ ]"
}

keywords = {
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


def Gen(Instruction):
    """
    Generation des tokens de l'instruction
    """
    #On cree la liste des token (on la divisera au fur et a mesure)
    tokenList = [Instruction]    
    #Pour chaque type de token
    for tokenName in tokenType.keys():
        #Si on effectue une modification
        changed = True
        #Tant qu'on trouve des token
        while(changed):
            #On remet les changement a aucun
            changed = False
            #Pour chaque partie du token
            for xToken,token in enumerate(tokenList):
                #Si le token n'est pas une liste (pas encore traiter)
                if type(token) != list:
                    #On trouve toute les coherance
                    findToken = re.findall(tokenType[tokenName],token)
                    #Si on à trouvé
                    if findToken != []:
                        #On prend uniquement le premier
                        findToken = findToken[0]
                        #On a modifier quelque chose
                        changed = True
                        #On cree une liste de token temporaire
                        tempTokenList = []
                        #On cherche la position du token
                        findTokenPos = token.find(findToken)
                        #On decoupe la liste en ce point
                        tempTokenList += tokenList[:xToken]+[tokenList[xToken][:findTokenPos]]
                        tempTokenList += [[tokenName,findToken]]
                        tempTokenList += [tokenList[xToken][findTokenPos+len(findToken):]]+tokenList[xToken+1:]
                        #On vide la liste
                        tokenList = []
                        #On supprime toute les partie vide de la liste
                        for tempToken in tempTokenList:
                            #Si c'est pas vide
                            if tempToken != '':
                                #On ajoute a la liste
                                   tokenList.append(tempToken)
                        #On quitte la boucle pour recommencer le scan
                        break
    #On cherche les keyword
    tokenList = keywordChecker(tokenList)
    return tokenList