# backend/api/v1/controllers/chat_controller.py

from typing import List

from fastapi import HTTPException, status

from backend.api.v1.schemas.chat_schemas import ChatRequest, ChatResponse, ChatMessage
from backend.api.v1.services.chat_service import generate_chat_reply


def handle_chat(request: ChatRequest) -> ChatResponse:
    """
    Controlador del chat.

    - Valida que haya al menos un mensaje de usuario.
    - Llama al servicio de chat para generar la respuesta.
    - Envuelve el resultado en un ChatResponse.
    """

    # Validación básica: debe haber al menos un mensaje
    if not request.messages:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La petición de chat debe incluir al menos un mensaje.",
        )

    # (Opcional) Validación extra: al menos un mensaje de role="user"
    has_user_message = any(m.role == "user" for m in request.messages)
    if not has_user_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe existir al menos un mensaje del usuario (role='user').",
        )

    # Llamamos al servicio para obtener la respuesta de texto
    reply_text = generate_chat_reply(request.messages)

    # Devolvemos la respuesta en el modelo Pydantic definido
    return ChatResponse(reply=reply_text)
