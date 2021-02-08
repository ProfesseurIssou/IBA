#On remplace les token par des noeud celon les regle

#8+5*22 => 
# MULT(5,22)
# ADD(8,MUL(5,22))

#On cree des nodes


#Token a ignoré
IGNORE = [
    ["SPACE"," "],
    ["DOUBLE_POINT",":"]
]

#Regle des noeuds (node est un noeud calculer)
RULES = {
    "NUMBER":["NUMBER"],
    "NEGATIVE_NUMBER":["OPEN_PARENTHESIS","MINUS","NUMBER","CLOSE_PARENTHESIS"],
    "STRING":["STRING"],
    "NONE_TYPE":["NONE_TYPE"],
    "VARIABLE":["VARIABLE"],

    "SET":["SET","NODE"],
    "PRINT":["PRINT","NODE"],
    "SPEAK":["SPEAK","NODE"],
    "LISTEN":["LISTEN"],
    "OPEN_BROWSER":["OPEN_BROWSER","NODE","COMMA","NODE","COMMA","NODE","CLOSE_PARENTHESIS"],

    "ADD":["NODE","PLUS","NODE"],
    "SUB":["NODE","MINUS","NODE"],
    "DIV":["NODE","DIV","NODE"],
    "MUL":["NODE","MUL","NODE"],

    "TO_STRING":["TO_STRING","NODE","CLOSE_PARENTHESIS"],
    "TO_NUMBER":["TO_NUMBER","NODE","CLOSE_PARENTHESIS"],

    "EXECUTE":["EXECUTE","NODE","CLOSE_PARENTHESIS"],

    "PARENTHESIS":["OPEN_PARENTHESIS","NODE","CLOSE_PARENTHESIS"],

    "CONDITION":["CONDITION","NODE"],
    "EGAL_CONDITION":["NODE","EGAL_TO_CONDITION","NODE"],
    "NOTEGAL_CONDITION":["NODE","NOTEGAL_TO_CONDITION","NODE"],
    "MORE_EGAL_CONDITION":["NODE","MORE_EGAL_THAN_CONDITION","NODE"],
    "MORE_CONDITION":["NODE","MORE_THAN_CONDITION","NODE"],
    "LESS_EGAL_CONDITION":["NODE","LESS_EGAL_THAN_CONDITION","NODE"],
    "LESS_CONDITION":["NODE","LESS_THAN_CONDITION","NODE"],
    "AND_CONDITION":["NODE","AND_CONDITION","NODE"],
    "OR_CONDITION":["NODE","OR_CONDITION","NODE"],
    "IN_CONDITION":["NODE","IN_CONDITION","NODE"]
}
PRIORITY = [
    ["NUMBER","VARIABLE","STRING","NEGATIVE_NUMBER","NONE_TYPE"],#TYPE DE DONNEE (1=en premier)
    ["TO_STRING","TO_NUMBER"],#CONVERSION DONNEE (2=en deuxieme)
    ["MUL","DIV"],#CALCUL
    ["ADD","SUB"],#CALCUL
    ["EGAL_CONDITION","NOTEGAL_CONDITION","MORE_EGAL_CONDITION","MORE_CONDITION","LESS_EGAL_CONDITION","LESS_CONDITION","IN_CONDITION"],#CONDITION
    ["AND_CONDITION","OR_CONDITION"],#CONDITION
    ["PARENTHESIS"],#PRIORITER
    ["SET","PRINT","CONDITION","SPEAK","LISTEN","EXECUTE","OPEN_BROWSER"]#INSTRUCTION
]


class node:
    def __init__(self,nodeName,nodeType,nodeValue,nodeNameInput1=None,nodeNameInput2=None,nodeNameInput3=None):
        #Nom du noeud (selon la taille de l'arbre syntaxique)
        self.name = nodeName
        #Type du noeud (VARIABLE, NUMBER, EGAL, PLUS, MINUS, DIV, MUL)
        self.type = nodeType
        #Valeur du noeud (Nombre ou charactere, sinon None)
        self.value = nodeValue
        #Nom des node input
        self.nameNode1 = nodeNameInput1
        self.nameNode2 = nodeNameInput2
        self.nameNode3 = nodeNameInput3

