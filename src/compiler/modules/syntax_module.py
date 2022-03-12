from ..mem import Memory
from ..systems.compute import Compute


class SyntaxModule:
    memory = Memory()
    compute = Compute()
    reserved_variable = '__'

    def __init__(self):
        pass
    
    def ast(self, tokens):
        raise 'Undefined Syntax (Conversion to AST)'

    def validate(self):
        raise 'Undefined Syntax (AST Validation)'
    
    def translate(self):
        raise 'Undefined Syntax (AST Translation)'
    
    def type_eval(self):
        return None

    def stringify(self):
        return self.translate()
    
    def numberify(self):
        return self.translate()
    
    def arraify(self):
        return self.translate()

    def is_variable_name(self, token, error=False):
        reserved = SyntaxModule.reserved_variable
        name = token.word
        throw = lambda exc: error_tok(token, exc) if error else False
        if name[:2] == reserved:
            return throw(f'Variable name cannot start with "{reserved}"')
        is_alpha = lambda l: l.isalpha() or l in ['_']
        if not is_alpha(name[0]):
            return throw('Variable name cannot start with a digit')
        for letter in name[1:]:
            if not is_alpha(letter) and not letter.isdigit():
                return False
        return True
    
    def parse_block(self, tokens, loop_scope=False):
        if len(tokens) >= 2:
            block = Block(loop_scope)
            # Multiline block
            if tokens[0].word == '{':
                if tokens[1].word != '\n':
                    error_tok(tokens[0], ErrorTypes.ENTER.value)
                res = block.ast(tokens[2:])
                return (block, res)
            # Singleline block
            if tokens[0].word == ':':
                tokens = tokens[1:]
            tokens = self.clear_empty_lines(tokens)
            SyntaxModule.memory.enter_scope(loop_scope=loop_scope)
            st = Statement()
            res = st.ast(tokens)
            block.statements.append(st)
            SyntaxModule.memory.leave_scope()
            return (block, res)
        return (None, None)

    def parse_shorthand_assignment(self, tokens, op):
        def array_shorthand(tokens, op):
            if len(tokens) >= 6:
                variable = ArraySubscription()
                rest = variable.ast(tokens)
                if rest and op:
                    if rest[0].word != op:
                        return (None, None, None)
                    rest = rest[1:]
                if not rest or rest[0].word != '=':
                    return (None, None, None)
                expr = Expression()
                rest = expr.ast(rest[1:])
                new_type = expr.type_eval()
                SyntaxModule.memory.update_variable(variable.name, new_type)
                return (variable, expr, rest)
            return (None, None, None)
        def variable_shorthand(tokens, op):
            if len(tokens) >= 3:
                name = tokens[0]
                is_var = self.is_variable_name(name)
                tokens = tokens[1:]
                if not is_var:
                    return (None, None, None)
                if op:
                    if op != tokens[0].word:
                        return (None, None, None)
                    tokens = tokens[1:]
                if tokens[0].word != '=':
                    return (None, None, None)
                variable = VariableReference(name.word)
                expr = Expression()
                tokens = expr.ast(tokens[1:])
                new_type = expr.type_eval()
                SyntaxModule.memory.update_variable(name.word, new_type)
                return (variable, expr, tokens)
            return (None, None, None)
        arr = array_shorthand(tokens, op)
        if arr[0]:
            return arr
        var = variable_shorthand(tokens, op)
        return var
    
    def translate_variable_statement(self, variable):
        if isinstance(variable, VariableReference):
            return f'{variable.name}'
        elif isinstance(variable, ArraySubscription):
            index = SyntaxModule.compute.truncate(variable.index.numberify())
            prefix = SyntaxModule.reserved_variable
            helper_var = f'{prefix}{variable.name}={index}'
            main_var = f'{variable.name}[${prefix}{variable.name}]'
            return '\n'.join([helper_var, main_var])
        return

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
                    # Omit shorthand operations
                    if tokens[index + len(ops)].word == '=':
                        return None
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
    def __init__(self, loop_scope=False):
        self.statements = []
        self.loop_scope = loop_scope
    
    def leave_block(self, tokens):
        SyntaxModule.memory.leave_scope()
        if len(SyntaxModule.memory.scopes) and not len(self.statements):
            error_tok(tokens[0], 'Scope cannot be empty')

    def ast(self, tokens):
        rest = tokens
        SyntaxModule.memory.enter_scope(self.loop_scope)
        while len(rest):
            rest = self.clear_empty_lines(rest)
            # End of line feed
            if not len(rest):
                self.leave_block(tokens)
                return []
            # End of current block
            if rest[0].word == '}':
                self.leave_block(tokens)
                return rest[1:]
            st = Statement()
            res = st.ast(rest)
            # Error predicates
            is_none = res == None
            is_unchanged = len(res) == len(rest)
            # Detect any error
            if is_none or is_unchanged:
                error_tok(rest[0], ErrorTypes.UNDEF.value)
            self.statements.append(st)
            rest = res
            if len(rest) and not (rest[0].word in ['\n', '}']):
                error_tok(rest[0], 'New line expected')
    
    def translate(self):
        return '\n'.join([st.translate() for st in self.statements])


class Statement(SyntaxModule):
    def __init__(self):
        self.expr = None
        self.modules = [
            Variable, If, Loop,
            Assignment, ShorthandSum, ShorthandSub,
            ShorthandMul, ShorthandDiv, ShorthandMod,
            StatementShell, Continue, Break,
            Function, FunctionCallStatement, Expression
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
            Or, And,
            Eq, Neq, Gt, Gte, Lt, Lte,
            Sum, Sub, Mul, Div, Mod, Not, Return, Range,
            Parenthesis, FunctionCall, Number, Text, Boolean,
            ArraySubscription, ShellCommand, ShellStatus, Array,
            VariableReference
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

    def type_eval(self):
        return self.expr.type_eval()

    def translate(self):
        return self.expr.translate()
    
    def numberify(self):
        return self.expr.numberify()
    
    def stringify(self):
        return self.expr.stringify()
    
    def arraify(self):
        return self.expr.arraify()

# Imports at the bottom prevents
# recursive importing
from copy import copy
from error import error_tok, ErrorTypes
from ..closures import ClosureStack
from .assignment import *
from .binops import *
from .data_types import *
from .if_stmt import *
from .loop import *
from .parenthesis import *
from .shell_command import *
from .variables import *
from .function import *