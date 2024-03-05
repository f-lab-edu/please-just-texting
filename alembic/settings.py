import sys
from pathlib import Path


def add_project_root_to_path():
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.append(str(PROJECT_ROOT))


add_project_root_to_path()
print(sys.path)
