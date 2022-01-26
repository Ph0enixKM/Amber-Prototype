from tok import Token
from file_iterator import FileIterator
from rules import Rules

def lexer(code):
    pos = FileIterator()
    rules = Rules(code, pos)
    lexem = []
    word = ''

    def add_word():
        if len(word):
            lexem.append(Token(*pos.get(len(word)), word))
            return ''
        return word

    for letter in code:
        if letter.isspace():
            word = add_word()
        elif rules.handle_rule():
            print('Rule handled')
        else:
            word += letter
        pos.next(letter)
    add_word()
    return lexem

if __name__ == '__main__':
    code = [
        'let a = 12',
        'if a == 12 {',
        '    $ echo "hello world"',
        '}'
    ]
    lexem = lexer('\n'.join(code))
    for tok in lexem:
        print(tok)
