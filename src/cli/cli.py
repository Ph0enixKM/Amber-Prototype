import argparse
from sys import argv
from compiler import Compiler
from os import system
from error import error
from std import compile_std, load_std
import json

class CLI:
    lang = 'amber'
    name = 'Amber Compiler'
    version = '1.0.0'

    def __init__(self):
        desc = f'Welcome to {CLI.name} version {CLI.version}'
        self.parser = argparse.ArgumentParser(description=desc)
        self.parser.add_argument('input', nargs='?', help=f'path to input {CLI.lang} file')
        self.parser.add_argument('output', nargs='?', help='path to output bash script file')
        self.parser.add_argument('--ast', action='store_true', help='Show Abstract Syntax Tree')
        self.parser.add_argument('--stdout', action='store_true', help='Display translation in standard output')
        self.parser.add_argument('--recompile-std', action='store_true', help='Recompile standard library')
        self.parser.add_argument('-- [...args]', action='store_true', dest='args', help='Pass arguments to your script (used with evaluation)')
        self.args = self.parser.parse_args()
        # Development usage
        if self.args.recompile_std:
            return compile_std()
        # Compiler usage
        if not self.args.input:
            error('No input file specified')
        self.compiler = self.compile()
        if self.args.ast:
            return self.get_ast()
        if self.args.output and not ('--' in argv):
            return self.save_to_file()
        if self.args.stdout:
            return self.get_stdout()
        self.eval()

        
    def compile(self):
        filename = self.args.input
        std = load_std()
        try:
            with open(filename, 'r') as file:
                code = ''.join(file.readlines())
                compiler = Compiler(code)
                compiler.loadPrecompiled(std)
                return compiler
        except FileNotFoundError:
            error(f'File \'{filename}\' does not exist')
        except Exception:
            error(f'Could not open exising file \'{filename}\'')
    
    def pass_arguments(self):
        args = ''
        if '--' in argv:
            index = argv.index('--')
            if len(argv) > index + 1:
                args = [f'"{item}"' for item in argv[index + 1:]]
                args = f'set -- {" ".join(args)}' + '\n'
        return args

    def eval(self):
        args = self.pass_arguments()
        system(args + self.compiler.compile())
    
    def save_to_file(self):
        filename = self.args.output
        with open(filename, 'w') as file:
            file.write(self.compiler.compile())
    
    def get_ast(self):
        ast = json.dumps(self.compiler.ast(), indent=4)
        if self.args.output:
            filename = self.args.output
            with open(filename, 'w') as file:
                file.write(ast)
                return None
        print(ast)
    
    def get_stdout(self):
        print(self.compiler.compile())


        