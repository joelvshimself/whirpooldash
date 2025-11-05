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
    
    st.markdown("### Price Calculator")
    
    # History dropdown
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("History"):
            st.session_state.show_history = not st.session_state.show_history
    
    # Display history if requested
    if st.session_state.get('show_history', False):
        st.markdown("#### History")
        history = api_client.get_history(limit=10)
        if history:
            for record in history:
                st.markdown(f"**{record['sku']}** - {record['region']} - {record['partner']} - ${record['price']:.2f}")
        else:
            st.info("No history available")
        st.markdown("---")
    
    # Input form
    st.markdown("Choose your entries")
    
    partner = st.selectbox(
        "Partner",
        options=config.DEFAULT_PARTNERS,
        index=0  # Walmart as default
    )
    
    sku = st.selectbox(
        "SKU",
        options=config.DEFAULT_SKUS
    )
    
    region = st.selectbox(
        "Region",
        options=config.DEFAULT_REGIONS
    )
    
    time_range = st.selectbox(
        "Time Range",
        options=config.TIME_RANGE_OPTIONS
    )
    
    # Optimize button
    if st.button("Optimize", type="primary", use_container_width=True):
        with st.spinner("Calculating price..."):
            try:
                result = api_client.calculate_price(sku, region, time_range, partner)
                
                # Store result in session state
                st.session_state.last_prediction = result
                
                # Display result
                st.success("Price calculated successfully!")
                
                # Results table
                st.markdown("#### Results")
                results_data = {
                    "SKU": [result['sku']],
                    "Region": [result['region']],
                    "Partner": [result['partner']],
                    "Release date": [result.get('release_date', datetime.now().isoformat())],
                    "Price": [f"${result['price']:.2f}"]
                }
                st.dataframe(results_data, use_container_width=True, hide_index=True)
                
            except Exception as e:
                st.error(f"Error calculating price: {str(e)}")
    
    # Display last prediction if available
    if 'last_prediction' in st.session_state:
        st.markdown("---")
        st.markdown("#### Last Prediction")
        result = st.session_state.last_prediction
        st.json(result)

