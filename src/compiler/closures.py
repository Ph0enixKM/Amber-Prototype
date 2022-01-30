class Closure:
    def __init__(self, opening, closing):
        self.opening = opening
        self.closing = closing

class ClosureStack:
    closures = [
        Closure('(', ')'),
        Closure('[', ']'),
        Closure('\'', '\''),
        Closure('$', '$')
    ]

    def __init__(self):
        self.opening = []
        self.closing = []
        self.closures = ClosureStack.closures
        self.iter_stack = []
        self.assemble_stacks()
    
    def assemble_stacks(self):
        for closure in self.closures:
            self.opening.append(closure.opening)
        for closure in self.closures:
            self.closing.append(closure.closing)
    
    def get_by_opening(self, opening):
        for closure in self.closures:
            if closure.opening == opening:
                return closure
    
    def get_by_closing(self, closing):
        for closure in self.closures:
            if closure.closing == closing:
                return closure

    def iter(self, token):
        if token.word in self.opening:
            self.iter_stack.append(self.get_by_opening(token.word))
        elif len(self.iter_stack):
            if token.word == self.iter_stack[-1].closing:
                self.iter_stack.pop()
        return len(self.iter_stack)

            