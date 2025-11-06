"""
Main Streamlit application
"""
import streamlit as st
import threading
import time
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


# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = "dashboard"  # Start with home page for testing

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

# Native Streamlit Sidebar - Simple test version
with st.sidebar:
    st.title("Sidebar")
    

# Custom CSS
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    /* Sidebar styling - Make sure it's visible */
    [data-testid="stSidebar"] {
        background-color: #F5F5F5 !important;
        visibility: visible !important;
    }
    
    /* Ensure sidebar toggle button is visible */
    [data-testid="stSidebar"] [data-testid="collapsedControl"] {
        visibility: visible !important;
        display: block !important;
    }
    
    /* Sidebar header with toggle */
    [data-testid="stHeader"] {
        z-index: 1000;
    }
    
    /* Global toggle button - positioned on right edge, always visible */
    .global-sidebar-toggle {
        position: fixed;
        right: 0;
        top: 50%;
        transform: translateY(-50%);
        z-index: 1000;
        transition: right 0.3s ease, left 0.3s ease;
    }
    
    /* When sidebar is collapsed, move button to left */
    [data-testid="stSidebar"].collapsed ~ * .global-sidebar-toggle,
    body:has([data-testid="stSidebar"].collapsed) .global-sidebar-toggle {
        right: auto;
        left: 0;
    }
    
    .global-toggle-btn {
        width: 2.5rem !important;
        height: 2.5rem !important;
        border-radius: 50% !important;
        background-color: #FFFFFF !important;
        border: 2px solid #E0E0E0 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 1.2rem !important;
        color: #000000 !important;
        cursor: pointer !important;
        transition: all 0.2s !important;
    }
    
    .global-toggle-btn:hover {
        background-color: #F5F5F5 !important;
        border-color: #FFD700 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
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
    
    /* Hide Streamlit branding (keep header visible for sidebar toggle) */
    #MainMenu {visibility: hidden;}

    </style>
""", unsafe_allow_html=True)

# Main content area
if st.session_state.page == "home":
    # Simple test page
    st.title("🏠 Home - Prueba 1")
    st.markdown("---")
    st.success("✅ Esta es una página de prueba para verificar que el sidebar funciona correctamente")
    st.info("👈 Mira el sidebar a la izquierda - deberías ver el icono de toggle (☰) en la esquina superior izquierda")
    
    st.markdown("### Instrucciones:")
    st.markdown("""
    1. Busca el icono de menú (☰) en la esquina superior izquierda
    2. Haz clic en él para abrir/cerrar el sidebar
    3. Usa los botones del sidebar para navegar entre páginas
    """)
    
    st.markdown("---")
    st.markdown("**Página actual:** " + st.session_state.page)

elif st.session_state.page == "dashboard":
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
    st.title("Home - Prueba 1")
    st.info("Página de prueba")

