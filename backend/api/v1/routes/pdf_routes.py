from fastapi import APIRouter, UploadFile, File
from api.v1.controllers.pdf_controller import upload_pdf, get_pdf_history
from api.v1.controllers.pdf_controller import delete_pdf, delete_pdf


router = APIRouter(prefix="/pdf", tags=["PDFs"])

@router.post("/upload")
def upload_pdf_route(user_id: int, file: UploadFile = File(...)):
    return upload_pdf(file, user_id)

@router.get("/history/{user_id}")
def pdf_history_route(user_id: int):
    return get_pdf_history(user_id)

@router.delete("/delete/{pdf_id}")
def delete_pdf_route(pdf_id: int, user_id: int):
    return delete_pdf(pdf_id, user_id)
