import sqlite3
import os

# Conectar a la base de datos
def conectar():
    directorio_archivo_inicial = os.path.dirname(os.path.abspath(__file__))
    return sqlite3.connect(f'{directorio_archivo_inicial}/0x0000000A12FDFD.db')

def crear_base_de_datos():
    # Conectar a la base de datos (o crearla si no existe)
    conn = conectar()

    # Crear un cursor para ejecutar comandos SQL
    cursor = conn.cursor()

    # Crear la tabla 'comandos'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comandos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE,
            comando TEXT UNIQUE,
            estado INTEGER DEFAULT 0
        )
    ''')

    # Crear la tabla 'respuestas'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS respuestas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_comando INTEGER,
            consulta TEXT,
            respuesta TEXT,
            FOREIGN KEY (id_comando) REFERENCES comandos (id)
        )
    ''')

    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

# Funciones para la tabla 'comandos'
def crear_comando(nombre, comando):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO comandos (nombre,comando) VALUES (?,?)", (nombre, comando,))
    id_insertado = cursor.lastrowid
    conn.commit()
    conn.close()
    return id_insertado


def obtener_comandos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM comandos")
    comandos = cursor.fetchall()
    conn.close()
    return comandos

def obtener_comandos_en_arreglo():
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM comandos")
    comandos = cursor.fetchall()
    conn.close()
    return comandos

def obtener_comandos_por_id(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM comandos WHERE id = ?", (int(id),))
    comando = cursor.fetchall()[0]
    conn.close()
    return comando

def editar_comando(id_comando, nuevo_nombre, nuevo_comando, nuevo_estado):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE comandos SET comando = ?, nombre = ?, estado = ? WHERE id = ?", (nuevo_comando, nuevo_nombre, nuevo_estado, id_comando))
    conn.commit()
    conn.close()

def eliminar_comando(id_comando):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM comandos WHERE id = ?", (id_comando,))
    conn.commit()
    conn.close()

# Funciones para la tabla 'respuestas'
def crear_respuesta(id_comando, consulta, respuesta):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO respuestas (id_comando, consulta, respuesta) VALUES (?, ?, ?)", (id_comando, consulta, respuesta))
    conn.commit()
    conn.close()

def obtener_respuestas(id_comando):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM respuestas WHERE id_comando = ?", (id_comando,))
    respuestas = cursor.fetchall()
    conn.close()
    return respuestas

def obtener_respuesta(id_comando, consulta):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT respuesta FROM respuestas WHERE id_comando = ? AND consulta = ?", (id_comando,consulta))
    respuesta = cursor.fetchone()
    conn.close()
    return respuesta

def editar_respuesta(id_respuesta, nueva_consulta, nueva_respuesta):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE respuestas SET consulta = ?, respuesta = ? WHERE id = ?", (nueva_consulta, nueva_respuesta, id_respuesta))
    conn.commit()
    conn.close()

def eliminar_respuesta(id_respuesta):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM respuestas WHERE id = ?", (id_respuesta,))
    conn.commit()
    conn.close()

def eliminar_respuestas_del_comando(id_comando):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM respuestas WHERE id_comando = ?", (id_comando,))
    conn.commit()
    conn.close()