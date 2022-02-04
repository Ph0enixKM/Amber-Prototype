from compiler.modules.data_types import Number
from compiler.type import Type
from .syntax_module import SyntaxModule, Expression


class StatementShell(SyntaxModule):
    def __init__(self):
        self.expr = None
        self.silent = False
    
    def ast(self, tokens):
        if len(tokens) >= 3:
            if tokens[0].word == 'silent':
                self.silent = True
                tokens = tokens[1:]
            if tokens[0].word != '$':
                return None
            self.expr = ShellCommand()
            return self.expr.ast(tokens)

    def translate(self):
        if self.silent:
            return f'{self.expr.translate(True)} > /dev/null 2>&1'
        return self.expr.translate(True)


class ShellCommand(SyntaxModule):
    def __init__(self):
        self.types = ['error']
        self.interp_map = []
        self.type = ''
        self.commandlets = []
        self.interps = []
    
    def ignore(self):
        return ['types', 'interp_map']
    
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
                    self.interp_map.append(True)
                else:
                    self.commandlets.append(tokens[0].word)
                    self.interp_map.append(False)
                tokens = tokens[1:]
            return tokens[1:]
    
    def type_eval(self):
        return Type.Text
    
    def translate(self, raw=False):
        interps = [interp.translate() for interp in self.interps]
        commandlets = [command for command in self.commandlets]
        res = []
        for id in self.interp_map:
            if id:
                res.append(interps[0])
                interps = interps[1:]
            else:
                command = (commandlets[0]
                    .replace('$', '\\$')
                    .replace('`', '\\`')
                    .replace('"', '\\"'))
                res.append(command)
                commandlets = commandlets[1:]
        if raw:
            return ''.join(res)
        if self.type == 'error':
            return ''.join(['$(', *res, ' 2>&1', ')'])
        return ''.join(['$(', *res, ')'])


class ShellStatus(SyntaxModule):
    def __init__(self):
        pass
    
    def ast(self, tokens):
        if len(tokens) >= 1:
            if tokens[0].word != 'status':
                return None
            return tokens[1:]
    
    def type_eval(self):
        return Type.Number

    def translate(self):
        return '$?'