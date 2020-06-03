import inspect
import os


def base_path():
    base_path = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
    return base_path
