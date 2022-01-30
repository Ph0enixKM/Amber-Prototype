from .lexer import Lexer
from .modules import *


class Parser:
    def __init__(self, lexem):
        self.lexem = lexem
        self.exp = None
        self.parser()

    def parser(self):
        self.exp = Block()
        self.exp.ast(self.lexem)
    
    def translate(self):
        translation = self.exp.translate()
        print(translation)

    def get(self):
        return self.exp

if __name__ == '__main__':
    code = 'let a = 12'
    lexer = Lexer(code)
    parser = Parser(lexer.get())
    