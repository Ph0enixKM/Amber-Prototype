from tok import Token
from file_iterator import FileIterator
from rules import Rules

symbols = ['\n', '\'', '{', '}', '(', ')', '*', '+', '=', '-', '%']

def lexer(code):
    pos = FileIterator()
    rules = Rules(code, pos)
    lexem = []
    word = ''

    def add_word(same_line = False):
        if len(word):
            lexem.append(Token(*pos.get(len(word) - same_line), word))
            return ''
        return word

    for letter in code:
        new_rule = rules.handle_rule()

        if not new_rule and rules.is_region():
            word += letter
        else:
            if letter in [' ', '\t']:
                word = add_word()
            elif letter in symbols:
                word = add_word()
                word += letter
                word = add_word(True)
            else:
                word += letter

        pos.next(letter)
    add_word()
    return lexem

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
                print(f'TEST Failed: ({word}) vs ({lookup}) [{row}:{col}]')
                return False
        return True

    code = [
        'let test a  this   = 12',
        'if a == 12 {',
        '    $ echo \'hello this {test} beautiful world\'',
        '}'
    ]
    lexem = lexer('\n'.join(code))
    test_positioner('\n'.join(code), lexem)

    for tok in lexem:

        print(tok)
