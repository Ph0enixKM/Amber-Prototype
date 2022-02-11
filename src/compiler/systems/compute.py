class ComputeTemplates:
    def __init__(self, binop=None, unop=None, mod=None, trunc=None):
        self.binop = binop
        self.unop = unop
        self.mod = mod
        self.trunc = trunc

class Compute:
    kind = 'bc'

    def __init__(self):
        self.scopes = 0
        self.templates = None
        if Compute.kind == 'bc':
            self.templates = ComputeTemplates(
                binop='$(bc -l <<< "{0} {1} {2}")',
                mod='$(bc <<< "{0} % {1}")',
                unop='$(bc -l <<< "{0} {1}")',
                trunc='$(echo "{0}/1" | bc)'
            )

    def binop(self, left, op, right):
        return self.templates.binop.format(left, op, right)
    
    def mod(self, expr1, expr2):
        return self.templates.mod.format(expr1, expr2)

    def unop(self, expr1, expr2):
        return self.templates.unop.format(expr1, expr2)
    
    def truncate(self, num):
        return self.templates.trunc.format(num)
