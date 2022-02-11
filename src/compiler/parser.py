from .lexer import Lexer
from .modules import *

class Parser:
    def __init__(self, lexem):
        self.lexem = lexem
        self.expr = Block()

    def parser(self):
        self.expr.ast(self.lexem)
    
    def translate(self):
        translation = self.expr.translate()
        return translation

    def get(self):
        return self.expr

if __name__ == '__main__':
    code = 'let a = 12'
    lexer = Lexer(code)
    parser = Parser(lexer.get())
    