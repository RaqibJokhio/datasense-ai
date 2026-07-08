from fastapi import APIRouter, HTTPException
from app.services.data_store import get_dataframe
from app.services.anomaly_detector import detect_anomalies
from app.models.schemas import AnomalyResponse

router = APIRouter(prefix="/api", tags=["anomaly"])

@router.get("/anomalies/{session_id}", response_model=AnomalyResponse)
async def get_anomalies(session_id: str):
    df = get_dataframe(session_id)
    if df is None:
        raise HTTPException(status_code=404, detail="Session not found. Please re-upload the file.")

    result = detect_anomalies(df)
    return AnomalyResponse(**result)