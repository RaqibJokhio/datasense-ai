import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # no GUI backend needed on a server
import matplotlib.pyplot as plt
from fastapi import HTTPException

# Only these names are visible to the executed code.
# Anything not in this dict (os, open, __import__, etc.) simply doesn't exist to it.
SAFE_GLOBALS = {
    "pd": pd,
    "np": np,
    "plt": plt,
    "__builtins__": {
        "len": len, "range": range, "sum": sum, "min": min, "max": max,
        "sorted": sorted, "list": list, "dict": dict, "set": set,
        "str": str, "int": int, "float": float, "bool": bool,
        "round": round, "abs": abs, "enumerate": enumerate, "zip": zip,
    },
}

def execute_code(code: str, df: pd.DataFrame):
    local_vars = {"df": df}

    try:
        exec(code, SAFE_GLOBALS, local_vars)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Code execution failed: {str(e)}")

    result = local_vars.get("result")

    if result is None:
        raise HTTPException(status_code=400, detail="Generated code did not produce a 'result' variable")

    return result