from flask import Flask, render_template, request 
import os
import sqlite3 

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "basedatos.db")

def conectar():
    return sqlite3.connect(DB_PATH)

@app.route('/')
def home():
    return render_template("index.html")  

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")  

    user = request.form.get('user')
    password = request.form.get('pass')

    conn = conectar()
    cursor = conn.cursor()

    # Consulta segura usando parámetros (previene SQL Injection)
    query = "SELECT * FROM USUARIOS WHERE USERNAME = ? AND PASSWORD = ?"
    
    print(f"\n[!] SQL Ejecutado: {query}")
    
    cursor.execute(query, (user, password))
    results = cursor.fetchall() 
    conn.close()

    if results:
        html = "<h2>⚠️ Datos Encontrados ⚠️</h2>"
        html += "<h2>⚠️ Datos Encontrados ⚠️</h2>"
        html += "<table border='1' style='border-collapse: collapse; width: 98%; text-align: left;'>"
        html += "<tr style='background-color: #f2f2f2;'><th>ID</th><th>Username</th><th>Password</th><th>Email</th><th>Nombre</th><th>Teléfono</th><th>Dirección</th></tr>"
        
        for fila in results:        # ← ahora sí está DENTRO del if
            html += "<tr>"
            for col in fila:
                html += f"<td>{col}</td>"
            html += "</tr>"
        
        html += "</table>"
        html += "<br><a href='/'>Volver al inicio</a>"
        return html
    else:
        return "<h2>Credenciales incorrectas ❌</h2><a href='/login'>Reintentar</a>"
    
# Se agregan cabeceras HTTP para mitigar vulnerabilidades comunes
@app.after_request
def agregar_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    #Se permite CDN necesario para Bootstrap
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
        "script-src 'self' https://cdn.jsdelivr.net; "
        "img-src 'self' data: https://cdn.jsdelivr.net; "
        "font-src 'self' https://fonts.gstatic.com;"
    )
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
