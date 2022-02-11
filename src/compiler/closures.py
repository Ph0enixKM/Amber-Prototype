class Closure:
    def __init__(self, opening, closing, region=False):
        self.opening = opening
        self.closing = closing
        self.region = region
        if self.region:
            assert(self.opening == self.closing)
    
    def __repr__(self):
        return f'{self.opening}{self.closing}'

class ClosureStack:
    closures = [
        Closure('(', ')'),
        Closure('[', ']'),
        Closure('\'', '\'', region=True),
        Closure('$', '$', region=True)
    ]

    def __init__(self):
        self.opening = []
        self.closing = []
        self.closures = ClosureStack.closures
        self.iter_stack = []
        self.escaped = False
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
        # Handle escape symbol
        if self.escaped:
            self.escaped = False
            return len(self.iter_stack)
        if token.word == '\\':
            self.escaped = True
            return len(self.iter_stack)
        # Handle opening symbol
        if token.word in self.opening:
            clo = self.get_by_opening(token.word)
            # If it's a region
            if len(self.iter_stack) and self.iter_stack[-1].region:
                if self.iter_stack[-1].closing == clo.closing:
                    self.iter_stack.pop()
                    return len(self.iter_stack)
            self.iter_stack.append(clo)
        # Handle closing symbol
        elif len(self.iter_stack):
            if token.word == self.iter_stack[-1].closing:
                self.iter_stack.pop()
        return len(self.iter_stack)

            