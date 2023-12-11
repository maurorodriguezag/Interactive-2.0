import database
import sqlite3
import os
import multiprocessing
from controllers.comandos import *
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Validar si se muestran las opciones de consola')
    parser.add_argument('-console', type=int, help='PID del proceso a manejar')
    args = parser.parse_args()
    multiprocessing.freeze_support()
    os.system('clear' if os.name == 'posix' else 'cls')
    
    print("Se está ejecutando la consola de interactive...")

    try:
        database.crear_base_de_datos()
        # Ejemplo de creación de un comando
        # limpiar_estados()
        ejecutar_comandos()
    except sqlite3.DatabaseError as e:
        print(f"Error al crear la base de datos: {e}")
    
    while True:
        if args.console:
            os.system('clear' if os.name == 'posix' else 'cls')
            eleccion = input(
    """************************************************************
    ************************************************************

                Bienvenido a Interactive 2.0
                    
    Este aplicativo fue desarrollado para automatizar los
    procesos de comunicación con el terminal como por ejemplo 
    tuneles, RDP, VPN, etc...
    Para mantener los procesos vivos en segundo plano.

    ************************************************************
    ************************************************************


    Puede listar, crear, editar o eliminar uno de los hilos del 
    proceso ¿Cual desea hacer?

        1. Listar
        2. Crear
        3. Editar
        4. Eliminar
        5. Salir
        
    Mi eleccion es: """
            )    
            os.system('clear' if os.name == 'posix' else 'cls')
            
            if int(eleccion) == 1:
                listar_comandos()
            if int(eleccion) == 2:
                crear_comandos()
            if int(eleccion) == 3:
                editar_comandos()
            if int(eleccion) == 4:
                eliminar_comandos()

            input("\nPresiona cualquier tecla para volver...")

            if int(eleccion) == 5:
                print("Gracias por usar el servicio.")
                break
        else:
            pass