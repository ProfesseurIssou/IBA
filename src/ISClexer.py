import re
tokenType = {          #Pour lexer
    "TokSh":"[#]",

    "TokString":"[\"|\'].+?[\"|\']",
    
    "TokNegativeNumber":r"(?:[^0-9a-zA-Z\)]{1})([-][0-9.]+)",
    "TokFloat":r"(?:[^0-9a-zA-Z]{1})([0-9]+[.]{1}[0-9]+)",
    "TokInt":r"(?:[^0-9a-zA-Z]{1})([0-9]+)",

    "TokListen":r"listen\(\)",

    "TokPlus":"[+]",
    "TokMinus":"[-]",
    "TokStar":"[*]",
    "TokSlash":"[/]",
    "TokPercent":"[%]",
    "TokExp":"[\^]",

    "TokEqual":"==",
    "TokNotEqual":"!=",
    "TokLessEqual":"<=",
    "TokGreaterEqual":">=",
    "TokLess":"<",
    "TokGreater":">",

    "TokAssign":"=",

    "TokOpenParen":r"[\(]",
    "TokCloseParen":r"[\)]",
    "TokOpenBrace":r"[\{]",
    "TokCloseBrace":r"[\}]",
    "TokOpenBracket":r"[\[]",
    "TokCloseBracket":r"[\]]",

    "TokSemiColon":"[;]",
    "TokColon":"[:]",
    "TokComma":"[,]",
    "TokSpace":"[ ]",
    
    "TokVariable":"[a-zA-Z0-9_]+",
}

keywords = { #Comme tout les token constitué de lettre passerons en variable, on vas repasser sur toute les variables pour voir si ce n'est pas des keyword
    "TokNone":"none",
    "TokFalse":"false",
    "TokTrue":"true",

    "TokPrint":"print",
    "TokSpeak":"speak",
    "TokGoto":"goto",
    "TokWait":"wait",
    "TokExecute":"run",
    "TokOpenBrowser":"openBrowser",

    "TokType":"type",
    "TokToStr":"toStr",
    "TokToFloat":"toFloat",
    "TokToInt":"toInt",
    "TokLen":"len",

    "TokStrType":"str",
    "TokIntType":"int",
    "TokFloatType":"float",
    "TokBoolType":"bool",
    "TokListType":"list",

    "TokIf":"if",
    "TokAnd":"and",
    "TokOr":"or",
    "TokIn":"in",
    "TokNot":"not",

    "TokDbSave":"db_save",
    "TokDbLoad":"db_load",
    "TokDbDel":"db_del",
    "TokDbExist":"db_exist",
}

def Lexer(Instruction):
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
                        #On prend uniquement le premier et sans les guillemet
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
    
    #Pour chaque keyword
    for keyword in keywords.keys():
        #Pour chaque token
        for x,token in enumerate(tokenList):
            #Si le token est une variable
            if token[0] == "TokVariable":
                #Si le token correspond au keyword
                if token[1] == keywords[keyword]:
                    #On remplace la variable par ce keyword
                    tokenList[x] = [keyword,token[1]]
    return tokenList