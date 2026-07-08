import pandas as pd

# Simple in-memory store: session_id -> DataFrame
# Good enough for a single-user demo/portfolio project.
# Swap for Redis/DB if this ever needs multi-user persistence.
_sessions: dict[str, pd.DataFrame] = {}

def save_dataframe(session_id: str, df: pd.DataFrame) -> None:
    _sessions[session_id] = df

def get_dataframe(session_id: str) -> pd.DataFrame | None:
    return _sessions.get(session_id)

def session_exists(session_id: str) -> bool:
    return session_id in _sessions