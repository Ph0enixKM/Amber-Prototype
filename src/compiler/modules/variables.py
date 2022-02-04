from error import error_tok, ErrorTypes
from .syntax_module import SyntaxModule, Expression
from ..type import Type


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
            if SyntaxModule.memory.has_double_variable(name.word):
                error_tok(name, f'Variable {name.word} already exists in this scope')
            self.name = name.word
            self.expr = Expression()
            tokens = self.expr.ast(exp)
            SyntaxModule.memory.add_variable(name.word, self.expr.type_eval())
            return tokens
    
    def translate(self):
        return f'{self.name}={self.expr.translate()}'


class VariableReference(SyntaxModule):
    def __init__(self, known_name=None):
        self.name = ''
        self.var_type = None
        if known_name:
            self.name = known_name
            self.var_type = SyntaxModule.memory.get_variable_type(known_name)
    
    def ast(self, tokens):
        if len(tokens):
            name = tokens[0]
            if not self.is_variable_name(name.word):
                return None
            if not SyntaxModule.memory.has_variable(name.word):
                error_tok(name, f'Variable {name.word} does not exist in this scope')
            self.var_type = SyntaxModule.memory.get_variable_type(name.word)
            self.name = name.word
            return tokens[1:]
    
    def type_eval(self):
        return SyntaxModule.memory.get_variable_type(self.name)
    
    def translate(self):
        return f'${self.name}'
    
    def numberify(self):
        if self.var_type == Type.Text:
            return f'${{#{self.name}}}'
        elif self.var_type == Type.Array:
            return f'${{#{self.name}[@]}}'
        return self.translate()
    
    def arraify(self):
        return f'${{{self.name}[@]}}'
