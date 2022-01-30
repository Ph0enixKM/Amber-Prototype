from .syntax_module import SyntaxModule


class Comment(SyntaxModule):
    def __init__(self):
        self.value = ''

    def ast(self, tokens):
        if len(tokens) >= 2:
            if tokens[0].word != '#':
                return None
            self.value = tokens[1].word.strip()
            tokens = tokens[2:]
            if len(tokens) >= 3 and tokens[2].word == '\n':
                tokens = tokens[1:]
            return tokens
