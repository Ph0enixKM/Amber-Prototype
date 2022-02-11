from compiler.type import Type
from error import ErrorTypes, error_tok
from .syntax_module import Expression, SyntaxModule

class Function(SyntaxModule):
    def __init__(self):
        self.name = ''
        self.params = []
        self.block = None
        pass

    def ast(self, tokens):
        if len(tokens) >= 5:
            [fun, name, *rest] = tokens
            if fun.word != 'fun':
                return None
            self.name = name.word
            if rest[0].word != '(':
                error_tok(rest[0], 'Expected "(" symbol')
            if SyntaxModule.memory.has_double_fun(self.name):
                error_tok(rest[0], f'Function "{self.name}" already exists in this scope')
            SyntaxModule.memory.add_fun(self.name)
            SyntaxModule.memory.enter_scope(fun_scope=True)
            while len(rest):
                rest = rest[1:]
                word = rest[0].word
                if word == ',':
                    continue
                if word == ')':
                    break
                if self.is_variable_name(rest[0]):
                    self.params.append(word)
                    SyntaxModule.memory.add_variable(word, Type.Text)
                else:
                    error_tok(rest[0], ErrorTypes.VAR.value)
            (self.block, rest) = self.parse_block(rest[1:])
            SyntaxModule.memory.leave_scope()
            return rest

    def translate(self):
        params = []
        for index, param in enumerate(self.params):
            params.append(f'local {param}=${index + 1}')
        body = [
            f'function {self.name} {{',
            *params,
            self.block.translate(),
            '}'
        ]
        return '\n'.join(body)

class FunctionCall(SyntaxModule):
    def __init__(self):
        self.name = ''
        self.shell = False
        self.params = []

    def ast(self, tokens):
        if len(tokens) >= 3:
            if tokens[0].word == 'sh':
                self.shell = True
                tokens = tokens[1:]
            [fun, *rest] = tokens
            is_var = self.is_variable_name(fun)
            if not is_var or rest[0].word != '(':
                return None
            if not SyntaxModule.memory.has_fun(fun.word) and not self.shell:
                error_tok(rest[0], f'Function "{fun.word}" does not exist')
            self.name = fun.word
            rest = rest[1:]
            while len(rest):
                word = rest[0].word
                if word == ',':
                    rest = rest[1:]
                    continue
                if word == ')':
                    break
                param = Expression()
                rest = param.ast(rest)
                if not rest:
                    return None
                self.params.append(param)
            return rest[1:]

    def translate(self):
        params = [param.arraify() for param in self.params]
        return f'$({self.name} {" ".join(params)})'


class FunctionCallStatement(SyntaxModule):
    def __init__(self):
        self.name = ''
        self.shell = False
        self.params = []

    def ast(self, tokens):
        if len(tokens) >= 3:
            if tokens[0].word == 'sh':
                self.shell = True
                tokens = tokens[1:]
            [fun, *rest] = tokens
            is_var = self.is_variable_name(fun)
            if not is_var or rest[0].word != '(':
                return None
            if not SyntaxModule.memory.has_fun(fun.word) and not self.shell:
                error_tok(rest[0], f'Function "{fun.word}" does not exist')
            self.name = fun.word
            rest = rest[1:]
            while len(rest):
                word = rest[0].word
                if word == ',':
                    rest = rest[1:]
                    continue
                if word == ')':
                    break
                param = Expression()
                rest = param.ast(rest)
                if not rest:
                    return None
                self.params.append(param)
            return rest[1:]

    def translate(self):
        params = [param.arraify() for param in self.params]
        return f'{self.name} {" ".join(params)}'

class Return(SyntaxModule):
    def __init__(self):
        self.value = None

    def ast(self, tokens):
        if len(tokens):
            if tokens[0].word != 'return':
                return None
            if not SyntaxModule.memory.is_fun_context():
                error_tok(tokens[0], 'Return can only be used inside of functions')
            tokens = tokens[1:]
            if tokens[0].word != '\n':
                self.value = Expression()
                tokens = self.value.ast(tokens)
            return tokens
    
    def translate(self):
        if self.value:
            normalized = SyntaxModule.compute.truncate(self.value.numberify())
            return f'return {normalized}'
        return 'return'
    