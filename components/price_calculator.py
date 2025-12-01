"""
Price Calculator component
"""
import streamlit as st
from services.api_client import PriceCalculatorAPI
from services.data_service import DataService
import config
from datetime import datetime

api_client = PriceCalculatorAPI()
data_service = DataService()


def render_price_calculator():
    """Render the price calculator panel"""
    # Initialize session state
    if 'show_history' not in st.session_state:
        st.session_state.show_history = False
    if 'price_calc_data' not in st.session_state:
        st.session_state.price_calc_data = []
    
    
    # Title
    st.markdown("### Price Calculator")
    st.caption("Using partner-specific ML models from Azure")
    
    # History (expander for a cleaner layout)
    with st.expander("History", expanded=False):
        try:
            history = api_client.get_history(limit=10)
            if history and len(history) > 0:
                for record in history:
                    st.markdown(f"**{record['sku']}** - {record['region']} - {record['partner']} - ${record['price']:.2f}")
            else:
                st.info("No history available")
        except Exception as e:
            st.info("No history available")
    
    # Inputs in a clean 2x2 grid
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            sku = st.selectbox(
                "SKU",
                options=config.DEFAULT_SKUS,
                key="pc_sku",
                help="Select a SKU from the validated list"
            )
            region = st.selectbox(
                "Region",
                options=config.DEFAULT_REGIONS,
                key="pc_region"
            )
        with col2:
            time_range = st.selectbox(
                "Time Range",
                options=config.TIME_RANGE_OPTIONS,
                key="pc_time_range"
            )
            partner = st.selectbox(
                "Training Partner",
                options=config.DEFAULT_PARTNERS,
                index=0,
                key="pc_partner",
                help="Select the partner whose trained model to use for prediction"
            )
        
        # Optimize action aligned to the right
        col_space, col_opt = st.columns([3, 1])
        with col_opt:
            if st.button("Optimize", key="pc_optimize", width='stretch'):
                with st.spinner("Calculating price..."):
                    try:
                        result = api_client.calculate_price(sku, region, time_range, partner)
                        st.session_state.last_prediction = result
                        
                        release_date = result.get('release_date', datetime.now().strftime('%Y-%m-%d'))
                        st.session_state.price_calc_data = [{
                            "SKU": result['sku'],
                            "Region": result['region'],
                            "Partner": result['partner'],
                            "Release date": release_date,
                            "Price": f"${result['price']:.2f}"
                        }]
                        
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error calculating price: {str(e)}")
