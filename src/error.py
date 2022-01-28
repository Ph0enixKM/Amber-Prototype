import sys
from colorama import init, Fore
from enum import Enum
init()

class ErrorTypes(Enum):
    UNDEF = 'Undefined Syntax'

def error_tok(token, text):
    error(f'{text} (at {token.row}:{token.col})')

def error(text):
    msg = [Fore.RED, text, Fore.RESET]
    print(''.join(msg))
    sys.exit(1)