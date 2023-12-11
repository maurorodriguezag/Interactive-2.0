from Interactive import Interactive
from tabulate import tabulate
import database
import os
import multiprocessing


matriz_comandos_ejecutandose = {}

def correr_comando(id_comando, interactivo = False):
    nuevo_shell = Interactive(id_comando=id_comando)
    nuevo_shell.iniciar(interactivo)

def limpiar_estados():
    comandos = database.obtener_comandos()
    for comando in comandos:
        database.editar_comando(comando[0], comando[1], comando[2], 0)

def ejecutar_comandos():
    comandos = database.obtener_comandos()

    for comando in comandos:
        if comando[0] not in matriz_comandos_ejecutandose:
            try:
                if comando[3] == 1:
                    matriz_comandos_ejecutandose[comando[0]] = multiprocessing.Process(
                        name=f"interactive_comand_{comando[0]}", 
                        target=correr_comando,
                        args=(comando[0], False)
                    )
                    matriz_comandos_ejecutandose[comando[0]].start()
                    database.editar_comando(comando[0], comando[1], comando[2], 1)
            except Exception as e:
                database.editar_comando(comando[0], comando[1], comando[2], 2)

def listar_comandos():
    print("Lista de comandos escritos: \n")
    comandos = [dict(row) for row in database.obtener_comandos_en_arreglo()]
    filas = database.obtener_comandos_en_arreglo()
    comandos = [
        {
            "id": fila["id"],
            "nombre": fila["nombre"],
            "comando": fila["comando"],
            "estado": "Activo" if fila["estado"] == 1 else "Inactivo"
        }
        for fila in filas
    ]
    print(tabulate(comandos, headers="keys", tablefmt="fancy_grid"))

def crear_comandos():
    print("Para crear comandos ingrese la siguiente información:")
    nombre_comando = input('Nombre del comando: ')
    comando = input('Ingrese el comando: ')
    id_comando_creado = database.crear_comando(nombre_comando, comando)
    os.system('clear' if os.name == 'posix' else 'cls')
    print("Se esta ejecuntando el comando, a continuación surgirán las consultas \ndel comando responda hasta verlo necesario. Cuando considere que el comando \nya trabaja por si mismo con las respuestas que usted a dado. Responda \"\033[1mfin\033[0m\".\n")
    correr_comando(id_comando_creado, True)
    ejecutar_comandos()
    
def editar_comandos():
    listar_comandos()
    id_comando_a_editar = input("Ingrese el ID del comando que desea editar: ")
    os.system('clear' if os.name == 'posix' else 'cls')
    try:
        comando_a_editar = database.obtener_comandos_por_id(id_comando_a_editar)
        print(f"Para Editar el comando \033[92m\033[1m{comando_a_editar[1]}\033[0m ingrese la siguiente información ")
        print(f"\033[93m\033[1m(Sí desea dejar la misma información solo presione Enter)\033[0m:\n")
        nombre_comando = input('Nombre del comando: ')
        comando = input('Ingrese el comando: ')
        nombre_comando = nombre_comando if  nombre_comando != '' else comando_a_editar[1]
        comando = comando if  comando != '' else comando_a_editar[2]
        print(f"\nEl comando \033[92m\033[1m{comando_a_editar[1]}\033[0m \nSe guardará con el nombre: \n\033[94m\033[1m{nombre_comando}\033[0m \nY el comando: \n\033[94m\033[1m{comando}\033[0m.")
        validar_respuestas = input("\n¿Desea cambiar las respuestas automaticas que guardó para este comando?\nTenga en cuenta que las respuestas almacenadas se borraran.\nEscriba \033[1mY\033[0m para SI u otra tecla para mantener las respuestas actuales: ")
        if validar_respuestas.lower() == "y":
            try:
                matriz_comandos_ejecutandose[int(id_comando_a_editar)].terminate()
                matriz_comandos_ejecutandose[int(id_comando_a_editar)].join()
                matriz_comandos_ejecutandose.pop(int(id_comando_a_editar))
                database.eliminar_respuestas_del_comando(int(id_comando_a_editar))
                print("\nSe esta ejecuntando el comando, a continuación surgirán las consultas \ndel comando responda hasta verlo necesario. Cuando considere que el comando \nya trabaja por si mismo con las respuestas que usted a dado. Responda \"\033[1mfin\033[0m\".\n")
                correr_comando(id_comando_a_editar, True)
            except Exception as e:
                print(f"\n\033[91mOcurrio un error al editar la matriz de respuesta: \033[1m\033[4m{e}\033[0m")
    except Exception as e:
        print("ID de comando erroneo.")
        
def eliminar_comandos():
    listar_comandos()
    id_comando_a_eliminar = input("Ingrese el ID del comando que desea eliminar: ")
    try:
        comando_a_editar = database.obtener_comandos_por_id(id_comando_a_eliminar)
       
        print(f"\nEl comando \033[92m\033[1m{comando_a_editar[1]}\033[0m se eliminará")
        validar_respuestas = input("\n¿Desea eliminar este comando con todas las respuestas automaticas?\nTenga en cuenta que no se podrá recuperar esta información.\nEscriba \033[1mY\033[0m para SI u otra tecla para mantener las respuestas actuales: ")
        if validar_respuestas.lower() == "y":
            try:
                matriz_comandos_ejecutandose[int(id_comando_a_eliminar)].terminate()
                matriz_comandos_ejecutandose[int(id_comando_a_eliminar)].join()
                matriz_comandos_ejecutandose.pop(int(id_comando_a_eliminar))
                database.eliminar_respuestas_del_comando(int(id_comando_a_eliminar))
                database.eliminar_comando(int(id_comando_a_eliminar))
            except Exception as e:
                print(f"\n\033[91mOcurrio un error al eliminar la matriz de respuesta: \033[1m\033[4m{e}\033[0m")
    except Exception as e:
        print("ID de comando erroneo.")