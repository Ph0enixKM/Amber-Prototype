from .syntax_module import SyntaxModule, Expression


class Sum(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['+'])
        return tokens


class Sub(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['-'])
        return tokens


class Mul(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['*'])
        return tokens


class Div(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['/'])
        return tokens


class Mod(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['%'])
        return tokens


class Eq(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['=', '='])
        return tokens


class Neq(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['!', '='])
        return tokens


class Gt(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['>'])
        return tokens


class Gte(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['>', '='])
        return tokens


class Lt(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['<'])
        return tokens


class Lte(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['<', '='])
        return tokens


class And(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['and'])
        return tokens


class Or(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['or'])
        return tokens


class Not(SyntaxModule):
    def __init__(self):
        self.expr = None
    
    def ast(self, tokens):
        if len(tokens) > 1:
            if tokens[0].word == 'not':
                self.expr = Expression()
                return self.expr.ast(tokens[1:])
