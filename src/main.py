from compiler import Lexer, Parser
import json

code = '''
'{1} a {2} b {3} c {4}'
'''



lexer = Lexer(code)
parser = Parser(lexer.get())
parser.translate()
# print(json.dumps(parser.get().generate_tree(), indent=4))


