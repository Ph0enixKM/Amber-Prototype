class FileIterator:
    def __init__(self, row = 1, col = 1):
        self.defaults = (row, col)
        self.row = row
        self.col = col
        self.index = 0

    def next(self, letter):
        self.index += 1
        self.col += 1
        if letter == '\n':
            self.row += 1
            self.col = self.defaults[1]

    def get(self, backward_offset = 0):
        return (self.row, self.col - backward_offset)
    
    def get_index(self):
        return self.index
