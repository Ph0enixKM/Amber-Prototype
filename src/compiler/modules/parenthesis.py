from .syntax_module import SyntaxModule, Expression


class Parenthesis(SyntaxModule):
    def __init__(self):
        self.expr = None
    
    def ast(self, tokens):
        if len(tokens) > 2:
            if tokens[0].word != '(':
                return None
            self.expr = Expression()
            tokens = self.expr.ast(tokens[1:])
            return tokens[1:]
