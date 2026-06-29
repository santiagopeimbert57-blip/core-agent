import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "cliente.json")

with open(_CONFIG_PATH, encoding="utf-8") as f:
    _cliente = json.load(f)

_client = Groq(api_key=os.environ["GROQ_API_KEY"])


def _build_system_prompt() -> str:
    negocio = _cliente["negocio"]
    servicios = _cliente["servicios"]
    horarios = _cliente["horarios"]
    agente = _cliente["agente"]

    nombre_negocio = negocio["nombre"] or "el negocio"

    servicios_lista = "\n".join(
        f"  - {s['nombre']} ({s['duracion_minutos']} min)" for s in servicios
    )

    horarios_lista = []
    for dia, info in horarios.items():
        if info["abierto"]:
            horarios_lista.append(f"  - {dia.capitalize()}: {info['inicio']} – {info['fin']}")
        else:
            horarios_lista.append(f"  - {dia.capitalize()}: cerrado")
    horarios_texto = "\n".join(horarios_lista)

    return f"""Eres un asistente virtual de WhatsApp para {nombre_negocio}.
Tu personalidad es {agente['personalidad']} y respondes siempre en {agente['idioma']}.

Servicios disponibles:
{servicios_lista}

Horarios de atención:
{horarios_texto}

Responde de forma breve y útil. Si el cliente quiere agendar una cita, pídele su nombre, el servicio que desea y la fecha/hora preferida."""


_SYSTEM_PROMPT = _build_system_prompt()


def responder(mensaje: str) -> str:
    response = _client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": mensaje},
        ],
    )
    return response.choices[0].message.content
