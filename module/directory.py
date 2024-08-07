import os
from pathlib import Path
from enum import Enum


PATH_DIRETORIO = os.path.realpath(os.path.dirname(__file__))

# modules dir
WORK_DIR = Path(PATH_DIRETORIO)

# main.py dir
MAIN_DIR = WORK_DIR.parent

class Directory(Enum):
    
    LOG = os.path.join(MAIN_DIR,'log')
    

for dir in Directory:
    os.makedirs(dir.value, exist_ok=True)
