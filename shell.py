

#RUN
from interpreter import Context, Interpreter
from lexer import Lexer
from parserLR import Parser



def run(fn, text):
    #Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    print('\nTOKENS: \n',tokens,'\n')
    if error: return None, error

    #Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    #Run program
    interpreter = Interpreter()
    context = Context('<program>')
    result = interpreter.visit(ast.node, context)

    return result.value, result.error


#main
while True:
    text = input('Cat > ')
    result, error = run('<stdin>', text)

    if error:
        print(error.as_string())
    else:
        print(result)