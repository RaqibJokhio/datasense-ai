import pandas as pd
import numpy as np

def detect_anomalies(df: pd.DataFrame) -> dict:
    """
    Detects outliers in each numeric column using the IQR method.
    IQR = Interquartile Range (Q3 - Q1). Any value outside
    [Q1 - 1.5*IQR, Q3 + 1.5*IQR] is considered an outlier.
    This is a standard, well-known statistical method — not AI-generated.
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if not numeric_cols:
        return {"columns_analyzed": [], "anomalies": {}}

    results = {}

    for col in numeric_cols:
        series = df[col].dropna()
        if len(series) == 0:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

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