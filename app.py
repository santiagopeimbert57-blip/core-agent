from flask import Flask, request
from agent.core import responder
from whatsapp.conexion import verificar_webhook, procesar_mensaje, enviar_mensaje

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Servidor activo"

@app.route("/privacy", methods=["GET"])
def privacy():
    return """
    <html><body>
    <h1>Política de Privacidad</h1>
    <p>Este servicio de asistente virtual no almacena conversaciones ni datos personales de los usuarios.</p>
    <p>Los mensajes se procesan en tiempo real para generar respuestas y no se guardan en ninguna base de datos.</p>
    <p>Contacto: santiagopeimbert57@gmail.com</p>
    </body></html>
    """

@app.route("/webhook", methods=["GET"])
def webhook_verificacion():
    return verificar_webhook(request)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    telefono, mensaje = procesar_mensaje(data)

    if not mensaje:
        return {"status": "ignored"}, 200

    print(f"[{telefono}] {mensaje}")
    respuesta = responder(mensaje)
    print(f"[Agente] {respuesta}")
    enviar_mensaje(telefono, respuesta)

    return {"status": "ok"}, 200

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
