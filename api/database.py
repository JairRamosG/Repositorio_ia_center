import sqlite3

conn = sqlite3.connect("prueba.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               nombre TEXT NOT NULL,
               edad INTEGER
               )""")

conn.commit() # Guardar cambios
conn.close() # Cerrar conexion


conn = sqlite3.connect("prueba.db")
cursor = conn.cursor()

cursor.execute("INSERT INTO usuarios (nombre, edad) VALUES(?,?)", ("Juan", 21))

conn.commit()
conn.close()



