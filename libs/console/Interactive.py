import platform
import time
import os
from multiprocessing import Process, Manager
from pexpect.popen_spawn import PopenSpawn
import pexpect
import database
from pynput import keyboard

    
class Interactive:
            
    def __init__(self, id_comando):
        self.comando = database.obtener_comandos_por_id(id_comando)
        self.permitir_consola = False
        # 1. Ejecutando
        # 2. Esperando respuesta
        # 3. En espera
        self.codigo = Manager().Value('i', 1)
        self.consola = Manager().Value('c', '')
        self.respuesta = Manager().Value('c', '')
        
    def iniciar(self, permitir_consola=False):
        self.permitir_consola = permitir_consola
        nombre_comando = self.comando[1]
        self.console_process = Process(name=nombre_comando,target=self.leer_comandos)
        self.console_process.start()
        while True:
            if (
                (self.consola.value != '' and self.consola.value is not None) and 
                (self.respuesta.value == '' or self.respuesta.value is None) and
                (self.codigo.value == 2)
                ):
                if permitir_consola:
                    self.respuesta.value = input(self.consola.value)
                    
                if str(self.respuesta.value).lower() == 'fin':
                    self.on_press()
                    break
                    
                self.codigo.value = 3
            time.sleep(1)
      
    def leer_comandos(self):
        id_comando = self.comando[0]
        nombre_comando = self.comando[1]
        cmd = self.comando[2]
        lineas = []
        
        current_dir = os.getcwd() # os.path.dirname(sys.executable)

        # Validar si existe la carpeta de logs
        current_dir_logs = f"{current_dir}/logs/{nombre_comando}"
        if(os.path.exists(current_dir_logs) == False and os.path.isdir(current_dir_logs) == False):
            os.makedirs(current_dir_logs)
            
        # Validar si existe el archivo para la conexión
        file_log = f"{current_dir_logs}/{nombre_comando}.log"
        
        if(os.path.exists(file_log) == False):
            self.escribir_log(file_log, cmd)
        else:
            self.limpiar_logs(file_log, cmd)
        try:
            if platform.system() != "Windows":
                self.child = pexpect.spawn('/bin/bash', ['-c', cmd], timeout=None)
            else:
                self.child = pexpect.popen_spawn.PopenSpawn(f'cmd /c {cmd}', timeout=None)
            
            while True:
                index = self.child.expect([pexpect.EOF, pexpect.TIMEOUT, pexpect.EOF], timeout=1)

                if index == 1:
                    linea_para_agregar = (self.child.before).decode('utf-8')
                    
                    for linea in lineas:
                        linea_para_agregar = str(linea_para_agregar).replace(linea, '')
                    
                    if linea_para_agregar != '' and linea_para_agregar not in lineas:
                        lineas.append(linea_para_agregar)
                        self.consola.value = linea_para_agregar
                        
                if self.consola.value != '' and self.consola.value is not None:
                    
                    response_in_database = database.obtener_respuesta(id_comando, self.consola.value)
                    response_in_database = response_in_database[0] if response_in_database is not None else None
                    
                    if response_in_database is None and self.codigo.value < 3:
                        self.codigo.value = 2
                        
                    if self.codigo.value == 3:
                        comprobacion_unica = database.obtener_respuesta(id_comando, self.consola.value)
                        
                        if comprobacion_unica == None and self.respuesta.value != None:
                            database.crear_respuesta(id_comando, self.consola.value, self.respuesta.value)
                        self.codigo.value = 1
                    
                    if response_in_database is not None:
                        self.respuesta.value = response_in_database
                    
                    if self.respuesta.value is not None and self.codigo.value ==1:
                        if self.respuesta.value != None:
                            self.escribir_log(file_log, f"\nConsola: {self.consola.value}\nRespuesta: {self.respuesta.value}")
                        self.child.sendline(self.respuesta.value)
                        self.respuesta.value = None
                time.sleep(1)
                
        except pexpect.EOF as e:
            if self.permitir_consola:
                print(f"Error al ejecutar el comando: {e}")
            
    def on_press(self):
        self.console_process.terminate()
        if self.permitir_consola:
            print("Se contestó fin a la consulta del comando. Saliendo del reconocimiento de las respuestas.")

        
    def escribir_log(self, dir, mensaje):
        try:
            with open(dir, "a") as file:
                file.write(f"{mensaje}\n")
        except IOError:
            if self.permitir_consola:
                print(f"No se pudo editar y guardar el archivo '{dir}'.")
            
    def limpiar_logs(self, dir, mensaje):
        try:
            with open(dir, "w") as file:
                file.write(f"{mensaje}\n")
        except IOError:
            if self.permitir_consola:
                print(f"No se pudo editar y guardar el archivo '{dir}'.")