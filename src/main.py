from frontend import Lexer, Parser
import json

lexer = Lexer('\n'.join([
    'box a = 12',
    'box b = \'test\''
]))
parser = Parser(lexer.get())
print(json.dumps(parser.get().generate_tree(), indent=4))
