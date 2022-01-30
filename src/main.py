from frontend import Lexer, Parser
import json

code = '''
box a = true
a += 12

box a = $ ls -a $
'''

lexer = Lexer(code)
parser = Parser(lexer.get())
print(json.dumps(parser.get().generate_tree(), indent=4))
# print([str(t) for t in lexer.get()])


