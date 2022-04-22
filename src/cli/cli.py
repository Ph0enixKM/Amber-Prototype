import argparse
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
        if self.args.output:
            return self.save_to_file()
        if self.args.stdout:
            return self.get_stdout()
        self.eval()

        
    def compile(self):
        filename = self.args.input
        std = load_std()
        with open(filename, 'r') as file:
            code = ''.join(file.readlines())
            compiler = Compiler(code)
            compiler.loadPrecompiled(std)
            return compiler
    
    def eval(self):
        system(self.compiler.compile())
    
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


        