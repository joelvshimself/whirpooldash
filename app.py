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

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'username' not in st.session_state:
    st.session_state.username = None


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


def render_login():
    """Render login page"""
    st.markdown("""
        <style>
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 2rem;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        st.title("🌀 Whirlpool Dashboard")
        st.markdown("### Login")
        
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", type="primary", use_container_width=True):
            if username and password:
                # Call authentication endpoint
                import requests
                try:
                    response = requests.post(
                        f"{config.API_BASE_URL}/api/auth/login",
                        json={"username": username, "password": password},
                        timeout=5
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("success"):
                            st.session_state.authenticated = True
                            st.session_state.username = data.get("username")
                            st.success("Login successful!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(data.get("message", "Invalid credentials"))
                    else:
                        st.error("Authentication service unavailable")
                except Exception as e:
                    st.error(f"Error connecting to authentication service: {e}")
            else:
                st.warning("Please enter both username and password")
        
        st.markdown("---")
        st.info("Default credentials: **admin** / **admin**")
        st.markdown("</div>", unsafe_allow_html=True)


# Check authentication
if not st.session_state.authenticated:
    render_login()
    st.stop()

# Native Streamlit Sidebar - Only show if authenticated
with st.sidebar:
    st.title("Navigation")
    
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
    
    if st.button("📊 Dashboard", use_container_width=True):
        st.session_state.page = "dashboard"
        st.rerun()
    
    if st.button("📋 Tables", use_container_width=True):
        st.session_state.page = "tables"
        st.rerun()
    
    st.markdown("---")
    st.markdown(f"**Logged in as:** {st.session_state.username}")
    if st.button("Logout", type="secondary", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()
    

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

