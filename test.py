from agent.core import responder

preguntas = [
    "¿Cuáles son sus servicios?",
    "¿Cuál es su horario?",
    "Quiero agendar una cita",
]

for pregunta in preguntas:
    print(f"Usuario: {pregunta}")
    print(f"Agente:  {responder(pregunta)}")
    print("-" * 60)
