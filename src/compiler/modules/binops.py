from compiler.systems.compute import Compute
from .syntax_module import SyntaxModule, Expression
from ..type import Type


class Sum(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['+'])
        return tokens
    
    @staticmethod
    def sum_eval(left, right):
        # Booleans are numbers
        if Type.Boolean in [left, right]:
            return Type.Number
        # If the types match, we return the type
        if left == right:
            return right
        # If we add to the Text - let it remain text
        if left == Type.Text:
            return left
        # Otherwise it's just a number
        return Type.Number
    
    def type_eval(self):
        return Sum.sum_eval(self.left.type_eval(), self.right.type_eval())
    
    def translate(self):
        sum_type = Sum.sum_eval(self.left.type_eval(), self.right.type_eval())
        # Number case
        if sum_type == Type.Number:
            left = self.left.numberify()
            right = self.right.numberify()
            return SyntaxModule.compute.binop(left, '+', right)
        # Array case
        if sum_type == Type.Array:
            left = self.left.arraify()
            right = self.right.arraify()
            return f'{left} {right}'
        # String case
        return f'{self.left.stringify()} + {self.right.stringify()}'


class Sub(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['-'])
        return tokens
    
    def type_eval(self):
        return Type.Number
    
    def translate(self):
        left = self.left.numberify()
        right = self.right.numberify()
        return SyntaxModule.compute.binop(left, '-', right)


class Mul(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['*'])
        return tokens
    
    def type_eval(self):
        return Type.Number
    
    def translate(self):
        left = self.left.numberify()
        right = self.right.numberify()
        return SyntaxModule.compute.binop(left, '*', right)


class Div(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['/'])
        return tokens
    
    def type_eval(self):
        return Type.Number
    
    def translate(self):
        left = self.left.numberify()
        right = self.right.numberify()
        return SyntaxModule.compute.binop(left, '/', right)


class Mod(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['%'])
        return tokens
    
    def type_eval(self):
        return Type.Number
    
    def translate(self):
        left = self.left.numberify()
        right = self.right.numberify()
        return SyntaxModule.compute.binop(left, '%', right)


class Eq(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['=', '='])
        return tokens
    
    def type_eval(self):
        return Type.Boolean
    
    def translate(self):
        left = self.left.numberify()
        right = self.right.numberify()
        return SyntaxModule.compute.binop(left, '==', right)


class Neq(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['!', '='])
        return tokens
    
    def type_eval(self):
        return Type.Boolean
    
    def translate(self):
        left = self.left.numberify()
        right = self.right.numberify()
        return SyntaxModule.compute.binop(left, '!=', right)


class Gt(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['>'])
        return tokens
    
    def type_eval(self):
        return Type.Boolean
    
    def translate(self):
        left = self.left.numberify()
        right = self.right.numberify()
        return SyntaxModule.compute.binop(left, '>', right)


class Gte(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['>', '='])
        return tokens
    
    def type_eval(self):
        return Type.Boolean
    
    def translate(self):
        left = self.left.numberify()
        right = self.right.numberify()
        return SyntaxModule.compute.binop(left, '>=', right)


class Lt(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['<'])
        return tokens
    
    def type_eval(self):
        return Type.Boolean
    
    def translate(self):
        left = self.left.numberify()
        right = self.right.numberify()
        return SyntaxModule.compute.binop(left, '<', right)


class Lte(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['<', '='])
        return tokens

    def type_eval(self):
        return Type.Boolean
    
    def translate(self):
        left = self.left.numberify()
        right = self.right.numberify()
        return SyntaxModule.compute.binop(left, '<', right)


class And(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['and'])
        return tokens
    
    def type_eval(self):
        return Type.Boolean
    
    def translate(self):
        left = self.left.numberify()
        right = self.right.numberify()
        return SyntaxModule.compute.binop(left, '&&', right)


class Or(SyntaxModule):
    def __init__(self):
        self.left = None
        self.right = None
    
    def ast(self, tokens):
        (self.left, self.right, tokens) = self.parse_binop(tokens, ['or'])
        return tokens
    
    def type_eval(self):
        return Type.Boolean
    
    def translate(self):
        left = self.left.numberify()
        right = self.right.numberify()
        return SyntaxModule.compute.binop(left, '||', right)


class Not(SyntaxModule):
    def __init__(self):
        self.expr = None
    
    def ast(self, tokens):
        if len(tokens) > 1:
            if tokens[0].word == 'not':
                self.expr = Expression()
                return self.expr.ast(tokens[1:])
    
    def type_eval(self):
        return Type.Boolean
    
    def translate(self):
        expr = self.expr.numberify()
        return SyntaxModule.compute.unop('!', expr)
