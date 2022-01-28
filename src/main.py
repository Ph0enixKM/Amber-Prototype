from frontend import Lexer, Parser
import json

code = '''
box name = 'Pablo'
loop i in [1,2,3] {
    box a = 12
}
'''

lexer = Lexer(code)
parser = Parser(lexer.get())
print(json.dumps(parser.get().generate_tree(), indent=4))
# print([str(t) for t in lexer.get()])
