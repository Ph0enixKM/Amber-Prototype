from .syntax_module import SyntaxModule, Expression


class SilentShell(SyntaxModule):
    def __init__(self):
        self.expr = None
    
    def ast(self, tokens):
        if len(tokens) >= 3:
            if tokens[0].word != 'silent':
                return None
            self.expr = ShellCommand()
            return self.expr.ast(tokens[1:])


class ShellCommand(SyntaxModule):
    def __init__(self):
        self.types = ['status', 'error']
        self.type = ''
        self.commandlets = []
        self.interps = []
    
    def ignore(self):
        return ['types']
    
    def ast(self, tokens):
        if len(tokens) >= 2:
            if tokens[0].word in self.types:
                self.type = tokens[0].word
                tokens = tokens[1:]
            if tokens[0].word != '$':
                return None
            tokens = tokens[1:]
            while tokens[0].word != '$':
                if tokens[0].word == '{':
                    expr = Expression()
                    tokens = expr.ast(tokens[1:])
                    self.interps.append(expr)
                else:
                    self.commandlets.append(tokens[0].word)
                tokens = tokens[1:]
            return tokens[1:]
