from error import error_tok
from .syntax_module import SyntaxModule, Expression
from ..type import Type
from .binops import Sum


class Assignment(SyntaxModule):
    def __init__(self):
        self.variable = None
        self.expr = None
    
    def ast(self, tokens):
        res = self.parse_shorthand_assignment(tokens, None)
        (self.variable, self.expr, tokens) = res
        return tokens
    
    def translate(self):
        var = self.translate_variable_statement(self.variable)
        return f'{var}={self.expr.translate()}'

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
        var = self.translate_variable_statement(self.variable)
        # Number case
        if sum_type == Type.Number:
            variable = self.variable.numberify()
            expr = self.expr.numberify()
            calc = SyntaxModule.compute.binop(variable, '+', expr)
            return f'{var}={calc}'
        # Array case
        if sum_type == Type.Array:
            variable = self.variable.arraify()
            expr = self.expr.arraify()
            return f'{var}=({variable} {expr})'
        # String case
        return f'{var}+={self.expr.stringify()}'


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
        var = self.translate_variable_statement(self.variable)
        return f'{var}={calc}'


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
        var = self.translate_variable_statement(self.variable)
        return f'{var}={calc}'


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
        var = self.translate_variable_statement(self.variable)
        return f'{var}={calc}'


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
        calc = SyntaxModule.compute.mod(variable, expr)
        var = self.translate_variable_statement(self.variable)
        return f'{var}={calc}'
