import database
import os
import multiprocessing
from controllers.comandos import *
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Validar si se muestran las opciones de consola')
    parser.add_argument('-idcommand', type=int, help='PID del proceso a manejar')
    args = parser.parse_args()
    multiprocessing.freeze_support()
    
    os.system('clear' if os.name == 'posix' else 'cls')
    if args.idcommand:
        database.eliminar_respuestas_del_comando(args.idcommand)
        correr_comando(args.idcommand, True)