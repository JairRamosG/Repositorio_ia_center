import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

conn = sqlite3.connect("billboard100.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS datos(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               titulo TEXT NOT NULL,
               artista TEXT NOT NULL,
               posicion INTEGER)
""")

conn.commit()
conn.close()