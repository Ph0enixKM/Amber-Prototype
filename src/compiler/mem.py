class VariableInfo:
    def __init__(self, eval_type) -> None:
        self.eval_type = eval_type

class Scope:
    def __init__(self):
        self.vars = {}
    
    def __repr__(self):
        return f'[{", ".join(self.vars.keys())}]'

class Memory:
    def __init__(self):
        self.scopes = []

    def enter_scope(self):
        self.scopes.append(Scope())
    
    def leave_scope(self):
        if len(self.scopes) > 0:
            self.scopes.pop()
        else:
            raise Exception('Cannot leave global scope context')
    
    def add_variable(self, name, eval_type):
        self.scopes[-1].vars[name] = VariableInfo(eval_type)
    
    def has_variable(self, name):
        for scope in self.scopes:
            if name in scope.vars:
                return True
        return False

    def has_double_variable(self, name):
        return name in self.scopes[-1].vars
    
    def get_variable_type(self, name):
        for scope in self.scopes[::-1]:
            if name in scope.vars:
                return scope.vars[name].eval_type
    
    def remove_variable(self, name):
        self.scopes[-1].vars = list(filter(
            lambda item: item == name,
            self.scopes[-1].vars))