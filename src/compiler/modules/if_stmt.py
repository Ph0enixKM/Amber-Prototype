from .syntax_module import SyntaxModule, Expression
from .parenthesis import Parenthesis

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
            if len(rest) and rest[0].word == 'else':
                (self.block_false, rest) = self.parse_block(rest[1:])
                return rest
            return rest
    
    def translate(self):
        result = []
        if self.block_true:
            cond = self.condition.numberify()
            cond = Parenthesis.remove_outer_parenthesis(cond)
            result.append(f'if [ {cond} != 0 ]; then')
            result.append(self.block_true.translate())
        if self.block_false:
            result.append(f'else')
            result.append(self.block_false.translate())
        result.append('fi')
        return '\n'.join(result)
