import argparse
from compiler import Compiler
from os import system
import json

class CLI:
    lang = 'amberscript'
    name = 'AmberScript Compiler'
    version = '1.0.0'

    def __init__(self):
        desc = f'Welcome to {CLI.name} version {CLI.version}'
        self.parser = argparse.ArgumentParser(description=desc)
        self.parser.add_argument('input', help=f'path to input {CLI.lang} file')
        self.parser.add_argument('output', nargs='?', help='path to output bash script file')
        self.parser.add_argument('--ast', action='store_true', help='Show Abstract Syntax Tree')
        self.parser.add_argument('--stdout', action='store_true', help='Display translation in standard output')
        self.args = self.parser.parse_args()
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
        with open(filename, 'r') as file:
            code = ''.join(file.readlines())
            return Compiler(code)
    
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
                return file.write(ast)
        print(ast)
    
    def get_stdout(self):
        print(self.compiler.compile())


        