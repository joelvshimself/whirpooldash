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
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Sidebar
render_sidebar()

# Floating toggle button - always visible on the left
if 'sidebar_collapsed' not in st.session_state:
    st.session_state.sidebar_collapsed = False

# Update CSS for floating button
st.markdown("""
<style>
/* Floating toggle button - fixed on left side */
.floating-toggle-btn {
    position: fixed !important;
    left: 1rem !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    z-index: 9999 !important;
    width: 3rem !important;
    height: 3rem !important;
    border-radius: 50% !important;
    background-color: #FFFFFF !important;
    border: 2px solid #FFD700 !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 1.5rem !important;
    color: #000000 !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    padding: 0 !important;
    margin: 0 !important;
}

.floating-toggle-btn:hover {
    background-color: #FFD700 !important;
    border-color: #FFA500 !important;
    box-shadow: 0 6px 16px rgba(0,0,0,0.3) !important;
    transform: translateY(-50%) scale(1.1) !important;
}

.floating-toggle-btn:active {
    transform: translateY(-50%) scale(0.95) !important;
}

/* Sidebar collapse animation */
[data-testid="stSidebar"].collapsed {
    transform: translateX(-100%) !important;
    transition: transform 0.3s ease !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

[data-testid="stSidebar"]:not(.collapsed) {
    transform: translateX(0) !important;
    transition: transform 0.3s ease !important;
    opacity: 1 !important;
    pointer-events: auto !important;
}

/* Ensure sidebar is visible by default */
[data-testid="stSidebar"] {
    visibility: visible !important;
    display: block !important;
    opacity: 1 !important;
}
</style>
""", unsafe_allow_html=True)

# Create floating button with JavaScript
toggle_icon = "▶" if st.session_state.sidebar_collapsed else "◀"

st.markdown(f"""
<button class="floating-toggle-btn" id="floating-sidebar-toggle">
    {toggle_icon}
</button>

<script>
(function() {{
    const sidebar = document.querySelector('[data-testid="stSidebar"]');
    const toggleBtn = document.getElementById('floating-sidebar-toggle');
    const isCollapsed = {str(st.session_state.sidebar_collapsed).lower()};
    
    // Apply initial state immediately - wait for DOM to be ready
    function applyInitialState() {{
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        const btn = document.getElementById('floating-sidebar-toggle');
        
        if (sidebar && btn) {{
            if ({str(st.session_state.sidebar_collapsed).lower()}) {{
                sidebar.classList.add('collapsed');
                btn.textContent = '▶';
            }} else {{
                sidebar.classList.remove('collapsed');
                btn.textContent = '◀';
            }}
        }}
    }}
    
    // Try multiple times to ensure sidebar is found
    applyInitialState();
    setTimeout(applyInitialState, 100);
    setTimeout(applyInitialState, 500);
    
    // Add click handler
    if (toggleBtn) {{
        toggleBtn.addEventListener('click', function(e) {{
            e.preventDefault();
            e.stopPropagation();
            
            if (sidebar) {{
                const currentlyCollapsed = sidebar.classList.contains('collapsed');
                const newState = !currentlyCollapsed;
                
                // Force sidebar to be visible before toggling
                sidebar.style.display = 'block';
                sidebar.style.visibility = 'visible';
                sidebar.style.opacity = '1';
                
                if (newState) {{
                    // Hide sidebar
                    sidebar.classList.add('collapsed');
                    toggleBtn.textContent = '▶';
                }} else {{
                    // Show sidebar - ensure it's visible
                    sidebar.classList.remove('collapsed');
                    sidebar.style.display = 'block';
                    sidebar.style.visibility = 'visible';
                    sidebar.style.opacity = '1';
                    sidebar.style.transform = 'translateX(0)';
                    toggleBtn.textContent = '◀';
                }}
                
                // Find and click Streamlit button to persist state
                setTimeout(function() {{
                    // Try multiple selectors
                    let streamlitBtn = document.querySelector('button[key="sidebar_toggle"]');
                    if (!streamlitBtn) {{
                        // Find by text
                        const allButtons = document.querySelectorAll('button');
                        allButtons.forEach(btn => {{
                            if (btn.textContent.trim() === 'Toggle') {{
                                streamlitBtn = btn;
                            }}
                        }});
                    }}
                    
                    if (streamlitBtn) {{
                        streamlitBtn.click();
                    }} else {{
                        // Force rerun if button not found
                        console.log('Triggering rerun');
                        window.location.reload();
                    }}
                }}, 100);
            }}
        }}, true);
    }}
}})();
</script>
""", unsafe_allow_html=True)

# Hidden Streamlit button to persist state - make it more accessible
st.markdown("""
<div style="position: absolute; left: -9999px; width: 1px; height: 1px; overflow: hidden;">
""", unsafe_allow_html=True)
if st.button("Toggle", key="sidebar_toggle"):
    st.session_state.sidebar_collapsed = not st.session_state.sidebar_collapsed
    st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

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

