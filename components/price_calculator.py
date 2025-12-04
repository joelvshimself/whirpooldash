"""
Price Calculator component
"""
import streamlit as st
from services.api_client import PriceCalculatorAPI
from services.data_service import DataService
import config
from datetime import datetime
from typing import Any, Dict, Optional

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
            partner_options = config.get_training_partners() or config.DEFAULT_PARTNERS
            if not partner_options:
                st.warning("No training partners available.")
                partner_options = ["—"]
            partner = st.selectbox(
                "Training Partner",
                options=partner_options,
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

    _render_price_statement()


def _render_price_statement():
    """Render the latest price statement (if any) using a white card theme."""
    result: Optional[Dict[str, Any]] = st.session_state.get("last_prediction")
    if not result:
        st.info("Run the optimizer to see the recommended price.")
        return

    price = result.get("price")
    price_text = f"${price:,.2f}" if isinstance(price, (int, float)) else "—"
    partner = result.get("partner", "—")
    sku = result.get("sku", "—")
    region = result.get("region", "—")
    release_raw = result.get("release_date") or result.get("prediction_date")
    release_date = release_raw.split("T")[0] if isinstance(release_raw, str) else str(release_raw)
    confidence = result.get("confidence")
    confidence_text = f"{confidence*100:.1f}%" if isinstance(confidence, (int, float)) else "—"

    st.markdown(
        """
        <style>
        .price-result-card {
            background: #FFFFFF;
            border-radius: 20px;
            padding: 32px;
            border: 1px solid #E5E7EB;
            box-shadow: 0 12px 24px rgba(15, 23, 42, 0.08);
            margin-top: 1.5rem;
        }
        .price-result-card h4 {
            margin: 0;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.18em;
            color: #6B7280;
        }
        .price-result-card .value {
            font-size: clamp(42px, 5vw, 64px);
            font-weight: 800;
            margin: 18px 0 6px 0;
            color: #111827;
        }
        .price-result-card .meta-row {
            display: flex;
            gap: 1.5rem;
            flex-wrap: wrap;
            margin-top: 18px;
        }
        .price-result-card .meta {
            font-size: 0.95rem;
            color: #4B5563;
        }
        .price-result-card .meta span {
            display: block;
            font-weight: 600;
            color: #111827;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="price-result-card">
            <h4>{partner} · {sku} · {region}</h4>
            <div class="value">{price_text}</div>
            <div class="meta-row">
                <div class="meta">Release Date<span>{release_date}</span></div>
                <div class="meta">Confidence<span>{confidence_text}</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
