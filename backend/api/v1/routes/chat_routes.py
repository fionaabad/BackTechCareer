# backend/api/v1/routes/chat_routes.py

from fastapi import APIRouter

from backend.api.v1.schemas.chat_schemas import ChatRequest, ChatResponse
from backend.api.v1.controllers.chat_controller import handle_chat

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("", response_model=ChatResponse)
def chat_endpoint(payload: ChatRequest) -> ChatResponse:
    """
    Endpoint principal del chatbot de TechCareer.

    Recibe el historial de mensajes (ChatRequest) y devuelve
    una respuesta generada por TechCareer Assistant (ChatResponse).
    """
    return handle_chat(payload)
