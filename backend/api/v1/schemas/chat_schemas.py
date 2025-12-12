# backend/api/v1/schemas/chat_schemas.py

from typing import Literal, List
from pydantic import BaseModel


class ChatMessage(BaseModel):
    """
    Representa un mensaje individual dentro de la conversación.

    role:
        - "user": mensaje escrito por la persona usuaria
        - "assistant": mensajes previos del asistente (si se envían en el historial)

    content:
        - texto del mensaje
    """
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    """
    Cuerpo de la petición al endpoint de chat.

    messages:
        - lista de mensajes que conforman el historial que el cliente quiere enviar.
        - normalmente, como mínimo, habrá un mensaje con role="user".
    """
    messages: List[ChatMessage]


class ChatResponse(BaseModel):
    """
    Cuerpo de la respuesta del endpoint de chat.

    reply:
        - texto generado por TechCareer Assistant en respuesta al último mensaje del usuario.
    """
    reply: str
