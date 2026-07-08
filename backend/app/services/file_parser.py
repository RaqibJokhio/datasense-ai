import pandas as pd
from io import BytesIO
from fastapi import UploadFile, HTTPException

ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

async def parse_file(file: UploadFile) -> pd.DataFrame:
    if not file.filename or "." not in file.filename:
        raise HTTPException(status_code=400, detail="File has no name or extension.")

    ext = "." + file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}. Please upload a CSV or Excel file.")

    contents = await file.read()

    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")

    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail=f"File too large. Maximum size is {MAX_FILE_SIZE_MB}MB.")

    try:
        if ext == ".csv":
            df = pd.read_csv(BytesIO(contents))
        else:
            df = pd.read_excel(BytesIO(contents))
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to parse file. Make sure it's a valid CSV or Excel file with a proper header row.")

    if df.empty:
        raise HTTPException(status_code=400, detail="Uploaded file has no data rows.")

    if len(df.columns) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file has no columns.")

    return df