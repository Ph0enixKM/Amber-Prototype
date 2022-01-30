from .syntax_module import SyntaxModule, Expression

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
