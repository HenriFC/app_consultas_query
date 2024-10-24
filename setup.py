from cx_Freeze import setup, Executable

base = 'Console'

executables = [Executable("app.py", base=base)]



setup(
    name = "agendador",
    version = "1.0",
    description = "",
    executables = executables
)