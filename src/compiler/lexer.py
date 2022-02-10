from .tok import Token
from .file_iterator import FileIterator
from .rules import Rules
from .closures import ClosureStack


class Lexer:
    def __init__(self, code):
        self.symbols = [
            '\n', '\'', '{', '}',
            '(', ')', '[', ']',
            '*', '+', '=', '-',
            '%', ':', ',', '#',
            '$', '\''
        ]
        self.closures = ClosureStack()
        self.code = code
        self.pos = FileIterator()
        self.rules = Rules(self.code, self.pos)
        self.lexem = []
        self.word = ''
        region_error = self.lexer()
        closure_error = self.asi()
        # TODO: Handle errors

    def add_word(self, same_line = False):
        if len(self.word):
            self.lexem.append(
                Token(*self.pos.get(len(self.word) - same_line), self.word))
            self.word = ''

    def lexer(self):
        for letter in self.code:
            new_rule = self.rules.handle_rule()
            if not new_rule and self.rules.is_region():
                if self.rules.get_region().name != 'comment':
                    self.word += letter
            else:
                if letter in [' ', '\t', '#']:
                    self.add_word()
                elif letter in self.symbols:
                    self.add_word()
                    self.word += letter
                    self.add_word(True)
                else:
                    self.word += letter
            self.pos.next(letter)
        self.add_word()
        if not self.rules.is_base_region():
            return self.lexem[-1]

    def asi(self):
        stack = []
        new_lexem = []
        for token in self.lexem:
            if token.word in self.closures.opening:
                stack.append(self.closures.get_by_opening(token.word))
            if token.word in self.closures.closing:
                closing = stack[-1]
                if token.word == closing.closing:
                    stack.pop()
                else:
                    return token
            if not(len(stack) and token.word == '\n'):
                new_lexem.append(token)
        if len(stack):
            return new_lexem[-1]
        self.lexem = new_lexem
        return False
    
    def get(self):
        return self.lexem

if __name__ == '__main__':
    def test_positioner(code, lexem):
        lines = code.split('\n')
        for token in lexem:
            if token.word == '\n':
                continue
            word = token.word
            row = token.row
            col = token.col
            lookup = lines[row - 1][col - 1:col - 1 + len(word)]
            if word != lookup:
                return (
                    False,
                    f'({word}) vs ({lookup}) [{row}:{col}]'
                )
        return (True, '')

    code = [
        'let test a  this   = 12',
        'if a == 12 {',
        '    $ echo \'hello this {test} beautiful world\'',
        '}'
    ]
    lexem = Lexer('\n'.join(code))
    # TODO: Create testing utility to display 
    # successfull and unsuccessfull tests
    print(test_positioner('\n'.join(code), lexem.get()))
