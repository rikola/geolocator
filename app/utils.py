import os.path
from pathlib import Path


def get_project_root() -> Path:
    p = Path(__file__).parent.parent
    print(p)
    return p


def get_data_path():
    return os.path.join(get_project_root(), "data")


def get_app_base_path():
    return os.path.dirname(os.path.realpath(__file__))

