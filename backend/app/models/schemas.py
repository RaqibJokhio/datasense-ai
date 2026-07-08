from pydantic import BaseModel
from typing import Any

class UploadResponse(BaseModel):
    session_id: str
    filename: str
    rows: int
    columns: list[str]
    preview: list[dict[str, Any]]

class ErrorResponse(BaseModel):
    detail: str