"""
Main Streamlit application
"""
import streamlit as st
import os
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

# Native Streamlit Sidebar - Company logo + chips + account section
with st.sidebar:
    # Company logo
    logo_candidates = [
        "assets/whirpool_logo.png",
        "assets/whirlpool_logo.png",
        "assets/logo.png",
        "assets/logo.jpg",
        "assets/logo.jpeg",
        "assets/logo.svg",
        "assets/logo.webp",
    ]
    logo_path = next((p for p in logo_candidates if os.path.exists(p)), None)
    if not logo_path:
        try:
            for fname in os.listdir("assets"):
                if fname.lower().endswith((".png", ".jpg", ".jpeg", ".svg", ".webp")):
                    logo_path = os.path.join("assets", fname)
                    break
        except Exception:
            pass
    if logo_path:
        st.image(logo_path, use_container_width=True)
    else:
        st.markdown("### Your Company")

    st.markdown("---")

    # Chip-like navigation
    is_dashboard = st.session_state.page == "dashboard"
    is_tables = st.session_state.page == "tables"

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Dashboard", use_container_width=True, type="primary" if is_dashboard else "secondary"):
            st.session_state.page = "dashboard"
            st.rerun()
    with col2:
        if st.button("Tables", use_container_width=True, type="primary" if is_tables else "secondary"):
            st.session_state.page = "tables"
            st.rerun()

    st.markdown("---")

    # Account/profile section
    st.markdown("#### Account")
    st.caption("Signed in as: user@example.com")
    if st.button("Logout", use_container_width=True):
        # Simple placeholder action for logout
        st.success("Logged out")

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
    /* Sidebar logo sizing */
    [data-testid="stSidebar"] img {
        max-height: 64px;
        width: auto;
        display: block;
        margin: 4px auto 12px auto;
        object-fit: contain;
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
        border-radius: 999px; /* pill shape for chips */
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
    button[kind="secondary"] {
        background-color: #F3F3F3 !important;
        color: #2D2D2D !important;
        border: 1px solid #E0E0E0 !important;
    }
    
    /* Cards and containers (main content default) */
    .element-container {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    /* Remove bubble effect on the sidebar */
    [data-testid="stSidebar"] .element-container {
        background-color: transparent !important;
        padding: 0 !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        border: none !important;
        margin-bottom: 0.5rem !important;
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

