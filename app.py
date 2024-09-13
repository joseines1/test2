from flask import Flask, render_template, request, jsonify
import pusher

app = Flask(__name__)

# Ruta para el índice
@app.route("/")
def index():
    return render_template("app.html")  # Corregido: render_template en lugar de render_templates

# Ruta para alumnos
@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

# Ruta para guardar alumnos
@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    matricula = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]
    return f"Matrícula: {matricula}  Nombre y Apellido: {nombreapellido}"

# Ruta para disparar el evento de Pusher
@app.route("/evento", methods=['POST'])
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
    pusher_client.trigger('my-channel', 'my-event', {'message':"Luna no vale verga"})

    return jsonify(success=True)

