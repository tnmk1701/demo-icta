from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
import shutil

router = APIRouter()
UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/")
async def upload_image(file: UploadFile = File(...)):
    save_path = UPLOAD_DIR / file.filename
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return JSONResponse(content={"url": f"/upload/{file.filename}"})

@router.get("/{filename}")
async def get_uploaded_image(filename: str):
    file_path = UPLOAD_DIR / filename
    if file_path.exists():
        return FileResponse(file_path)
    return JSONResponse(status_code=404, content={"message": "File not found"})
