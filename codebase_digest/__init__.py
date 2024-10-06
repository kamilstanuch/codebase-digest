import os

def read_version():
    version_file = os.path.join(os.path.dirname(__file__), '..', 'VERSION')
    try:
        with open(version_file) as f:
            return f.read().strip()
    except FileNotFoundError:
        return "unknown"

__version__ = read_version()