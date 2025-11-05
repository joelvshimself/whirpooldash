# Whirlpool Dashboard

Internal WHP Dashboard built with Streamlit, featuring a comprehensive dashboard with KPIs, charts, SKU management, and an integrated Price Calculator with LSTM backend.

## Features

- **Dashboard**: Real-time KPIs, sales overview charts, and active user metrics
- **SKU Management**: Top 10 SKUs table with completion tracking
- **Price Calculator**: LSTM-powered price prediction with HTTP API integration
- **Modular Architecture**: Clean separation of concerns with data abstraction layer

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

The backend API server will start automatically on port 8000.

## Architecture

- **Frontend**: Streamlit dashboard
- **Backend**: FastAPI server with LSTM model
- **Data Layer**: Abstract data source interface (currently using mock data)
- **ML**: TensorFlow/Keras LSTM model for price prediction

## Configuration

Edit `config.py` to:
- Change data source (mock to database)
- Configure API endpoints
- Adjust default values

## Project Structure

```
whirpooldash/
├── app.py                 # Main Streamlit entry point
├── backend.py             # FastAPI backend server
├── config.py              # Configuration
├── data/                  # Data source abstraction
├── services/              # Business logic services
├── ml/                    # Machine learning models
├── components/            # UI components
└── utils/                 # Utility functions
```

