import uuid
from fastapi import APIRouter, UploadFile, File
from app.services.file_parser import parse_file
from app.services.data_store import save_dataframe
from app.models.schemas import UploadResponse

router = APIRouter(prefix="/api", tags=["upload"])

@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    df = await parse_file(file)

    session_id = str(uuid.uuid4())
    save_dataframe(session_id, df)

    preview = df.head(5).fillna("").to_dict(orient="records")

    return UploadResponse(
        session_id=session_id,
        filename=file.filename,
        rows=len(df),
        columns=df.columns.tolist(),
        preview=preview,
    )