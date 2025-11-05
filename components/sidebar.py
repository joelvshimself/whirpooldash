"""
Sidebar navigation component
"""
import streamlit as st


def render_sidebar():
    """Render the left sidebar with navigation"""
    with st.sidebar:
        # Logo and branding
        st.markdown("### 🌀 Whirlpool")
        st.markdown("**Internal WHP Dashboard**")
        st.markdown("---")
        
        # Home Page section
        st.markdown("### Home Page")
        if st.button("📊 Dashboard", use_container_width=True, type="primary"):
            st.session_state.page = "dashboard"
        
        st.markdown("---")
        
        # Navigation section
        st.markdown("### Dashboard modules")
        if st.button("📊 Dashboard", use_container_width=True, key="nav_dashboard"):
            st.session_state.page = "dashboard"
        
        if st.button("📋 Tables", use_container_width=True):
            st.session_state.page = "tables"
        
        st.markdown("---")
        
        # Account pages
        st.markdown("### ACCOUNT PAGES")
        st.button("👤 Profile", use_container_width=True)
        st.button("🔐 Sign In", use_container_width=True)
        st.button("📝 Sign Up", use_container_width=True)
        
        st.markdown("---")
        
        # Help section
        st.markdown("### Need help?")
        st.markdown("❓ Please check our docs")

