from .syntax_module import SyntaxModule, Expression


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
            self.variable = name.word
            self.expr = Expression()
            return self.expr.ast(rest)


class ShorthandSum(SyntaxModule):
    def __init__(self):
        self.variable = None
        self.expr = None
    
    def ast(self, tokens):
        res = self.parse_shorthand_assignment(tokens, '+')
        (self.variable, self.expr, tokens) = res
        return tokens


class ShorthandSub(SyntaxModule):
    def __init__(self):
        self.variable = None
        self.expr = None
    
    def ast(self, tokens):
        res = self.parse_shorthand_assignment(tokens, '-')
        (self.variable, self.expr, tokens) = res
        return tokens


class ShorthandMul(SyntaxModule):
    def __init__(self):
        self.variable = None
        self.expr = None
    
    def ast(self, tokens):
        res = self.parse_shorthand_assignment(tokens, '*')
        (self.variable, self.expr, tokens) = res
        return tokens


class ShorthandDiv(SyntaxModule):
    def __init__(self):
        self.variable = None
        self.expr = None
    
    def ast(self, tokens):
        res = self.parse_shorthand_assignment(tokens, '/')
        (self.variable, self.expr, tokens) = res
        return tokens


class ShorthandMod(SyntaxModule):
    def __init__(self):
        self.variable = None
        self.expr = None
    
    def ast(self, tokens):
        res = self.parse_shorthand_assignment(tokens, '%')
        (self.variable, self.expr, tokens) = res
        return tokens
