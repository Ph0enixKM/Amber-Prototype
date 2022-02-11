from cx_Freeze import setup, Executable

setup(
    name = "amber",
    version = "0.1",
    description = "AmberScript compiler",
    executables = [Executable("main.py")]
)
