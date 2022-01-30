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
                (self.block, tokens) = self.parse_block(tokens)
                return tokens
            # For loop
            is_var = self.is_variable_name(tokens[0].word)
            if is_var and tokens[1].word == 'in':
                self.iterator = tokens[0].word
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
