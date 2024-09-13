from flask import Flask
import pusher
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    return render_templates("app.html")

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    matricula       =  request.form["txtMatriculaFA"]
    nombreapellido  =  request.form["txtNombreApellidoFA"]
    return f"Matrícula: {matricula}  Nombre y Apellido: {nombreapellido} "

@app.route("/evento")
def eventoNuevo():
    pusher_client = pusher.Pusher(
      app_id='1768013',
      key='93f016bf1fd53612e9ad',
      secret='e6eef555c5cb98e94bee',
      cluster='us2',
      ssl=True
    )

    message = "Este es un mensaje enviado desde Flask."

    # Disparar el evento a través de Pusher
    pusher_client.trigger('my-channel', 'my-event', {'message': message})

    # Devolver un mensaje que será recibido en el cliente
    return jsonify({'status': 'success', 'message': 'Mensaje enviado correctamente.'}),
