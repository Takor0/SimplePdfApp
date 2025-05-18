from fastapi import APIRouter, UploadFile, HTTPException
from starlette import status
from starlette.responses import FileResponse
from werkzeug.utils import secure_filename

from src.config import UPLOAD_DIR, RESULTS_DIR
from src.cosntants import ALLOWED_EXTENSIONS

router = APIRouter(
    prefix="/api/file",
    tags=["file"],
)


@router.post("/upload")
def upload_file(file: UploadFile):
    extension = file.filename.split(".")[-1]
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"File type '{extension}' not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}",
        )
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return file.filename


@router.get("/download-result")
def download_result(file_name: str):
    file_path = RESULTS_DIR / secure_filename(file_name)
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File '{file_name}' not found.",
        )
    return FileResponse(
        file_path,
        media_type="application/zip",
        filename=file_name,
    )
