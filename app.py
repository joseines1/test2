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

@app.route("/")
def index():
    return "<p>Hola, Mundo!</p>"

@app.route("/alumnos")
def alumnos():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)

    # Consulta a la base de datos
    query = "SELECT * FROM tst0_cursos_pagos"
    cursor.execute(query)
    
    # Obtener todos los registros de la tabla
    registros = cursor.fetchall()
    
    # Cerrar el cursor
    cursor.close()

    # Pasar los registros a la plantilla alumnos.html
    return render_template("alumnos.html", registros=registros)

@app.route("/ver_todos")
def ver_todos():
    return redirect("/alumnos")

# Ruta para insertar un nuevo registro desde la URL (GET)
@app.route("/insertar", methods=["GET"])
def insertar():
    id_curso_pago = request.args.get('Id_Curso_Pago')
    telefono = request.args.get('Telefono')
    archivo = request.args.get('Archivo')
    
    try:
        if not con.is_connected():
            con.reconnect() 
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
    except mysql.connector.Error as err:
        return jsonify({"status": "error", "message": str(err)})

    return jsonify({"status": "success", "message": "Registro insertado correctamente"})


# Ruta para eliminar un registro por ID desde la URL (GET)
@app.route("/eliminar", methods=["GET"])
def eliminar():
    id_curso_pago = request.args.get('Id_Curso_Pago')
    
    try:
        if not con.is_connected():
            con.reconnect()

        cursor = con.cursor(dictionary=True)
        
        # Consulta SQL para eliminar un registro por su ID
        query = "DELETE FROM tst0_cursos_pagos WHERE Id_Curso_Pago = %s"
        cursor.execute(query, (id_curso_pago,))
        con.commit()

        # Notificar a través de Pusher que un registro ha sido eliminado
        pusher_client.trigger('my-channel', 'delete-event', {
            'Id_Curso_Pago': id_curso_pago
        })

        cursor.close()
    except mysql.connector.Error as err:
        return jsonify({"status": "error", "message": str(err)})

    return jsonify({"status": "success", "message": "Registro eliminado correctamente"})

    
# Ruta para editar un registro desde la URL (GET)
@app.route("/editar", methods=["GET"])
def editar():
    id_curso_pago = request.args.get('Id_Curso_Pago')
    telefono = request.args.get('Telefono')
    archivo = request.args.get('Archivo')
    
    try:
        if not con.is_connected():
            con.reconnect()
        cursor = con.cursor(dictionary=True)
        
        # Consulta SQL para actualizar el registro
        query = "UPDATE tst0_cursos_pagos SET Telefono = %s, Archivo = %s WHERE Id_Curso_Pago = %s"
        cursor.execute(query, (telefono, archivo, id_curso_pago))
        con.commit()
        
        cursor.close()

        # Notificar a través de Pusher que un registro ha sido editado
        pusher_client.trigger('my-channel', 'my-event', {
            'Id_Curso_Pago': id_curso_pago,
            'Telefono': telefono,
            'Archivo': archivo
        })

    except mysql.connector.Error as err:
        return jsonify({"status": "error", "message": str(err)})
    
    return jsonify({"status": "success", "message": "Registro actualizado correctamente"})

# Ruta para buscar registros desde la URL (GET)
@app.route("/buscar", methods=["GET"])
def buscar():
    search_query = request.args.get('query', '')

    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)

    # Consulta SQL para buscar registros
    query = "SELECT * FROM tst0_cursos_pagos WHERE Id_Curso_Pago = %s OR Telefono LIKE %s OR Archivo LIKE %s"
    cursor.execute(query, (search_query, f'%{search_query}%', f'%{search_query}%'))
    
    # Obtener todos los registros que coinciden
    registros = cursor.fetchall()
    
    cursor.close()

    # Pasar los registros a la plantilla alumnos.html
    return render_template("alumnos.html", registros=registros)

@app.route("/ping")
def ping():
    try:
        con.ping(reconnect=True, attempts=3, delay=5)
        return jsonify({"status": "success", "message": "Conexión a la base de datos exitosa"})
    except mysql.connector.Error as err:
        return jsonify({"status": "error", "message": str(err)})

if __name__ == "__main__":
    app.run(debug=True)

