import importlib
import pathlib

file_ = ['__init__.py']


def loadClasses(folder: str):
    global file_
    load = list()
    current_directory = pathlib.Path(folder)
    for current_file in current_directory.glob('*.py'):
        if current_file.name not in file_:
            file = current_file.name.replace('.py', '')
            module = importlib.import_module(f"{folder}.{file}")
            my_class = getattr(module, file)
            load.append(my_class)

    return load