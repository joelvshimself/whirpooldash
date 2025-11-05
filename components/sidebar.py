"""
Sidebar navigation component with toggle functionality
Precisely matches the design with interactive toggle/untoggle
"""
import streamlit as st


def render_sidebar():
    """Render the left sidebar with navigation matching the design"""
    
    # Initialize page state
    if 'page' not in st.session_state:
        st.session_state.page = "dashboard"
    
    # Initialize account page state  
    if 'account_page' not in st.session_state:
        st.session_state.account_page = None
    
    with st.sidebar:
        # Custom CSS for sidebar - matches design precisely
        st.markdown("""
        <style>
        /* Sidebar background */
        [data-testid="stSidebar"] {
            background-color: #F5F5F5;
        }
        
        /* Branding area */
        .whirlpool-brand {
            padding: 1.5rem 1rem 1rem 1rem;
            text-align: left;
        }
        
        .whirlpool-logo {
            font-size: 1.5rem;
            font-weight: bold;
            color: #000000;
            margin-bottom: 0.25rem;
            position: relative;
            display: inline-block;
        }
        
        .whirlpool-logo::before {
            content: '';
            position: absolute;
            left: -0.5rem;
            top: 50%;
            transform: translateY(-50%);
            width: 2rem;
            height: 2rem;
            background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
            border-radius: 50%;
            opacity: 0.7;
            z-index: -1;
        }
        
        .whirlpool-corp {
            font-size: 0.7rem;
            color: #000000;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 0.25rem;
        }
        
        /* Divider */
        .sidebar-divider {
            height: 1px;
            background-color: #E0E0E0;
            margin: 1rem 0;
            border: none;
        }
        
        /* Navigation button styling - target all sidebar buttons */
        [data-testid="stSidebar"] button {
            width: 100% !important;
            padding: 0.75rem 1rem !important;
            margin: 0.25rem 0 !important;
            border-radius: 0.5rem !important;
            border: none !important;
            text-align: left !important;
            font-size: 0.95rem !important;
            font-weight: 500 !important;
            transition: all 0.2s !important;
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
        }
        
        /* Inactive state - default gray */
        [data-testid="stSidebar"] button[kind="secondary"] {
            background-color: #F5F5F5 !important;
            color: #9E9E9E !important;
        }
        
        /* Active state - white background */
        [data-testid="stSidebar"] button[kind="primary"] {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }
        
        /* Button hover */
        [data-testid="stSidebar"] button[kind="secondary"]:hover {
            background-color: #EEEEEE !important;
        }
        
        [data-testid="stSidebar"] button[kind="primary"]:hover {
            background-color: #FFFFFF !important;
        }
        
        /* Add icon box before text for all buttons */
        [data-testid="stSidebar"] button::before {
            content: '';
            display: inline-block;
            width: 1.25rem;
            height: 1.25rem;
            margin-right: 0.75rem;
            border-radius: 0.25rem;
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0;
            flex-shrink: 0;
        }
        
        /* Active icon box - yellow */
        [data-testid="stSidebar"] button[kind="primary"]::before {
            background-color: #FFD700 !important;
            border: none !important;
        }
        
        /* Sign Up button with rocket emoji */
        [data-testid="stSidebar"] button[key="signup_btn"]::before {
            content: '🚀' !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 0.85rem !important;
        }
        
        [data-testid="stSidebar"] button[key="signup_btn"][kind="primary"]::before {
            background-color: #FFD700 !important;
        }
        
        /* Section headers */
        .section-header {
            font-size: 0.75rem;
            font-weight: bold;
            color: #000000;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 0.5rem 1rem;
            margin-top: 0.5rem;
        }
        
        /* Help panel */
        .help-panel {
            background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
            border-radius: 0.5rem;
            padding: 1.25rem;
            margin: 1rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .help-icon {
            width: 2.5rem;
            height: 2.5rem;
            background-color: #FFFFFF;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 0.75rem;
            font-size: 1.25rem;
            color: #FFD700;
            font-weight: bold;
        }
        
        .help-title {
            color: #FFFFFF;
            font-weight: bold;
            font-size: 1rem;
            margin-bottom: 0.25rem;
        }
        
        .help-text {
            color: #FFFFFF;
            font-size: 0.85rem;
            opacity: 0.95;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Branding area
        st.markdown("""
        <div class="whirlpool-brand">
            <div class="whirlpool-logo">Whirlpool</div>
            <div class="whirlpool-corp">CORPORATION</div>
        </div>
        <hr class="sidebar-divider">
        """, unsafe_allow_html=True)
        
        # Main Navigation - Dashboard (active by default)
        dashboard_active = st.session_state.page == "dashboard"
        if st.button("Dashboard", key="dashboard_btn", width='stretch', 
                     type="primary" if dashboard_active else "secondary"):
            st.session_state.page = "dashboard"
            st.rerun()
        
        # Main Navigation - Tables
        tables_active = st.session_state.page == "tables"
        if st.button("Tables", key="tables_btn", width='stretch',
                     type="primary" if tables_active else "secondary"):
            st.session_state.page = "tables"
            st.rerun()
        
        st.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)
        
        # ACCOUNT PAGES section
        st.markdown('<div class="section-header">ACCOUNT PAGES</div>', unsafe_allow_html=True)
        
        # Profile - with toggle
        profile_active = st.session_state.account_page == "profile"
        if st.button("Profile", key="profile_btn", width='stretch',
                     type="primary" if profile_active else "secondary"):
            # Toggle: if already active, deactivate; otherwise activate
            st.session_state.account_page = None if profile_active else "profile"
            st.rerun()
        
        # Sign In - with toggle
        signin_active = st.session_state.account_page == "signin"
        if st.button("Sign In", key="signin_btn", width='stretch',
                     type="primary" if signin_active else "secondary"):
            # Toggle: if already active, deactivate; otherwise activate
            st.session_state.account_page = None if signin_active else "signin"
            st.rerun()
        
        # Sign Up - with toggle (rocket icon when active)
        signup_active = st.session_state.account_page == "signup"
        if st.button("Sign Up", key="signup_btn", width='stretch',
                     type="primary" if signup_active else "secondary"):
            # Toggle: if already active, deactivate; otherwise activate
            st.session_state.account_page = None if signup_active else "signup"
            st.rerun()
        
        # Help panel at bottom
        st.markdown("""
        <div class="help-panel">
            <div class="help-icon">?</div>
            <div class="help-title">Need help?</div>
            <div class="help-text">Please check our docs</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Toggle button is handled in app.py - no duplicate buttons here
