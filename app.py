"""
Main Streamlit application
"""
import streamlit as st
import threading
import time
from components.sidebar import render_sidebar
from components.dashboard import render_dashboard
from components.sku_table import render_sku_table
from components.price_calculator import render_price_calculator
import config

# Page configuration
st.set_page_config(
    page_title="Whirlpool Dashboard",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "dashboard"

if 'backend_started' not in st.session_state:
    st.session_state.backend_started = False


def start_backend():
    """Start the FastAPI backend server in a separate thread"""
    if not st.session_state.backend_started:
        try:
            import uvicorn
            import backend
            
            def run_backend():
                uvicorn.run(backend.app, host="0.0.0.0", port=config.API_PORT, log_level="error")
            
            backend_thread = threading.Thread(target=run_backend, daemon=True)
            backend_thread.start()
            st.session_state.backend_started = True
            time.sleep(2)  # Give backend time to start
        except Exception as e:
            st.warning(f"Backend startup issue: {e}. Some features may not work.")


# Start backend
start_backend()

# Custom CSS
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #F5F5F5;
    }
    
    /* Metric cards styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: bold;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 1rem;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        border-radius: 0.5rem;
        background-color: #FF6B35;
        color: white;
        border: none;
    }
    
    .stButton>button:hover {
        background-color: #F7931E;
    }
    
    /* Primary button */
    button[kind="primary"] {
        background-color: #FF6B35 !important;
    }
    
    /* Cards and containers */
    .element-container {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* Table styling */
    .dataframe {
        font-size: 0.9rem;
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background-color: #FF6B35;
    }
    
    /* Chart container */
    .js-plotly-plot {
        background-color: white;
        border-radius: 0.5rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Sidebar
render_sidebar()

# Main content area
if st.session_state.page == "dashboard":
    # Three column layout: main content and calculator
    col1, col2 = st.columns([2.5, 1])
    
    with col1:
        render_dashboard()
        st.markdown("---")
        render_sku_table()
    
    with col2:
        render_price_calculator()

elif st.session_state.page == "tables":
    st.title("Tables")
    st.info("Tables page - Coming soon")
    render_sku_table()

else:
    st.title("Dashboard")
    render_dashboard()

