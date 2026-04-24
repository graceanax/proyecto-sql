from flask import Flask, render_template, request
import sqlite3
import os   

app = Flask(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "basedatos.db")

def crear_base():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS USUARIOS")

    cursor.execute("""
    CREATE TABLE USUARIOS (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        USERNAME TEXT NOT NULL,
        PASSWORD TEXT NOT NULL,
        EMAIL TEXT NOT NULL,
        NOMBRE TEXT NOT NULL,
        TELEFONO TEXT,
        DIRECCION TEXT
    )
    """)
    # USERNAME, PASSWORD, EMAIL, NOMBRE, TELEFONO, DIRECCION 
    usuarios = [
        ("admin", "admin123", "admin@gmail.com.gt", "Administrador", "5555-1111", "Oficina central"),
        ("ana", "ana2026", "ana@mail.com", "Ana Pérez", "5555-2222", "Zona 3, Ciudad Guatemala"),
        ("gerber", "password456", "gerber@mail.com", "Gerber Agustín", "5555-3333", "Mixco, Guatemala"),
        ("mario", "mario24", "mario@mail.com", "Mario Montufar", "48759865", "Zona 10, Ciudad de Guatemala"),
        ("mady", "mady2024", "madelayne@mail.com", "Madelayne García", "75986877", "Zon 3, Ciudad de Guatemla"),
        ("kathy", "kathy2025", "katheryn@mail.com", "Katheryn Taló", "84759833", "Mixco, Guatemala")
    ]

    cursor.executemany("""
    INSERT INTO USUARIOS (USERNAME, PASSWORD, EMAIL, NOMBRE, TELEFONO, DIRECCION)
    VALUES (?, ?, ?, ?, ?, ?)
    """, usuarios)

    conn.commit()
    conn.close()
    print("✅ Base de datos mejorada creada correctamente")

if __name__ == "__main__":
    crear_base()