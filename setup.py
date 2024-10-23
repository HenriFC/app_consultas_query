from cx_Freeze import setup, Executable

base = None

executables = [Executable("app.py", base=base)]



setup(
    name = "agendador",
    version = "1.0",
    description = "",
    executables = executables
)