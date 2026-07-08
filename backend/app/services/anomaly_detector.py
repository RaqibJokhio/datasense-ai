import pandas as pd
import numpy as np


def _get_outlier_bounds(series: pd.Series) -> tuple[float, float]:
    """
    Calculates IQR (Interquartile Range) bounds for outlier detection.
    IQR = Q3 - Q1. Anything outside [Q1 - 1.5*IQR, Q3 + 1.5*IQR] is an outlier.
    This is a standard, well-known statistical method — not AI-generated.
    """
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return lower_bound, upper_bound


def detect_anomalies(df: pd.DataFrame) -> dict:
    """Returns a summary of anomalies per numeric column, capped at 10 example rows each."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if not numeric_cols:
        return {"columns_analyzed": [], "anomalies": {}}

    results = {}

    for col in numeric_cols:
        series = df[col].dropna()
        if len(series) == 0:
            continue

        lower_bound, upper_bound = _get_outlier_bounds(series)
        outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
        outlier_rows = df[outlier_mask]

        if len(outlier_rows) > 0:
            results[col] = {
                "count": int(len(outlier_rows)),
                "lower_bound": round(float(lower_bound), 2),
                "upper_bound": round(float(upper_bound), 2),
                "outliers": outlier_rows.head(10).fillna("").to_dict(orient="records"),
            }

    return {
        "columns_analyzed": numeric_cols,
        "anomalies": results,
    }


def get_full_outliers_for_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Returns ALL outlier rows for a single column, uncapped — used for CSV export."""
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in dataset.")

    series = df[column].dropna()
    if len(series) == 0:
        return pd.DataFrame(columns=df.columns)

    lower_bound, upper_bound = _get_outlier_bounds(series)
    outlier_mask = (df[column] < lower_bound) | (df[column] > upper_bound)
    return df[outlier_mask]