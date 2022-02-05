from numpy import var
from error import error_tok
from .syntax_module import SyntaxModule, Expression
from ..type import Type
from .binops import Sum


class Assignment(SyntaxModule):
    def __init__(self):
        self.variable = None
        self.expr = None
    
    def ast(self, tokens):
        if len(tokens) >= 3:
            [name, eq, *rest] = tokens
            is_var = self.is_variable_name(name.word)
            if not is_var or eq.word != '=':
                return None
            if not SyntaxModule.memory.has_variable(name.word):
                error_tok(name, f'Variable {name.word} does not exists in this scope')
            self.variable = name.word
            self.expr = Expression()
            rest = self.expr.ast(rest)
            new_type = self.expr.type_eval()
            SyntaxModule.memory.update_variable(name.word, new_type)
            return rest
    
    def translate(self):
        return f'{self.variable}={self.expr.translate()}'


class ShorthandSum(SyntaxModule):
    def __init__(self):
        self.variable = None
        self.expr = None
    
    def ast(self, tokens):
        res = self.parse_shorthand_assignment(tokens, '+')
        (self.variable, self.expr, tokens) = res
        return tokens
    
    def translate(self):
        sum_type = Sum.sum_eval(self.variable.var_type, self.expr.type_eval())
        # Number case
        if sum_type == Type.Number:
            variable = self.variable.numberify()
            expr = self.expr.numberify()
            calc = SyntaxModule.compute.binop(variable, '+', expr)
            return f'{self.variable.name}={calc}'
        # Array case
        if sum_type == Type.Array:
            variable = self.variable.arraify()
            expr = self.expr.arraify()
            return f'{self.variable.name}=({variable} {expr})'
        # String case
        return f'{self.variable.name}+={self.expr.stringify()}'


class ShorthandSub(SyntaxModule):
    def __init__(self):
        self.variable = None
        self.expr = None
    
    def ast(self, tokens):
        res = self.parse_shorthand_assignment(tokens, '-')
        (self.variable, self.expr, tokens) = res
        return tokens
    
    def translate(self):
        variable = self.variable.numberify()
        expr = self.expr.numberify()
        calc = SyntaxModule.compute.binop(variable, '-', expr)
        return f'{self.variable.name}={calc}'


class ShorthandMul(SyntaxModule):
    def __init__(self):
        self.variable = None
        self.expr = None
    
    def ast(self, tokens):
        res = self.parse_shorthand_assignment(tokens, '*')
        (self.variable, self.expr, tokens) = res
        return tokens
    
    def translate(self):
        variable = self.variable.numberify()
        expr = self.expr.numberify()
        calc = SyntaxModule.compute.binop(variable, '*', expr)
        return f'{self.variable.name}={calc}'


class ShorthandDiv(SyntaxModule):
    def __init__(self):
        self.variable = None
        self.expr = None
    
    def ast(self, tokens):
        res = self.parse_shorthand_assignment(tokens, '/')
        (self.variable, self.expr, tokens) = res
        return tokens
    
    def translate(self):
        variable = self.variable.numberify()
        expr = self.expr.numberify()
        calc = SyntaxModule.compute.binop(variable, '/', expr)
        return f'{self.variable.name}={calc}'


class ShorthandMod(SyntaxModule):
    def __init__(self):
        self.variable = None
        self.expr = None
    
    def ast(self, tokens):
        res = self.parse_shorthand_assignment(tokens, '%')
        (self.variable, self.expr, tokens) = res
        return tokens
    
    def translate(self):
        variable = self.variable.numberify()
        expr = self.expr.numberify()
        calc = SyntaxModule.compute.binop(variable, '%', expr)
        return f'{self.variable.name}={calc}'
