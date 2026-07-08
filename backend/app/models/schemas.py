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

class QueryRequest(BaseModel):
    session_id: str
    question: str

class QueryResponse(BaseModel):
    question: str
    generated_code: str
    result_type: str
    result_data: Any