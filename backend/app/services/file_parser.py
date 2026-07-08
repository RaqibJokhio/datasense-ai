import pandas as pd
from io import BytesIO
from fastapi import UploadFile, HTTPException

ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}

async def parse_file(file: UploadFile) -> pd.DataFrame:
    ext = "." + file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    contents = await file.read()

    try:
        if ext == ".csv":
            df = pd.read_csv(BytesIO(contents))
        else:
            df = pd.read_excel(BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {str(e)}")

    if df.empty:
        raise HTTPException(status_code=400, detail="Uploaded file has no data")

    return df