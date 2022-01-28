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

    def is_variable_name(self, name):
        is_alpha = lambda l: l.isalpha() or l in ['_', '$']
        if not is_alpha(name[0]):
            return False
        for letter in name[1:]:
            if not is_alpha(letter) and not letter.isdigit():
                return False
        return True
    
    def parse_block(self, tokens):
        if len(tokens) >= 2:
            block = Block()
            # Multiline block
            if tokens[0].word == '{':
                if tokens[1].word != '\n':
                    error_tok(tokens[0], ErrorTypes.ENTER.value)
                res = block.ast(tokens[2:])
                return (block, res)
            # Singleline block
            elif tokens[0].word == ':':
                st = Statement()
                res = st.ast(tokens[1:])
                block.statements.append(st)
                return (block, res)
        return (None, None)
    
    def clear_empty_lines(self, tokens):
        while len(tokens) and tokens[0].word == '\n':
            tokens = tokens[1:]
        return tokens

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
            tokens = self.clear_empty_lines(tokens)
            # End of line feed
            if not len(tokens):
                return []
            # End of current block
            if tokens[0].word == '}':
                return tokens[1:]
            st = Statement()
            res = st.ast(tokens)
            # Error predicates
            is_none = res == None
            is_unchanged = len(res) == len(tokens)
            # Detect any error
            if is_none or is_unchanged:
                error_tok(tokens[0], ErrorTypes.UNDEF.value)
            self.statements.append(st)
            tokens = res


class Statement(SyntaxModule):
    def __init__(self):
        self.modules = [Variable, If, Loop, Expression]
    
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
        self.modules = [Number, String, Boolean, Array, VariableReference]
    
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


class Boolean(SyntaxModule):
    def __init__(self):
        self.value = False
    
    def ast(self, tokens):
        if len(tokens):
            if not (tokens[0].word in ['true', 'false']):
                return None
            self.value = tokens[0].word == 'true'
            return tokens[1:]

class Variable(SyntaxModule):
    def __init__(self):
        self.name = ''
        self.expr = None

    def ast(self, tokens):
        if len(tokens) > 3:
            [key, name, eq, *exp] = tokens
            if key.word != 'box' or eq.word != '=':
                return None
            if not self.is_variable_name(name.word):
                error_tok(name, ErrorTypes.VAR.value)
            self.name = name.word
            self.expr = Expression()
            return self.expr.ast(exp)


class VariableReference(SyntaxModule):
    def __init__(self):
        self.name = ''
    
    def ast(self, tokens):
        if len(tokens):
            if not self.is_variable_name(tokens[0].word):
                return None
            self.name = tokens[0].word
            return tokens[1:]


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
                    

class Loop(SyntaxModule):
    def __init__(self):
        self.while_loop = False
        self.condition = None
        self.iterator = None
        self.iterable = None
        self.block = None
    
    def ast(self, tokens):
        if len(tokens) >= 4:
            if tokens[0].word != 'loop':
                return None
            tokens = tokens[1:]
            # While true loop
            if tokens[0].word == '{':
                self.condition = Boolean()
                self.condition.value = True
                self.while_loop = True
                (self.block, tokens) = self.parse_block(tokens)
                return tokens
            # For loop
            is_var = self.is_variable_name(tokens[0].word)
            if is_var and tokens[1].word == 'in':
                self.iterator = Variable()
                self.iterator.name = tokens[0].word
                tokens = tokens[1:]
                self.iterable = Expression()
                tokens = self.iterable.ast(tokens[1:])
                (self.block, tokens) = self.parse_block(tokens)
                return tokens
            # While loop
            self.while_loop = True
            self.condition = Expression()
            tokens = self.condition.ast(tokens)
            (self.block, tokens) = self.parse_block(tokens)
            return tokens


class If(SyntaxModule):
    def __init__(self):
        self.condition = None
        self.block_true = None
        self.block_false = None
    
    def ast(self, tokens):
        if len(tokens) > 5:
            [key, *rest] = tokens
            if key.word != 'if':
                return None
            self.condition = Expression()
            rest = self.condition.ast(rest)
            (self.block_true, rest) = self.parse_block(rest)
            rest = self.clear_empty_lines(rest)
            # Handle else
            if rest[0].word == 'else':
                (self.block_false, rest) = self.parse_block(rest[1:])
                return rest
            return rest
