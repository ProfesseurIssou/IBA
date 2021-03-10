#Calculé les valeur
import json

def calc(syntax_tree,nodeName,variables):
    node = syntax_tree[nodeName]
    if node.type == "VARIABLE":
        syntax_tree[nodeName] = variables[node.value]
    if node.type == "NUMBER":
        syntax_tree[nodeName] = float(node.value)
    if node.type == "STRING":
        syntax_tree[nodeName] = str(node.value)
    if node.type == "NONE_TYPE":
        syntax_tree[nodeName] = None
    if node.type == "TRUE_BOOL_TYPE" or node.type == "FALSE_BOOL_TYPE":
        syntax_tree[nodeName] = node.value
    if node.type == "LIST_DATA":
        data1 = 0
        data2 = 0
        #Si la premiere valeur est deja une liste
        if type(syntax_tree[node.nameNode1]) == list:
            data1 = syntax_tree[node.nameNode1]
        else:
            #Sinon on la transforme en liste
            data1 = [syntax_tree[node.nameNode1]]
        #Si la deuxieme valeur est deja une liste
        if type(syntax_tree[node.nameNode2]) == list:
            data2 = syntax_tree[node.nameNode2]
        else:
            #Sinon on la transforme en liste
            data2 = [syntax_tree[node.nameNode2]]
        syntax_tree[nodeName] = data1 + data2
    if node.type == "LIST_VARIABLE":
        value = syntax_tree[node.value]
        index = int(syntax_tree[node.nameNode1])
        syntax_tree[nodeName] = value[index]

    if node.type == "PARENTHESIS":
        syntax_tree[nodeName] = syntax_tree[node.nameNode1]

    if node.type == "TO_STRING":
        syntax_tree[nodeName] = str(syntax_tree[node.nameNode1])
    if node.type == "TO_NUMBER":
        syntax_tree[nodeName] = float(syntax_tree[node.nameNode1])
    if node.type == "TO_INT":
        syntax_tree[nodeName] = int(syntax_tree[node.nameNode1])

    if node.type == "ADD":
        syntax_tree[nodeName] = syntax_tree[node.nameNode1] + syntax_tree[node.nameNode2]
    if node.type == "SUB":
        syntax_tree[nodeName] = syntax_tree[node.nameNode1] - syntax_tree[node.nameNode2]
    if node.type == "MUL":
        syntax_tree[nodeName] = syntax_tree[node.nameNode1] * syntax_tree[node.nameNode2]
    if node.type == "DIV":
        syntax_tree[nodeName] = syntax_tree[node.nameNode1] / syntax_tree[node.nameNode2]

    if node.type == "EGAL_CONDITION":
        syntax_tree[nodeName] = (syntax_tree[node.nameNode1] == syntax_tree[node.nameNode2])
    if node.type == "NOTEGAL_CONDITION":
        syntax_tree[nodeName] = (syntax_tree[node.nameNode1] != syntax_tree[node.nameNode2])
    if node.type == "MORE_EGAL_CONDITION":
        syntax_tree[nodeName] = (syntax_tree[node.nameNode1] >= syntax_tree[node.nameNode2])
    if node.type == "MORE_CONDITION":
        syntax_tree[nodeName] = (syntax_tree[node.nameNode1] > syntax_tree[node.nameNode2])
    if node.type == "LESS_EGAL_CONDITION":
        syntax_tree[nodeName] = (syntax_tree[node.nameNode1] <= syntax_tree[node.nameNode2])
    if node.type == "LESS_CONDITION":
        syntax_tree[nodeName] = (syntax_tree[node.nameNode1] < syntax_tree[node.nameNode2])
    if node.type == "AND_CONDITION":
        syntax_tree[nodeName] = (syntax_tree[node.nameNode1] and syntax_tree[node.nameNode2])
    if node.type == "OR_CONDITION":
        syntax_tree[nodeName] = (syntax_tree[node.nameNode1] or syntax_tree[node.nameNode2])
    if node.type == "IN_CONDITION":
        syntax_tree[nodeName] = (syntax_tree[node.nameNode1] in syntax_tree[node.nameNode2])
    if node.type == "NOT_CONDITION":
        syntax_tree[nodeName] = not(syntax_tree[node.nameNode1])

    if node.type == "DB_LOAD":
        with open('lib/data') as json_file:
            db = json.load(json_file)
        syntax_tree[nodeName] = db[syntax_tree[node.nameNode1]]
    if node.type == "DB_EXIST":
        with open('lib/data') as json_file:
            db = json.load(json_file)
        syntax_tree[nodeName] = syntax_tree[node.nameNode1] in db.keys()

    return syntax_tree

def eval(syntax_tree,variables):
    #Pour chaque node
    for node in syntax_tree:
        #Si la premiere dependance est None ou pas une liste (donc deja definie)
        if syntax_tree[node].nameNode1 == None or type(syntax_tree[syntax_tree[node].nameNode1]) != list or syntax_tree[node].type == "LIST_DATA":
            #Si la deuxieme dependance est None ou pas une liste (donc deja definie)
            if syntax_tree[node].nameNode2 == None or type(syntax_tree[syntax_tree[node].nameNode2]) != list or syntax_tree[node].type == "LIST_DATA":
                #On calcul
                syntax_tree = calc(syntax_tree,node,variables)

    return syntax_tree