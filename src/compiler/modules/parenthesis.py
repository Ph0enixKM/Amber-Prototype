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
    
    @staticmethod
    def remove_outer_parenthesis(code):
        while code[0] == '(' and code[-1] == ')':
            code = code[1:-1]
        return code
    
    def translate(self):
        return f'({self.expr.translate()})'
    
    def numberify(self):
        return f'({self.expr.numberify()})'
    
    def stringify(self):
        return f'({self.expr.stringify()})'
    
    def arraify(self):
        return f'({self.expr.arraify()})'
