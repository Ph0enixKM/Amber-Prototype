class VariableInfo:
    def __init__(self, eval_type) -> None:
        self.eval_type = eval_type

class Scope:
    def __init__(self, loop_scope, fun_scope):
        self.vars = {}
        self.funs = []
        self.loop_scope = loop_scope
        self.fun_scope = fun_scope
    
    def __repr__(self):
        return f'[{", ".join(self.vars.keys())} : {", ".join(self.funs)}]'

class Memory:
    def __init__(self):
        self.scopes = []

    def enter_scope(self, loop_scope=False, fun_scope=False):
        self.scopes.append(Scope(loop_scope, fun_scope))
    
    def leave_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()
    
    def add_variable(self, name, eval_type):
        self.scopes[-1].vars[name] = VariableInfo(eval_type)
    
    def add_fun(self, name):
        self.scopes[-1].funs.append(name)
    
    def has_fun(self, name):
        for scope in self.scopes:
            if name in scope.funs:
                return True
        return False
    
    def has_double_fun(self, name):
        return name in self.scopes[-1].funs
    
    def has_variable(self, name):
        for scope in self.scopes:
            if name in scope.vars:
                return True
        return False
    
    def update_variable(self, name, new_type):
        for scope in self.scopes:
            if name in scope.vars:
                scope.vars[name].eval_type = new_type
        return None

    def has_double_variable(self, name):
        return name in self.scopes[-1].vars
    
    def get_variable_type(self, name):
        for scope in self.scopes[::-1]:
            if name in scope.vars:
                return scope.vars[name].eval_type

    def is_loop_context(self):
        for scope in self.scopes[::-1]:
            if scope.loop_scope:
                return True
        return False

    def is_fun_context(self):
        for scope in self.scopes[::-1]:
            if scope.fun_scope:
                return True
        return False

    def remove_variable(self, name):
        self.scopes[-1].vars = list(filter(
            lambda item: item == name,
            self.scopes[-1].vars))