def Eval(syntaxTree,variables):
    variables = syntaxTree.execute(variables)   #On dit aux noeud de s'executer
    return variables