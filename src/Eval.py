#Calculé les valeur

def calc(syntax_tree,nodeName,variables):
    node = syntax_tree[nodeName]
    if node.type == "VARIABLE":
        syntax_tree[nodeName] = variables[node.value]
    if node.type == "NUMBER":
        syntax_tree[nodeName] = float(node.value)
    if node.type == "STRING":
        syntax_tree[nodeName] = str(node.value)

    if node.type == "PARENTHESIS":
        syntax_tree[nodeName] = syntax_tree[node.nameNode1]

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

    return syntax_tree

def eval(syntax_tree,variables):
    #Pour chaque node
    for node in syntax_tree:
        #Si la premiere dependance est None ou pas une liste (donc deja definie)
        if syntax_tree[node].nameNode1 == None or type(syntax_tree[syntax_tree[node].nameNode1]) != list:
            #Si la deuxieme dependance est None ou pas une liste (donc deja definie)
            if syntax_tree[node].nameNode2 == None or type(syntax_tree[syntax_tree[node].nameNode2]) != list:
                #On calcul
                syntax_tree = calc(syntax_tree,node,variables)

    return syntax_tree