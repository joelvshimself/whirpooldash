import logging
import pickle
from functools import lru_cache
from io import BytesIO
from typing import List, Optional

import numpy as np
import pandas as pd
import requests
import xgboost  # noqa: F401 - ensures pickle can import xgboost objects

logger = logging.getLogger(__name__)


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


def predict_price_scenario_xgb_from_pickle(
    sku_list: List[str],
    date_input: str,
    inflation_adjustment: float = 0.0,
    model_path: str = 'https://modelstoragest.blob.core.windows.net/models/xgboost_model.pkl?sp=r&st=2025-12-01T18:33:44Z&se=2026-03-06T02:48:44Z&sv=2024-11-04&sr=b&sig=eeRT9WytrsP4aCIijJngHAskPs4WobFtkJeClwnuRxA%3D',
    columns_path: str = 'https://modelstoragest.blob.core.windows.net/data/xgb_encoded_columns.pkl?sp=r&st=2025-12-01T18:36:04Z&se=2026-03-07T02:51:04Z&sv=2024-11-04&sr=b&sig=mc4wcriw68V5Hl0%2FXDabxul3O0ottE5qwPxr48XCUkg%3D',
    df_path: str = 'https://modelstoragest.blob.core.windows.net/data/xgb_source_data.pkl?sp=r&st=2025-12-01T18:36:32Z&se=2026-03-20T02:51:32Z&sv=2024-11-04&sr=b&sig=KWYG7OAExjvkad77eam9%2BzcWtYyM%2FShn%2Fnxfq5FoCC4%3D'
) -> Optional[pd.DataFrame]:
    """
    Predice precios usando el modelo XGBoost cargado desde pickle.
    Similar a predict_price_scenario_xgb pero carga el modelo desde archivos pickle.
    
    Args:
        sku_list: Lista de SKUs a predecir (ej: ['WFR5000D'])
        date_input: Fecha de predicción (ej: '2025-11-18')
        inflation_adjustment: Ajuste de inflación (ej: 0.04 para +4%)
        model_path: Ruta al modelo guardado
        columns_path: Ruta a las columnas codificadas
        df_path: Ruta al dataset fuente
    
    Returns:
        DataFrame con predicciones listas para graficarse
    """
    logger.info("Starting XGBoost prediction for SKUs=%s, date=%s", sku_list, date_input)
    # Cargar recursos desde Azure Blob
    trained_model = _load_remote_pickle(model_path)
    X_encoded_columns = _load_remote_pickle(columns_path)
    df_source = _load_remote_pickle(df_path)
    
    # Usar la misma lógica que predict_price_scenario_xgb
    df_latest = df_source[df_source['SKU'].isin(sku_list)].copy()
    df_latest = (
        df_latest.sort_values(['SKU', 'TP', 'DATE'])
        .groupby(['SKU', 'TP'])
        .tail(1)
    )
    
    if df_latest.empty:
        logger.warning("No data found for SKUs=%s", sku_list)
        return None

    X_future = df_latest[['INV', 'QTY', 'GROSS_SALES', 'SKU', 'TP', 'CATEGORY']].copy()
    X_future_encoded = pd.get_dummies(
        X_future, columns=['SKU', 'TP', 'CATEGORY'], drop_first=True
    )

    missing_cols = set(X_encoded_columns) - set(X_future_encoded.columns)
    for c in missing_cols:
        X_future_encoded[c] = 0

    X_future_encoded = X_future_encoded[X_encoded_columns]

    preds = trained_model.predict(X_future_encoded)
    preds = np.maximum(preds, 0)

    if inflation_adjustment != 0:
        preds = preds * (1 + inflation_adjustment)

    result = df_latest[['SKU', 'CATEGORY', 'TP']].copy()
    result['Predicted_Date'] = date_input
    result['Predicted_Real_Price'] = preds.round(2)
    result['Adjusted_for_Inflation'] = (
        f"+{inflation_adjustment*100:.1f}%" if inflation_adjustment != 0 else "—"
    )

    result = result.sort_values(['CATEGORY', 'SKU', 'TP']).reset_index(drop=True)
    logger.info(
        "Prediction ready: %d rows (SKU=%s, date=%s)",
        len(result),
        sku_list,
        date_input,
    )
    return result