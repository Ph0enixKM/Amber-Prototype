from .lexer import Lexer
from .modules import *


class Parser:
    def __init__(self, lexem):
        self.lexem = lexem
        self.parser()

    def parser(self):
        exp = Expression()
        exp.ast(self.lexem)
        print(exp.__dict__)

if __name__ == '__main__':
    code = 'let a = 12'
    lexer = Lexer(code)
    parser = Parser(lexer.get())
    