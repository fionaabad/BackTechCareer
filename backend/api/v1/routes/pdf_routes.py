from fastapi import APIRouter
from backend.api.v1.controllers.pdf_controller import (
    get_pdf_history,
    delete_pdf
)

router = APIRouter(
    prefix="/api/v1/pdf",
    tags=["PDFs"]
)


@router.get("/history/{user_id}")
def pdf_history_route(user_id: int):
    return get_pdf_history(user_id)


@router.delete("/delete/{pdf_id}")
def delete_pdf_route(pdf_id: int, user_id: int):
    return delete_pdf(pdf_id, user_id)
