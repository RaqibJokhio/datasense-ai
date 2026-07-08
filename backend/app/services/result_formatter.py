import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def format_result(result) -> dict:
    """Converts whatever the executed code produced into a JSON-safe response."""

    # Case 1: it's a matplotlib figure
    if isinstance(result, plt.Figure):
        buf = BytesIO()
        result.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode("utf-8")
        plt.close(result)
        return {"type": "chart", "data": f"data:image/png;base64,{img_base64}"}

    # Case 2: it's a DataFrame
    if isinstance(result, pd.DataFrame):
        return {"type": "table", "data": result.fillna("").to_dict(orient="records")}

    # Case 3: it's a Series
    if isinstance(result, pd.Series):
        return {"type": "table", "data": result.fillna("").reset_index().to_dict(orient="records")}

    # Case 4: numpy scalar (e.g. np.float64)
    if isinstance(result, (np.integer, np.floating)):
        return {"type": "value", "data": result.item()}

    # Case 5: plain number, string, list, dict
    if isinstance(result, (int, float, str, list, dict, bool)):
        return {"type": "value", "data": result}

    # Fallback: stringify anything unexpected
    return {"type": "value", "data": str(result)}