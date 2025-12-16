from fastapi import APIRouter, status
from backend.api.v1.schemas.pdf_schemas import PdfCreate
from backend.api.v1.controllers.pdf_controller import (
    upload_pdf,
    get_user_pdfs,
    delete_pdf
)

router = APIRouter(
    prefix="/pdfs",
    tags=["PDFs"]
)

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
def create_pdf(data: PdfCreate):
    return upload_pdf(data)


@router.get(
    "/user/{user_id}",
    status_code=status.HTTP_200_OK
)
def list_user_pdfs(user_id: int):
    return get_user_pdfs(user_id)


@router.delete(
    "/{pdf_id}",
    status_code=status.HTTP_200_OK
)
def remove_pdf(pdf_id: int):
    return delete_pdf(pdf_id)
