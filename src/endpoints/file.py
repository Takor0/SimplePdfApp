from fastapi import APIRouter, UploadFile

from src.config import UPLOAD_DIR

router = APIRouter(
    prefix="/api/file",
    tags=["file"],
)


@router.post("/pdf/")
def upload_pdf(file: UploadFile):
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return file.filename
