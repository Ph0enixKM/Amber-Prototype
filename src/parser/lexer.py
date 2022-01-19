from token import Token
from file_iterator import FileIterator

def lexer(code):
    pos = FileIterator()
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
        else:
            word += letter
        pos.next(letter)
    return lexem