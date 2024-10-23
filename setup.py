from cx_Freeze import setup, Executable

base = None

executables = [Executable("app.py", base=base)]

options = {
    "build_exe" : {
        "include_files": ["icon.png"]
    }
}

setup(
    name = "agendador",
    version = "1.0",
    description = "",
    options = options,
    executables = executables
)