def nodeMaker(syntaxTree,rule,tokens):
    nodeName = str(len(syntaxTree))
    nodeType = rule
    nodeValue = None
    nodeNameInput1 = None
    nodeNameInput2 = None
    nodeNameInput3 = None

    if rule=="NUMBER":
        nodeValue = tokens[0][1]
    if rule=="NEGATIVE_NUMBER":
        nodeType = "NUMBER"
        nodeValue = -float(tokens[2][1])
    if rule=="STRING":
        #On retire les " et ' de la valeur
        nodeValue = tokens[0][1].replace("'","").replace('"',"")
    if rule=="NONE_TYPE":
        nodeValue = None
    if rule=="VARIABLE":
        nodeValue = tokens[0][1]

    if rule=="PARENTHESIS":
        nodeNameInput1 = tokens[1][1].name

    if rule=="TO_STRING":
        nodeNameInput1 = tokens[1][1].name
    if rule=="TO_NUMBER":
        nodeNameInput1 = tokens[1][1].name

    if rule=="EXECUTE":
        nodeNameInput1 = tokens[1][1].name
    
    if rule=="ADD":
        nodeNameInput1 = tokens[0][1].name
        nodeNameInput2 = tokens[2][1].name
    if rule=="SUB":
        nodeNameInput1 = tokens[0][1].name
        nodeNameInput2 = tokens[2][1].name
    if rule=="MUL":
        nodeNameInput1 = tokens[0][1].name
        nodeNameInput2 = tokens[2][1].name
    if rule=="DIV":
        nodeNameInput1 = tokens[0][1].name
        nodeNameInput2 = tokens[2][1].name

    if rule=="SET":
        nodeValue = tokens[0][1]
        nodeNameInput1 = tokens[1][1].name
    if rule=="PRINT":
        nodeValue = tokens[0][1]
        nodeNameInput1 = tokens[1][1].name
    if rule=="LISTEN":
        #On prend la variable dans la quelle il faut stocker
        nodeValue = tokens[0][1].split(" ")[1]

    if rule=="OPEN_BROWSER":
        nodeNameInput1 = tokens[1][1].name
        nodeNameInput2 = tokens[3][1].name
        nodeNameInput3 = tokens[5][1].name

    if rule=="EGAL_CONDITION":
        nodeNameInput1 = tokens[0][1].name
        nodeNameInput2 = tokens[2][1].name
    if rule=="NOTEGAL_CONDITION":
        nodeNameInput1 = tokens[0][1].name
        nodeNameInput2 = tokens[2][1].name
    if rule=="MORE_EGAL_CONDITION":
        nodeNameInput1 = tokens[0][1].name
        nodeNameInput2 = tokens[2][1].name
    if rule=="MORE_CONDITION":
        nodeNameInput1 = tokens[0][1].name
        nodeNameInput2 = tokens[2][1].name
    if rule=="LESS_EGAL_CONDITION":
        nodeNameInput1 = tokens[0][1].name
        nodeNameInput2 = tokens[2][1].name
    if rule=="LESS_CONDITION":
        nodeNameInput1 = tokens[0][1].name
        nodeNameInput2 = tokens[2][1].name
    if rule=="AND_CONDITION":
        nodeNameInput1 = tokens[0][1].name
        nodeNameInput2 = tokens[2][1].name
    if rule=="OR_CONDITION":
        nodeNameInput1 = tokens[0][1].name
        nodeNameInput2 = tokens[2][1].name
    if rule=="IN_CONDITION":
        nodeNameInput1 = tokens[0][1].name
        nodeNameInput2 = tokens[2][1].name

    currentNode = node(nodeName,nodeType,nodeValue,nodeNameInput1,nodeNameInput2,nodeNameInput3)
    return currentNode

def clearTokens(oldTokens):
    """
    Retire tout les tokens ignoré
    """
    #Nouveau tokens
    tokens = []
    #Pour chaque token
    for token in oldTokens:
        #Si le token n'est pas ignoré
        if not token in IGNORE:
            #On ajoute le token a la nouvelle liste
            tokens.append(token)
    return tokens

def parse(tokens):
    """
    Verifie et remplace les differents tokens et keyword selon la syntax
    """
    #On retire tout les tokens a ignoré
    tokens = clearTokens(tokens)
    #L'arbre syntaxique
    syntaxTree = {}
    #Niveau de priorité (il augmente tour par tout et dés qu'un calcul est fait, il repasse a 0)
    priorityLevel = 0
    #tant qu'on n'a pas fait tout les modification de toute les priorité
    while priorityLevel != len(PRIORITY):
        #Nombre de token
        nbToken = len(tokens)
        #Pour chaque tokens
        for xToken in range(nbToken):
            #Pour chaque règles de la priorité
            for rule in PRIORITY[priorityLevel]:
                #Nombre de token restant
                nbToken = len(tokens)
                #Si on depasse le nombre de token (du a la suppression par la creation d'une node)
                if xToken > nbToken:
                    break
                #Nombre de regle a respecter
                nbRulePart = len(RULES[rule])
                #Nombre de regle respecter
                nbRuleAccepted = 0
                #Pour chaque partie de la regle
                for xRule,ruleCondition in enumerate(RULES[rule]):
                    #Si la regle depasse la limite des token
                    if xRule+xToken == len(tokens):
                        #On passe au suivant
                        break
                    #Si la regle est une condition unique
                    if type(ruleCondition) == list:
                        #Si le type correspond
                        if tokens[xToken+xRule][0] == ruleCondition[0]:
                            #Si c'est une node et que le type correspond
                            if tokens[xToken+xRule][0] == "NODE" and syntaxTree[tokens[xToken+xRule][1].name].type == ruleCondition[1]:
                                #On augmente de 1 le nombre de condition respecter
                                nbRuleAccepted += 1
                            #Sinon si la valeur est le meme
                            elif tokens[xToken+xRule][1] == ruleCondition[1]:
                                #On augmente de 1 le nombre de condition respecter
                                nbRuleAccepted += 1
                    else:
                        #Si la partie correspond
                        if tokens[xToken+xRule][0] == ruleCondition:
                            #On augmente de 1 le nombre de condition respecter
                            nbRuleAccepted += 1
                #Si la regle est accepter
                if nbRulePart == nbRuleAccepted:
                    #On passe a la plus haute priorité
                    priorityLevel = 0
                    #On cree une node
                    syntaxTree[str(len(syntaxTree))] = nodeMaker(syntaxTree,rule,tokens[xToken:xToken+nbRulePart])
                    # #On change ça valeur dans les tokens
                    tokens[xToken] = ["NODE",syntaxTree[str(len(syntaxTree)-1)]]
                    #Si on a plus qu'un token
                    if nbRulePart != 1:
                        #Pour chaque autre token
                        for x in range(nbRulePart-1):
                            #On supprime les token qui suit
                            del tokens[xToken+1]
        #On passe à la priorité suivante
        priorityLevel += 1
    return syntaxTree