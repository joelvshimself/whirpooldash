# Installation Guide

## Installed Packages

The following packages have been successfully installed:
- ✅ streamlit (1.51.0)
- ✅ fastapi (0.121.0)
- ✅ uvicorn (0.38.0)
- ✅ plotly (already installed)
- ✅ pandas (already installed)
- ✅ numpy (already installed)
- ✅ requests (already installed)

## Optional ML Dependencies

Due to PyPy compatibility limitations, the following packages are **optional**:
- ⚠️ TensorFlow - Not compatible with PyPy. The app uses a simple trend-based prediction fallback.
- ⚠️ scikit-learn - Has build issues with PyPy. The app uses a custom numpy-based scaler.

**Note:** If you switch to CPython (standard Python), you can install these for full LSTM functionality:
```bash
pip install tensorflow scikit-learn
```

## Running the Application

```bash
streamlit run app.py
```

The backend API will start automatically on port 8000.

## Current Status

✅ All core dependencies installed
✅ Application ready to run
✅ Fallback implementations work without TensorFlow/scikit-learn
✅ Price predictions use simple trend-based algorithm when ML libraries unavailable

## Features Working

- Dashboard with KPIs and charts
- SKU table
- Price Calculator (with fallback prediction algorithm)
- Backend API server
- Data abstraction layer (mock data)

