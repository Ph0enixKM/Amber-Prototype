import os
from cx_Freeze import setup, Executable

def get_std_paths():
    files = os.listdir('std/src')
    return [f'std/src{file}' for file in files]

build_exe = {
    'build_exe': '../build',
    'bin_includes': [*get_std_paths(), 'std/std.bin']
}

setup(
    name = 'amber',
    version = '0.1',
    description = 'AmberScript compiler',
    executables = [Executable('main.py')],
    options = {'build_exe': build_exe}
)
