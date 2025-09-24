from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from app.services import tabular_service

router = APIRouter()

@router.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    # simple mock: save uploaded file to data/uploads and parse if csv/xlsx
    content = await file.read()
    path = f"data/uploads/{file.filename}"
    with open(path, "wb") as f:
        f.write(content)
    parsed = tabular_service.parse_file(path)
    return JSONResponse({'filename': file.filename, 'parsed_preview': parsed[:5] if isinstance(parsed, list) else str(parsed)})