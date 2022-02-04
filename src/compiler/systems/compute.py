class ComputeTemplates:
    def __init__(self, binop=None, unop=None):
        self.binop = binop
        self.unop = unop

class Compute:
    kind = 'bc'

    def __init__(self):
        self.scopes = 0
        self.templates = None
        if Compute.kind == 'bc':
            self.templates = ComputeTemplates(
                binop='$(bc -l <<< "{0} {1} {2}")',
                unop='$(bc -l <<< "{0} {1}")',
            )

    def binop(self, left, op, right):
        return self.templates.binop.format(left, op, right)
    
    def unop(self, expr1, expr2):
        return self.templates.unop.format(expr1, expr2)