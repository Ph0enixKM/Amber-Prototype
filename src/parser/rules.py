class Rule:
    def __init__(self, name, start, end=None, interp=None, region=True):
        self.name = name
        self.start = start
        self.end = end if end else start
        self.interp = interp
        self.region = region
    
    def is_region(self):
        return self.region

class RuleCodeChunk:
    def __init__(self, code, file_iter):
        self.code = code
        self.file_iter = file_iter
    
    def get(self):
        print(self.file_iter.__dict__)
        index = self.file_iter.get_index()
        return self.code[:index + 1]

class Rules:
    def __init__(self, code, file_iter):
        self.chunk = RuleCodeChunk(code, file_iter)
        self.stack = [Rule('global', None)]
        self.rules = [
            Rule('string_single', '\'', interp='string_interp'),
            Rule('string_interp', '{', '}', region=False),
            Rule('comment', '#', '\n'),
            Rule('global', None, region=False),
        ]
        self.begin_rules = list(map(lambda r: r.start, self.rules))
        self.end_rules = list(map(lambda r: r.end, self.rules))
    
    def get_rule_by_func(self, func):
        for rule in self.rules:
            if func(rule):
                return rule
        return None

    def get_rule_by_name(self, name):
        return self.get_rule_by_func(lambda r: r.name == name)

    def get_rule_by_tok_str(self, chunk, tok_str):
        is_equal = lambda r: tok_str(r) == chunk[-len(tok_str(r)):]
        is_escaped = lambda r: chunk[-len(tok_str(r)) - 1] == '\\'
        return self.get_rule_by_func(lambda r: is_equal(r) and not is_escaped(r))

    def get_rule_by_start(self, chunk):
        return self.get_rule_by_tok_str(chunk, lambda r: r.start)

    def get_rule_by_end(self, chunk):
        return self.get_rule_by_tok_str(chunk, lambda r: r.end)

    
    def handle_rule(self):
        # If it's a region - close it
        if self.stack[-1].is_region():
            print(f'chunk (5) ...{self.chunk.get()[-5:]}')
            rule = self.get_rule_by_end(self.chunk.get())
            if rule:
                print(f'New rule: {rule}')
                # self.stack.append(rule)
                # TODO: Finish it

