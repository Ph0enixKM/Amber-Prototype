from frontend import Lexer, Parser

lexer = Lexer('let code = 12')
parser = Parser(lexer.get())



for token in lexer.get():
    print(token)
    