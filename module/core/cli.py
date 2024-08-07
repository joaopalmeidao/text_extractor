import argparse

from module import settings, __codname__,__version__


class CLI:
    
    def __init__(self, description, all_arguments={}, **kwargs):
        self.parser = argparse.ArgumentParser(description=description)
        self.subparsers = self.parser.add_subparsers(dest='subcommand')
        if not all_arguments:
            all_arguments = kwargs
        self.all_arguments = all_arguments
        
        self.parser.add_argument('-v', '--version', action='store_true', help='Mostra a versão')
        self.parser.add_argument('-s', '--settings', nargs='?', const='all', help='Mostra a configuração atual (opcional: filtro de configuração)')
        self.parser.add_argument('--setenv', nargs=2, metavar=('VARIAVEL', 'VALOR'), help='Define uma variável de ambiente no arquivo .env')
    
    def command(self, name=''):
        def decorator(func):
            nonlocal name
            if not name:
                name = func.__name__
            if not name in self.all_arguments.keys():
                self.all_arguments[name] = func
            else:
                raise Exception(f'Argument already defined: {name}')
            return func
        return decorator
    
    def parse_args(self):
        self._register_all()
        for key, value in self.all_arguments.items():
            if hasattr(self.args, key):
                if bool(getattr(self.args, key)):
                    value()
    
    def _register_all(self):
        self._register_commands()
        self.args = self.parser.parse_args()
        self._handle_default()
        self._handle_settings()
        self._handle_setenv()
    
    def _register_commands(self):
        for key, value in self.all_arguments.items():
            self.parser.add_argument(f'--{key}', action='store_true',help=f'{value.__doc__} -> {value.__module__}.{value.__name__}')
    
    def _handle_default(self):
        # Defina aqui as chamadas para os comandos enviados pelo usuario
        for k, v in self.args.__dict__.items():
            if v: break
        else: print('Nenhum argumento foi enviado. Envie [--help] ou [-h] para ver os comandos.')
        
        if self.args.version: print(__codname__, ':', __version__)
    
    def _handle_settings(self):
        if self.args.settings:
            variaveis = [var for var in dir(settings) if not var.startswith("__")]
            if self.args.settings == 'all':
                for var in variaveis:
                    print(f"{var} = {getattr(settings, var)}")
            else:
                filter_string = self.args.settings
                variaveis = [var for var in variaveis if filter_string.lower() in var.lower()]
                for var in variaveis:
                    print(f"{var} = {getattr(settings, var)}")

    def _handle_setenv(self):
        if self.args.setenv:
            encontrada = False
            env_variable, env_value = self.args.setenv
            with open(settings.ENV_LOC, 'r') as env_file:
                env_lines = env_file.readlines()
            with open(settings.ENV_LOC, 'w') as env_file:
                for line in env_lines:
                    if line.split('=')[0].strip() == env_variable:
                        env_file.write(f'{env_variable}={env_value}\n')
                        encontrada = True
                    else:
                        env_file.write(line)
            if encontrada:
                print(f'Variável de ambiente {env_variable} definida como {env_value} no arquivo .env')
            else:
                print(f"A variável de ambiente {env_variable} não foi encontrada no arquivo .env")
