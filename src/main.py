from frontend import Lexer, Parser
import json

lexer = Lexer('\n'.join([
    'box a = -12',
    'if 12 {',
    '12',
    '}',
    'else: 12',
    'box b = \'test{\'test{\'test\'}\'}\''
]))
parser = Parser(lexer.get())
print(json.dumps(parser.get().generate_tree(), indent=4))
# print([str(t) for t in lexer.get()])
