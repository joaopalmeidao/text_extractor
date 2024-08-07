
from module.core.utils import clear_folder
from module.directory import Directory
from module.core.customlogger import logger, task_log_cleanup

from module.manager import cli
from module import __codname__, __version__
from module import settings




if __name__ == '__main__':
    print('Argumentos da CLI:')
    for arg, func in cli.all_arguments.items():
        print(f'{arg} -> {func.__module__}.{func.__name__}')
    
    cli.parse_args()
