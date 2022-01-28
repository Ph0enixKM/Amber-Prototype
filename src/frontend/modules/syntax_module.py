from copy import copy
from error import error_tok, ErrorTypes

class SyntaxModule:
    def __init__(self):
        pass
    
    def ast(self, tokens):
        raise 'Undefined Syntax (Conversion to AST)'

    def validate(self, ast):
        raise 'Undefined Syntax (AST Validation)'
    
    def translate(self, ast):
        raise 'Undefined Syntax (AST Translation)'
    
    def ignore(self):
        return []
    
    def generate_tree(self):
        kind = self.__class__.__name__
        root = copy(self.__dict__)
        new = { 'kind': kind }
        ignored = self.ignore()
        if 'kind' in root:
            raise Exception(f'\'Kind\' is a reserved field (used in {kind})')
        for item in root:
            if item in ignored:
                continue
            if isinstance(root[item], SyntaxModule):
                new[item] = root[item].generate_tree()
            elif isinstance(root[item], list):
                new[item] = list(map(
                    lambda item: item.generate_tree()
                        if isinstance(item, SyntaxModule) 
                        else item, root[item]))
            else:
                new[item] = root[item]
        return new

class Block(SyntaxModule):
    def __init__(self):
        self.statements = []

    def ast(self, tokens):
        while len(tokens):
            st = Statement()
            res = st.ast(tokens)
            # Error predicates
            is_none = res == None
            is_unchanged = len(res) == len(tokens)
            is_not_end_line = len(res) and res[0].word != '\n'
            # Detect any error
            if is_none or is_unchanged or is_not_end_line:
                row = tokens[0].row
                col = tokens[0].col
                error(f'Undefined Syntax at {row}:{col}')
            self.statements.append(st)
            tokens = res[1:]
            if not len(res):
                return []


class Statement(SyntaxModule):
    def __init__(self):
        self.modules = [Variable, Expression]
    
    def ignore(self):
        return ['modules']

    def ast(self, tokens):
        for module in self.modules:
            mod = module()
            res = mod.ast(tokens)
            if res != None:
                self.expr = mod
                return res
        error_tok(tokens[0], ErrorTypes.UNDEF.value)

class Expression(SyntaxModule):
    def __init__(self):
        self.modules = [Number, String]
    
    def ignore(self):
        return ['modules']

    def ast(self, tokens):
        for module in self.modules:
            mod = module()
            res = mod.ast(tokens)
            if res != None:
                self.expr = mod
                return res
        error_tok(tokens[0], ErrorTypes.UNDEF.value)

class Number(SyntaxModule):
    def positive(self, tokens):
        if len(tokens) >= 1:
            self.value = tokens[0].word
            if not self.value.replace('.', '', 1).isdigit():
                return None
            return tokens[1:]
    
    def negative(self, tokens):
        if len(tokens) >= 2:
            [minus, value, *rest] = tokens
            if minus.word != '-':
                return None
            if not value.replace('.', '', 1).isdigit():
                return None
            self.value = value
            return rest

    def ast(self, tokens):
        return self.negative(tokens) or self.positive(tokens)
        

class Variable(SyntaxModule):
    def ast(self, tokens):
        if len(tokens) > 3:
            [key, name, eq, *exp] = tokens
            if key.word != 'box' or eq.word != '=':
                return None
            self.name = name.word
            self.expr = Expression()
            return self.expr.ast(exp)

class String(SyntaxModule):
    def __init__(self):
        self.stringlets = []
        self.interps = [] 

    def ast(self, tokens):
        if len(tokens) >= 3:
            if tokens[0].word != '\'':
                return None
            tokens = tokens[1:]
            while tokens[0].word != '\'':
                self.stringlets.append(tokens[0].word)
                if tokens[0].word == '{':
                    expr = Expression()
                    tokens = expr.ast(tokens[1:])
                    self.interps.append(expr)
                tokens = tokens[1:]
            return tokens[1:]
                
                    

            