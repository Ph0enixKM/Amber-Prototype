from error import error_tok, ErrorTypes
from .syntax_module import SyntaxModule, Expression


class Variable(SyntaxModule):
    def __init__(self):
        self.name = ''
        self.expr = None

    def ast(self, tokens):
        if len(tokens) > 3:
            [key, name, eq, *exp] = tokens
            if key.word != 'box' or eq.word != '=':
                return None
            if not self.is_variable_name(name.word):
                error_tok(name, ErrorTypes.VAR.value)
            self.name = name.word
            self.expr = Expression()
            return self.expr.ast(exp)


class VariableReference(SyntaxModule):
    def __init__(self):
        self.name = ''
    
    def ast(self, tokens):
        if len(tokens):
            if not self.is_variable_name(tokens[0].word):
                return None
            self.name = tokens[0].word
            return tokens[1:]
