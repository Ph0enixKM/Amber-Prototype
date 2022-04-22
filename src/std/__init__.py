from distutils.log import error
import pickle
from os import path
from compiler import Compiler
from compiler.modules import SyntaxModule
from error import error

std = 'std.bin'

def compile_std():
    dir = path.dirname(path.realpath(__file__))
    std_files = ['io.amber', 'utils.amber']
    statements = []
    for std_file in std_files:
        with open(f'{dir}/src/{std_file}', 'r') as file:
            comp = Compiler(''.join(file.readlines()))
            ast = comp.rawAst()
            statements += ast.statements
    file = open(f'{dir}/{std}', 'wb')
    pickle.dump({
        'code': statements,
        'memory': SyntaxModule.memory.scopes
    }, file)
    file.close()

def load_std():
    dir = path.dirname(path.realpath(__file__))
    filepath = f'{dir}/{std}'
    file = open(filepath, 'rb')
    if not path.exists(filepath):
        error(f'Could not load standard library\nFile \'{filepath}\' doesn\'t exist')
    bin = pickle.load(file)
    file.close()
    return bin
