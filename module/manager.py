from .core.cli import CLI

from module import __codname__, __version__, settings


print('Registrando funcoes do sistema...')
cli = CLI(description=f'{__codname__} CLI')