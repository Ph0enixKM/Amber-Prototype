from compiler import Lexer, Parser
from os import system
import json

code = '''
silent $ do_you_have_this_command $
if status == 0 {
    $ echo 'Yes, we do have this command!' $
}
else {
    $ echo 'Please, install this command' $
}
'''

lexer = Lexer(code)
parser = Parser(lexer.get())
bash = parser.translate()
# print(bash, '\n')
system(bash)
# print(json.dumps(parser.get().generate_tree(), indent=4))
# print(lexer.get())
