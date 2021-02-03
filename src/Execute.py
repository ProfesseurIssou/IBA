

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
        variables["%IDENTATION%"]+=1
    return variables



def execute(eval,variables):
    #On recupere le type de l'instruction
    instructionType = eval[str(len(eval)-1)].type
    if instructionType == "SET":
        variables = SET(eval,variables)
    if instructionType == "PRINT":
        PRINT(eval)
    if instructionType == "CONDITION":
        variables = CONDITION(eval,variables)
        
    return variables