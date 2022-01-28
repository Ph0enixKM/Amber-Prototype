from error import error

class SyntaxModule:
    def __init__(self):
        pass
    
    def ast(self, tokens):
        raise 'Undefined Syntax (Conversion to AST)'

    def validate(self, ast):
        raise 'Undefined Syntax (AST Validation)'
    
    def translate(self, ast):
        raise 'Undefined Syntax (AST Translation)'

class Expression(SyntaxModule):
    def __init__(self):
        # TODO: Values are incorrect:
        self.modules = [Variable, Number]

    def ast(self, tokens):
        for module in self.modules:
            mod = module()
            res = mod.ast(tokens)
            if res != None:
                self.expr = mod
                if len(res) == 0:
                    return res
        row = tokens[0].row
        col = tokens[0].col
        error(f'Undefined Syntax at {row}:{col}')

class Number(SyntaxModule):
    def ast(self, tokens):
        if len(tokens) == 1:
            self.value = tokens[0].word
            if not self.value.replace('.', '', 1).isdigit():
                return None
            return []
        if len(tokens) == 2:
            [minus, value] = tokens
            if minus.word != '-':
                return None
            if not value.replace('.', '', 1).isdigit():
                return None
            self.value = value
            return []

class Variable(SyntaxModule):
    def ast(self, tokens):
        if len(tokens) > 3:
            [key, name, eq, *exp] = tokens
            if key.word != 'box' and eq.word != '=':
                return None
            self.name = name.word
            self.expr = Expression()
            return self.expr.ast(exp)
