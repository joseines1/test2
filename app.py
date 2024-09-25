from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector
import pusher

# Conexión a la base de datos MySQL
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

# Inicializar Flask y Pusher
app = Flask(__name__)

pusher_client = pusher.Pusher(
    app_id='1768013',
    key='93f016bf1fd53612e9ad',
    secret='e6eef555c5cb98e94bee',
    cluster='us2',
    ssl=True
)

#@app.route("/")
#def index():
 #   return "<p>Hola, Mundo!</p>"

@app.route("/app.html")
def index():
    cursor = con.cursor(dictionary=True)
    
    # Consulta a la base de datos
    query = "SELECT * FROM tst0_cursos_pagos"
    cursor.execute(query)
    
    # Obtener todos los registros de la tabla
    registros = cursor.fetchall()
    
    # Cerrar el cursor
    cursor.close()

    # Pasar los registros a la plantilla alumnos.html
    return render_template("app.html", registros=registros)

# Ruta para insertar un nuevo registro
@app.route("/insertar", methods=["POST"])
def insertar():
    id_curso_pago = request.form['Id_Curso_Pago']
    telefono = request.form['Telefono']
    archivo = request.form['Archivo']
    
    cursor = con.cursor(dictionary=True)
    query = "INSERT INTO tst0_cursos_pagos (Id_Curso_Pago, Telefono, Archivo) VALUES (%s, %s, %s)"
    cursor.execute(query, (id_curso_pago, telefono, archivo))
    con.commit()

    # Notificar a través de Pusher
    pusher_client.trigger('my-channel', 'my-event', {
        'Id_Curso_Pago': id_curso_pago,
        'Telefono': telefono,
        'Archivo': archivo
    })

    cursor.close()

    return redirect("/alumnos")

if __name__ == "__main__":
    app.run(debug=True)
