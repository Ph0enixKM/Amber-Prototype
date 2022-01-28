import sys
from colorama import init, Fore
from enum import Enum
init()

debug = True

class ErrorTypes(Enum):
    UNDEF = 'Undefined Syntax'
    ENTER = 'This token must be followed by a new line'
    VAR = 'Invalid variable name'

def error_tok(token, text):
    error(f'{text} (at {token.row}:{token.col})')

def error(text):
    msg = [Fore.RED, text, Fore.RESET]
    print(''.join(msg))
    if debug:
        raise Exception(text)
    sys.exit(1)