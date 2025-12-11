# backend/api/v1/services/chat_service.py

from typing import List, Dict, Any

from core.chat_prompt import SYSTEM_PROMPT
from core.config import settings
from api.v1.schemas.chat_schemas import ChatMessage


def _build_llm_messages(messages: List[ChatMessage]) -> List[Dict[str, str]]:
    """
    Convierte la lista de ChatMessage (user/assistant) en el formato
    que normalmente consumen los modelos de lenguaje (role + content),
    añadiendo al principio el mensaje de sistema con el prompt del asistente.

    IMPORTANTE: aquí NO se hace ninguna llamada a Gemini todavía,
    solo preparamos la estructura de mensajes.
    """
    llm_messages: List[Dict[str, str]] = []

    # Mensaje de sistema con la identidad y reglas del asistente
    llm_messages.append({
        "role": "system",
        "content": SYSTEM_PROMPT.strip(),
    })

    # Mensajes de la conversación (usuario / asistente anteriores)
    for msg in messages:
        llm_messages.append({
            "role": msg.role,
            "content": msg.content,
        })

    return llm_messages


def _call_gemini_api(llm_messages: List[Dict[str, str]]) -> str:
    """
    Punto central donde, más adelante, integraremos la llamada real a Gemini.

    De momento devuelve una respuesta de prueba (modo 'fake') para poder
    probar el endpoint /api/v1/chat sin depender todavía de la API externa.

    Cuando integremos Gemini de verdad, esta función:
      - Leerá la API key desde settings.GEMINI_API_KEY
      - Creará el cliente de Gemini
      - Enviará llm_messages al modelo
      - Devolverá el texto de la respuesta generada
    """
    # API key (aún sin usar, pero la dejamos preparada)
    api_key = settings.GEMINI_API_KEY

    # TODO: aquí irá la integración real con Gemini.
    # Por ahora devolvemos una respuesta de ejemplo para poder probar el flujo.
    # Podemos usar el último mensaje del usuario para hacer el fake más agradable.
    last_user_message = None
    for msg in reversed(llm_messages):
        if msg["role"] == "user":
            last_user_message = msg["content"]
            break

    if last_user_message:
        return (
            "👋 Hola, soy TechCareer Assistant (modo demo).\n\n"
            "De momento estoy en una versión de prueba sin conexión real a Gemini, "
            "pero ya puedo ayudarte con dudas generales sobre la plataforma, "
            "tecnología o carrera profesional.\n\n"
            f"He recibido tu mensaje: «{last_user_message}».\n"
            "Cuando activemos la integración con el modelo de lenguaje, "
            "podré responderte de forma mucho más inteligente 😊."
        )

    # Si por alguna razón no hay mensaje de usuario:
    return (
        "👋 Hola, soy TechCareer Assistant (modo demo).\n\n"
        "Todavía no he recibido ninguna pregunta tuya, "
        "pero puedes escribirme para que te ayude con dudas sobre "
        "TechCareer, la plataforma o el mundo tech en general."
    )


def generate_chat_reply(messages: List[ChatMessage]) -> str:
    """
    Función principal del servicio de chat.

    - Recibe la lista de mensajes de la conversación (ChatMessage).
    - Construye la lista de mensajes en formato LLM (añadiendo el SYSTEM_PROMPT).
    - Llama a la función que se encarga de hablar con el modelo (por ahora, fake).
    - Devuelve el texto de respuesta generado por el asistente.
    """
    # 1. Construimos los mensajes para el modelo (con mensaje de sistema incluido)
    llm_messages = _build_llm_messages(messages)

    # 2. Llamamos a la capa que, más adelante, hablará con Gemini
    reply_text = _call_gemini_api(llm_messages)

    # 3. Devolvemos el texto al controller
    return reply_text
