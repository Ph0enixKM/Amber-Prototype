from cmath import log
from error import error_tok, ErrorTypes
from .syntax_module import SyntaxModule, Expression
from ..type import Type


class Number(SyntaxModule):
    def __init__(self):
        self.value = 0

    def positive(self, tokens):
        if len(tokens) >= 1:
            if not tokens[0].word.replace('.', '', 1).isdigit():
                return None
            self.value = float(tokens[0].word)
            return tokens[1:]
    
    def negative(self, tokens):
        if len(tokens) >= 2:
            [minus, value, *rest] = tokens
            if minus.word != '-':
                return None
            if not value.word.replace('.', '', 1).isdigit():
                return None
            self.value = -float(value.word)
            return rest

    def ast(self, tokens):
        return self.negative(tokens) or self.positive(tokens)
    
    def type_eval(self):
        return Type.Number

    def translate(self):
        return str(self.value).rstrip('0').rstrip('.')


class Boolean(SyntaxModule):
    def __init__(self):
        self.value = False
    
    def ast(self, tokens):
        if len(tokens):
            if not (tokens[0].word in ['true', 'false']):
                return None
            self.value = tokens[0].word == 'true'
            return tokens[1:]
    
    def type_eval(self):
        return Type.Boolean

    def translate(self):
        return '1' if self.value else '0'


class Text(SyntaxModule):
    def __init__(self):
        self.interp_map = []
        self.stringlets = []
        self.interps = []
        self.tok = None
    
    def ignore(self):
        return ['interp_map', 'tok']

    def ast(self, tokens):
        if len(tokens) >= 3:
            if tokens[0].word != '\'':
                return None
            tokens = tokens[1:]
            while tokens[0].word != '\'':
                if tokens[0].word == '{':
                    expr = Expression()
                    tokens = expr.ast(tokens[1:])
                    self.interps.append(expr)
                    self.interp_map.append(True)
                else:
                    self.stringlets.append(tokens[0].word)
                    self.interp_map.append(False)
                tokens = tokens[1:]
            return tokens[1:]
    
    def translate(self):
        interps = [interp.translate() for interp in self.interps]
        stringlets = [string for string in self.stringlets]
        res = []
        for id in self.interp_map:
            if id:
                res.append(interps[0])
                interps = interps[1:]
            else:
                string = (stringlets[0]
                    .replace('$', '\\$')
                    .replace('`', '\\`')
                    .replace('"', '\\"'))
                res.append(string)
                stringlets = stringlets[1:]
        return ''.join(['"', *res, '"'])
    
    def type_eval(self):
        return Type.Text
    
    def numberify(self):
        return str(len(self.translate()) - 2)


class Array(SyntaxModule):
    def __init__(self):
        self.values = []
    
    def ast(self, tokens):
        if len(tokens) > 1:
            if tokens[0].word != '[':
                return None
            tokens = tokens[1:]
            while len(tokens):
                exp = Expression()
                tokens = exp.ast(tokens)
                self.values.append(exp)
                if tokens[0].word == ',':
                    tokens = tokens[1:]
                    continue
                if tokens[0].word != ']':
                    return error_tok(tokens[0], ErrorTypes.UNDEF.value)
                return tokens[1:]

    def type_eval(self):
        return Type.Array

    def translate(self):
        vals = [val.stringify() for val in self.values]
        return f'({" ".join(vals)})'

    def stringify(self):
        vals = [val.stringify() for val in self.values]
        return f'\'{" ".join(vals)}\''

    def numberize(self):
        return str(len(self.values))

    def booleanize(self):
        return f'[ {self.numberify()} != 0 ]'
    
    def arraify(self):
        vals = [val.stringify() for val in self.values]
        return ' '.join(vals)


class Range(SyntaxModule):
    is_range = False

    def __init__(self):
        self.expr_from = None
        self.expr_to = None
    
    def ast(self, tokens):
        if len(tokens) > 2 and not Range.is_range:
            Range.is_range = True
            self.expr_from = Expression()
            tokens = self.expr_from.ast(tokens)
            if not len(tokens) or tokens[0].word != 'to':
                Range.is_range = False
                return None
            self.expr_to = Expression()
            Range.is_range = False
            return self.expr_to.ast(tokens[1:])

    def type_eval(self):
        return Type.Array

    def translate(self):
        start = SyntaxModule.compute.truncate(self.expr_from.translate())
        end = SyntaxModule.compute.truncate(self.expr_to.translate())
        return f'$(seq {start} {end})'
