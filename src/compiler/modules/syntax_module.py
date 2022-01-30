class SyntaxModule:
    def __init__(self):
        pass
    
    def ast(self, tokens):
        raise 'Undefined Syntax (Conversion to AST)'

    def validate(self):
        raise 'Undefined Syntax (AST Validation)'
    
    def translate(self):
        raise 'Undefined Syntax (AST Translation)'

    def is_variable_name(self, name):
        is_alpha = lambda l: l.isalpha() or l in ['_']
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
                tokens = self.clear_empty_lines(tokens[1:])
                st = Statement()
                res = st.ast(tokens)
                block.statements.append(st)
                return (block, res)
        return (None, None)

    def parse_shorthand_assignment(self, tokens, op):
        if len(tokens) >= 3:
            [name, oper, eq, *rest] = tokens
            is_var = self.is_variable_name(name.word)
            if not is_var or oper.word != op or eq.word != '=':
                return ('', None, None)
            variable = name.word
            expr = Expression()
            tokens = expr.ast(rest)
            return (variable, expr, tokens)
        return ('', None, None)

    def parse_binop(self, tokens, ops):
        def is_binop(tokens):
            closures = ClosureStack()
            for index, token in enumerate(tokens):
                gen = closures.iter(token)
                if token.word == '\n':
                    return None
                if token.word == ops[0]:
                    tokens_slice = tokens[index:index + len(ops)]
                    words = list(map(lambda t: t.word, tokens_slice))
                    if words == ops and not gen:
                        return index
        if len(tokens) >= 3:
            index = is_binop(tokens)
            if not index:
                return (None, None, None)
            left = Expression()
            left.ast(tokens[:index])
            offset = 0
            for op in ops:
                if tokens[index + offset].word != op:
                    return (None, None, None)
                offset += 1
            right = Expression()
            tokens = right.ast(tokens[index + len(ops):])
            return (left, right, tokens)
        return (None, None, None)

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
    
    def translate(self):
        return ''.join([st.translate() for st in self.statements])


class Statement(SyntaxModule):
    def __init__(self):
        self.expr = None
        self.modules = [
            Variable, If, Loop,
            Assignment, ShorthandSum, ShorthandSub,
            ShorthandMul, ShorthandDiv, ShorthandMod,
            SilentShell, Expression
        ]
    
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
    
    def translate(self):
        return self.expr.translate()


class Expression(SyntaxModule):
    def __init__(self):
        self.expr = None
        self.modules = [
            Parenthesis,
            Sum, Sub, Mul, Div, Mod, Not,
            Or, And, Eq, Neq, Gt, Gte, Lt, Lte,
            Number, String, Boolean, ShellCommand,
            Array, VariableReference, Comment
        ]
    
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

    def translate(self):
        return self.expr.translate()

# Imports at the bottom prevents
# recursive importing
from copy import copy
from error import error_tok, ErrorTypes
from ..closures import ClosureStack
from .assignment import *
from .binops import *
from .comment import *
from .data_types import *
from .if_stmt import *
from .loop import *
from .parenthesis import *
from .shell_command import *
from .variables import *
