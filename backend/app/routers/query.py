from fastapi import APIRouter, HTTPException
from app.services.data_store import get_dataframe
from app.services.llm_service import generate_pandas_code
from app.services.code_executor import execute_code
from app.services.result_formatter import format_result
from app.models.schemas import QueryRequest, QueryResponse

router = APIRouter(prefix="/api", tags=["query"])

@router.post("/query", response_model=QueryResponse)
async def query_data(request: QueryRequest):
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    df = get_dataframe(request.session_id)
    if df is None:
        raise HTTPException(status_code=404, detail="Session not found. Please re-upload the file.")

    dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}
    code = await generate_pandas_code(request.question, df.columns.tolist(), dtypes)

    result = execute_code(code, df)
    formatted = format_result(result)

    return QueryResponse(
        question=request.question,
        generated_code=code,
        result_type=formatted["type"],
        result_data=formatted["data"],
    )