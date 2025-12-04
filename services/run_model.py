import logging
import pickle
from functools import lru_cache
from io import BytesIO
from typing import Any, Dict, Tuple, Union
from datetime import datetime

import pandas as pd
import requests
import xgboost  # noqa: F401 - ensures pickle can import xgboost objects

logger = logging.getLogger(__name__)

FINAL_MODEL_PATH = (
    "https://modelstoragest.blob.core.windows.net/models/final_xgb_model.pkl?"
    "sp=r&st=2025-12-02T03:34:14Z&se=2026-01-16T11:49:14Z&sv=2024-11-04&sr=b&"
    "sig=0RIRxO3ObExUaEeTSwkjCUkjALTt7z%2BmDlifnZVlecU%3D"
)
FINAL_COLUMNS_PATH = (
    "https://modelstoragest.blob.core.windows.net/data/final_xgb_encoded_columns.pkl?"
    "sp=r&st=2025-12-02T03:40:41Z&se=2026-01-29T11:55:41Z&sv=2024-11-04&sr=b&"
    "sig=0jjkvyd2NtZB8rOk8PvrsXR29QHkNNebe11zH4Bsxug%3D"
)
FINAL_SOURCE_DATA_PATH = (
    "https://modelstoragest.blob.core.windows.net/data/final_xgb_source_data.pkl?"
    "sp=r&st=2025-12-02T03:36:29Z&se=2026-01-23T11:51:29Z&sv=2024-11-04&sr=b&"
    "sig=NMp6i38erBfXcrkBRYD15gmAjifrjCTC2v7835ez8Fo%3D"
)


@lru_cache(maxsize=16)
def _load_remote_pickle(url: str):
    """
    Download a pickle file from Azure Blob Storage and deserialize it.
    Cached to avoid repeated downloads across reruns.
    """
    logger.info("Downloading pickle resource from %s", url)
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    obj = pickle.load(BytesIO(response.content))
    logger.debug("Loaded pickle from %s (type=%s)", url, type(obj))
    return obj


def _format_date(value: Union[str, datetime, pd.Timestamp]) -> str:
    """Convert timestamps/strings to YYYY-MM-DD strings."""
    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d")
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")
    return str(value)


def price_comparison_table(
    df: pd.DataFrame,
    model: Any,
    feature_cols,
    tp: str,
    sku: str,
    pred_date: str,
) -> Tuple[pd.DataFrame, str]:
    """
    Construye la tabla de comparación entre el último precio y la predicción.
    Devuelve el DataFrame listo para usarse y el HTML estilizado.
    """
    latest_rows = df[(df["TP"] == tp) & (df["SKU"] == sku)].sort_values("DATE")
    if latest_rows.empty:
        raise ValueError(f"No history for SKU={sku} with TP={tp}")

    past = latest_rows.iloc[-1]
    past_price = float(past["Real_price"])
    past_period = _format_date(past["DATE"])
    category = past["CATEGORY"]
    inflation = float(past.get("INFLATION", 0.0))

    base_row = pd.DataFrame(
        [
            {
                "INV": 1,
                "QTY": 1,
                "GROSS_SALES": past["GROSS_SALES"],
                "SKU": sku,
                "TP": tp,
                "CATEGORY": category,
            }
        ]
    )

    encoded_row = (
        pd.get_dummies(base_row, columns=["SKU", "TP", "CATEGORY"])
        .reindex(columns=feature_cols, fill_value=0)
    )

    pred_price = float(model.predict(encoded_row)[0])
    pct_change = (
        ((pred_price - past_price) / past_price) * 100 if past_price != 0 else None
    )

    result_df = pd.DataFrame(
        {
            "SKU": [sku],
            "CATEGORY": [category],
            "Past Period": [past_period],
            "Past Price/Unit": [past_price],
            "Prediction Date": [pred_date],
            "Predicted Price/Unit": [pred_price],
            "% Change": [pct_change],
            "INF": [inflation],
        }
    )

    styler = (
        result_df.style.set_properties(
            subset=["Past Period", "Past Price/Unit"],
            **{"background-color": "gray", "color": "white"},
        )
        .set_properties(
            subset=["Prediction Date", "Predicted Price/Unit"],
            **{"background-color": "#FFC700", "color": "white"},
        )
        .format(
            {
                "Past Price/Unit": "{:,.2f}".format,
                "Predicted Price/Unit": "{:,.2f}".format,
                "% Change": (lambda x: f"{x:,.2f}%" if x is not None else "—"),
                "INF": "{:,.6f}".format,
            }
        )
        .set_caption(f"Showing {tp.upper()} – {sku} for {pred_date}")
    )

    table_html = styler.to_html()
    return result_df, table_html


def generate_price_prediction_statement(
    sku: str,
    tp: str,
    prediction_date: Union[str, datetime],
    model_path: str = FINAL_MODEL_PATH,
    columns_path: str = FINAL_COLUMNS_PATH,
    df_path: str = FINAL_SOURCE_DATA_PATH,
) -> Dict[str, Any]:
    """
    Ejecuta el modelo final y devuelve un statement listo para mostrarse.
    """
    pred_date = (
        prediction_date.strftime("%Y-%m-%d")
        if hasattr(prediction_date, "strftime")
        else str(prediction_date)
    )

    trained_model = _load_remote_pickle(model_path)
    encoded_columns = _load_remote_pickle(columns_path)
    df_source = _load_remote_pickle(df_path)
    
    result_df, table_html = price_comparison_table(
        df=df_source,
        model=trained_model,
        feature_cols=encoded_columns,
        tp=tp,
        sku=sku,
        pred_date=pred_date,
    )

    row = result_df.iloc[0]
    pct_change = row["% Change"]

    return {
        "table_df": result_df,
        "table_html": table_html,
        "sku": sku,
        "tp": tp,
        "category": row["CATEGORY"],
        "prediction_date": pred_date,
        "past_period": row["Past Period"],
        "past_price": row["Past Price/Unit"],
        "predicted_price": row["Predicted Price/Unit"],
        "pct_change": pct_change,
        "inflation": row["INF"],
    }