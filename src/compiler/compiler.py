from .lexer import Lexer
from .parser import Parser


class Compiler:
    def __init__(self, code):
        self.lexer = Lexer(code)
        self.parser = Parser(self.lexer.get())
        
    
    def ast(self):
        return self.parser.get().generate_tree()
    
    def compile(self):
        return self.parser.translate()
