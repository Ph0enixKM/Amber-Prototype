from compiler.modules.parenthesis import Parenthesis
from compiler.type import Type
from error import error_tok
from .syntax_module import SyntaxModule, Expression
from .data_types import Boolean


class Loop(SyntaxModule):
    def __init__(self):
        self.while_loop = False
        self.condition = None
        self.iterator = ''
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
                (self.block, tokens) = self.parse_block(tokens, loop_scope=True)
                return tokens
            # For loop
            is_var = self.is_variable_name(tokens[0].word)
            if is_var and tokens[1].word == 'in':
                self.iterator = tokens[0].word
                tokens = tokens[1:]
                self.iterable = Expression()
                tokens = self.iterable.ast(tokens[1:])
                SyntaxModule.memory.enter_scope()
                SyntaxModule.memory.add_variable(self.iterator, Type.Text)
                (self.block, tokens) = self.parse_block(tokens, loop_scope=True)
                SyntaxModule.memory.leave_scope()
                return tokens
            # While loop
            self.while_loop = True
            self.condition = Expression()
            tokens = self.condition.ast(tokens)
            (self.block, tokens) = self.parse_block(tokens, loop_scope=True)
            return tokens
    
    def translate(self):
        # While true loop
        header = ''
        # For loop
        if not self.while_loop:
            header = f'for {self.iterator} in {self.iterable.arraify()}\ndo'
        # While loop
        if self.while_loop:
            cond = self.condition.numberify()
            cond = Parenthesis.remove_outer_parenthesis(cond)
            header = f'while [ {cond} != 0 ]; do'
        # Body
        block = self.block.translate()
        return '\n'.join([
            header, block, 'done'
        ])


class Break(SyntaxModule):
    def ast(self, tokens):
        if len(tokens):
            if tokens[0].word != 'break':
                return None
            if not SyntaxModule.memory.is_loop_context():
                error_tok(tokens[0], 'Break statements can only be used in a loop context')
            return tokens[1:]
    
    def translate(self):
        return 'break'


class Continue(SyntaxModule):
    def ast(self, tokens):
        if len(tokens):
            if tokens[0].word != 'continue':
                return None
            if not SyntaxModule.memory.is_loop_context():
                error_tok(tokens[0], 'Continue statements can only be used in a loop context')
            return tokens[1:]
    
    def translate(self):
        return 'continue'
