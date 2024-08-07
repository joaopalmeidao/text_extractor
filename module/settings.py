import logging
from platform import system
from dotenv import load_dotenv, find_dotenv
import json
import os
import socket

from module.directory import WORK_DIR


load_dotenv()

ENV_LOC = find_dotenv()

SYSTEM = system()

# //////////////////////////////////////////// 
# Log Config:
# //////////////////////////////////////////// 

LOG_LEVEL = os.getenv("LOG_LEVEL")

if not LOG_LEVEL:
    LOG_LEVEL = 'INFO'

LOG_LEVEL = logging._nameToLevel.get(LOG_LEVEL)

# //////////////////////////////////////////// 
# PID:
# //////////////////////////////////////////// 

PID = os.getpid()

# Obtém o nome do host da máquina
HOST_NAME = socket.gethostname()

# Obtém o endereço IP associado ao nome do host
IP_ADRESS = socket.gethostbyname(HOST_NAME)


# //////////////////////////////////////////// 
# DEBUG:
# //////////////////////////////////////////// 

DEBUG = os.getenv("DEBUG", 'False').lower() in ('true', '1', 't')

if DEBUG:
    LOG_LEVEL = 'DEBUG'
    print('WARNING: Running in debug mode!')

# ////////////////////////////////////////////////////////
# CONFIGURACOES DA API
# ////////////////////////////////////////////////////////

AUTH_TOKEN=os.getenv("AUTH_TOKEN")

if not AUTH_TOKEN:
    raise Exception('Configure o AUTH_TOKEN no arquivo .env')

# ////////////////////////////////////////////////////////
# CONFIGURACOES DO TESSERACT E POPPLER
# ////////////////////////////////////////////////////////

POPPLER_PATH=os.getenv("POPPLER_PATH")
TESSERACT_CMD=os.getenv("TESSERACT_CMD")