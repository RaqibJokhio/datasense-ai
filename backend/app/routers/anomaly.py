from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from io import StringIO
from app.services.data_store import get_dataframe
from app.services.anomaly_detector import detect_anomalies, get_full_outliers_for_column
from app.models.schemas import AnomalyResponse

router = APIRouter(prefix="/api", tags=["anomaly"])

@router.get("/anomalies/{session_id}", response_model=AnomalyResponse)
async def get_anomalies(session_id: str):
    df = get_dataframe(session_id)
    if df is None:
        raise HTTPException(status_code=404, detail="Session not found. Please re-upload the file.")

    result = detect_anomalies(df)
    return AnomalyResponse(**result)


@router.get("/anomalies/{session_id}/download")
async def download_anomalies_csv(session_id: str, column: str):
    df = get_dataframe(session_id)
    if df is None:
        raise HTTPException(status_code=404, detail="Session not found. Please re-upload the file.")

    try:
        outlier_df = get_full_outliers_for_column(df, column)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    buffer = StringIO()
    outlier_df.to_csv(buffer, index=False)
    buffer.seek(0)

    safe_column_name = "".join(c if c.isalnum() else "_" for c in column)
    filename = f"anomalies_{safe_column_name}.csv"

    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )