"""
SKU table component
"""
import streamlit as st
from services.data_service import DataService
from utils.helpers import format_currency

data_service = DataService()


def render_sku_table():
    """Render the SKU table"""
    st.markdown("### SKU's top 10 this month")
    
    sku_data = data_service.get_sku_table()
    
    # Create table display
    for sku in sku_data:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
            
            with col1:
                st.markdown(f"{sku['icon']} **{sku['company']}**")
            
            with col2:
                # Display member avatars (simplified)
                members_display = "👤" * sku['members']
                st.markdown(f"**MEMBERS** {members_display}")
            
            with col3:
                budget = sku['budget'] if sku['budget'] != "Not set" else "Not set"
                if budget != "Not set":
                    st.markdown(f"**BUDGET** {format_currency(budget)}")
                else:
                    st.markdown(f"**BUDGET** {budget}")
            
            with col4:
                st.markdown(f"**COMPLETION** {sku['completion']}%")
                st.progress(sku['completion'] / 100)
            
            st.markdown("---")

