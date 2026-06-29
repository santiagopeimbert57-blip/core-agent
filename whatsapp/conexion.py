import os
import requests


def verificar_webhook(request):
    """Handles Meta's webhook verification challenge."""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == os.environ.get("WHATSAPP_VERIFY_TOKEN"):
        return challenge, 200

    return "Token de verificación inválido", 403


def procesar_mensaje(data):
    """Extracts phone number and text from an incoming WhatsApp message.

    Returns (telefono, mensaje) or (None, None) if the payload has no text message.
    """
    try:
        entry = data["entry"][0]
        change = entry["changes"][0]
        value = change["value"]
        message = value["messages"][0]

        if message.get("type") != "text":
            return None, None

        telefono = message["from"]
        mensaje = message["text"]["body"]
        return telefono, mensaje
    except (KeyError, IndexError):
        return None, None


def enviar_mensaje(telefono, mensaje):
    """Sends a text message back to the user via WhatsApp Cloud API."""
    token = os.environ.get("WHATSAPP_TOKEN", "").strip()
    phone_number_id = os.environ.get("WHATSAPP_PHONE_NUMBER_ID")
    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": telefono,
        "type": "text",
        "text": {"body": mensaje},
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers)
    if not response.ok:
        print(f"[WhatsApp API error] {response.status_code}: {response.text}")
        return None
    return response.json()
