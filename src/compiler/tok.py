class Token:
    def __init__(self, row, col, word = ''):
        self.word = word
        self.row = row
        self.col = col
    
    def append(self, letter):
        self.word += letter
    
    def is_ready(self):
        return bool(len(self.word))
    
    def __str__(self):
        return f'Tok[{self.word}:{self.row}:{self.col}]'

    def __repr__(self):
        return self.__str__()
