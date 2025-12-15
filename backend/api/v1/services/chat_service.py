# backend/api/v1/services/chat_service.py

from typing import List, Dict, Any

from core.chat_prompt import SYSTEM_PROMPT
from core.config import settings
from api.v1.schemas.chat_schemas import ChatMessage
import google.generativeai as genai
from fastapi import HTTPException


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
    Implementación REAL de la llamada a Gemini.

    - Lee la API key desde settings.GEMINI_API_KEY
    - Configura el cliente de Gemini
    - Construye un prompt a partir de los mensajes (system + user/assistant)
    - Llama al modelo y devuelve el texto de la respuesta

    Si falta la API key o hay un error al llamar a la API,
    lanza una HTTPException para que FastAPI devuelva un error claro.
    """
    api_key = settings.GEMINI_API_KEY

    if not api_key:
        # Si no hay API key configurada, devolvemos un error 500 claro
        raise HTTPException(
            status_code=500,
            detail="Gemini API key no configurada. Define GEMINI_API_KEY en el archivo .env.",
        )

    # Configuramos el cliente de Gemini con la API key
    genai.configure(api_key=api_key)

    # Para simplificar, vamos a convertir la lista de mensajes en un único prompt de texto.
    # Podríamos mapear roles de forma más sofisticada, pero para este uso nos vale
    # concatenar el mensaje de sistema y luego los mensajes de usuario/assistant.
    # El SYSTEM_PROMPT ya viene como primer mensaje (role="system") desde _build_llm_messages.

    system_part = ""
    conversation_parts: List[str] = []

    for msg in llm_messages:
        role = msg["role"]
        content = msg["content"]

        if role == "system":
            # Nos quedamos con el prompt del sistema
            system_part = content
        elif role == "user":
            conversation_parts.append(f"Usuario: {content}")
        elif role == "assistant":
            conversation_parts.append(f"Asistente: {content}")

    # Construimos el prompt final que daremos al modelo
    full_prompt = system_part.strip() + "\n\n" + "\n".join(conversation_parts).strip()

    try:
        # Creamos el modelo de Gemini que quieras usar (por ejemplo, gemini-1.5-flash)
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Llamamos al modelo con el prompt
        response = model.generate_content(full_prompt)

        # Extraemos el texto de la respuesta
        reply_text = response.text if hasattr(response, "text") else str(response)

        if not reply_text:
            raise HTTPException(
                status_code=502,
                detail="Gemini no devolvió texto en la respuesta.",
            )

        return reply_text

    except HTTPException:
        # Re-lanzamos errores HTTP tal cual
        raise
    except Exception as e:
        # Cualquier otro error lo traducimos a un 502 para el cliente
        raise HTTPException(
            status_code=502,
            detail=f"Error al comunicarse con Gemini: {e}",
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
