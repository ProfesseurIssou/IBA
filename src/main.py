import Lexer, Parser, Eval, Execute

#Pour les goto_line mettre dans une variable tout le fichier et une autre pour la ligne actuel pour changer de ligne

def test1():
    instruction = "%maVar% = 93+98"
    instruction1 = "%maVar% = 93+98/50-%z%"
    instruction2 = "print %test%"
    instruction3 = "if x == y"

    variables = {
        "%z%":10
    }

    #On rassemble les données de l'instruction en token
    tokens = Lexer.Gen(instruction1)
    # tokens = Lexer.Gen(instruction2)
    # tokens = Lexer.Gen(instruction3)
    print(tokens)
    #On separe le sens d'execution des token
    syntax_tree = Parser.parse(tokens)
    print(syntax_tree)
    #On calcul (eval)
    eval = Eval.eval(syntax_tree,variables)
    print(eval)
    #On execute l'instruction
    variables = Execute.execute(eval,variables)
    print(variables)
# test1()

def test2():
    variables = {}
    while 1:
        tokens = Lexer.Gen(str(input(">")))
        #On separe le sens d'execution des token
        syntax_tree = Parser.parse(tokens)
        #On calcul (eval)
        eval = Eval.eval(syntax_tree,variables)
        #On execute l'instruction
        variables = Execute.execute(eval,variables)
        print(variables)
# test2()

def test3():
    instructionList = [
        '%test% = None',
        'print %test%'
    ]
    variables = {"%IDENTATION%":0}
    for instruction in instructionList:
        tokens = Lexer.Gen(instruction)
        #On separe le sens d'execution des token
        syntax_tree = Parser.parse(tokens)
        #On calcul (eval)
        eval = Eval.eval(syntax_tree,variables)
        #On execute l'instruction
        variables = Execute.execute(eval,variables)
        print(variables)
test3()