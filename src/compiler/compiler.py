from .lexer import Lexer
from .parser import Parser
from .modules import SyntaxModule


class Compiler:
    def __init__(self, code):
        self.lexer = Lexer(code)
        self.parser = Parser(self.lexer.get())

    def loadPrecompiled(self, binary):
        self.parser.expr.statements += binary['code']
        SyntaxModule.memory.scopes = binary['memory']

    def rawAst(self):
        self.parser.parser()
        return self.parser.get()

    def ast(self):
        return self.rawAst().generate_tree()

    def compile(self):
        self.parser.parser()
        return self.parser.translate()
