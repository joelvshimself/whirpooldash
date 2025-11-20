"""
Dashboard component with KPIs, charts, and metrics
"""
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from services.data_service import DataService
from utils.helpers import format_currency, format_number, format_percentage

data_service = DataService()


def _get_icon_svg(name: str) -> str:
    """Return a small monochrome SVG for the chip icon."""
    if name == "money":
        # Minimal bill icon
        return """
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="3" y="6" width="18" height="12" rx="2" stroke="white" stroke-width="2"/>
            <circle cx="12" cy="12" r="3" stroke="white" stroke-width="2"/>
            <path d="M6 9h0M18 15h0" stroke="white" stroke-width="2" stroke-linecap="round"/>
        </svg>
        """
    if name == "users":
        # Minimal user avatar
        return """
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="8" r="3.5" stroke="white" stroke-width="2"/>
            <path d="M5 19c1.8-3 5-4.5 7-4.5s5.2 1.5 7 4.5" stroke="white" stroke-width="2" stroke-linecap="round"/>
        </svg>
        """
    # Default: dot
    return """
    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="12" r="6" fill="white"/>
    </svg>
    """


def render_kpi_chip(label: str, value_text: str, delta_value: float, delta_text: str, icon_name: str = "users", accent_color: str = "#E5B31A") -> None:
    """Render a single KPI as a chip-style card"""
    # Inject CSS once per call site (cheap, idempotent)
    st.markdown("""
    <style>
    .kpi-chip {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 18px 22px;
        border-radius: 16px;
        background: #FFFFFF;
        border: 1px solid #EEEEEE;
        box-shadow: 0 6px 24px rgba(0,0,0,0.06);
        width: 100%;
        box-sizing: border-box;
    }
    .kpi-left { display: flex; flex-direction: column; gap: 6px; }
    .kpi-label { color: #9CA3AF; font-weight: 700; font-size: 0.95rem; }
    .kpi-main { display: flex; align-items: baseline; gap: 10px; }
    .kpi-value { color: #111827; font-size: 2rem; font-weight: 800; line-height: 1; }
    .kpi-delta { font-weight: 700; font-size: 1rem; }
    .kpi-delta.positive { color: #22C55E; }
    .kpi-delta.negative { color: #EF4444; }
    .kpi-icon {
        width: 64px; height: 64px;
        border-radius: 16px;
        display: flex; align-items: center; justify-content: center;
        color: #FFFFFF;
        flex-shrink: 0;
    }
    .kpi-icon svg { width: 28px; height: 28px; }
    </style>
    """, unsafe_allow_html=True)
    delta_class = "positive" if delta_value >= 0 else "negative"
    icon_svg = _get_icon_svg(icon_name)
    st.markdown(f"""
    <div class="kpi-chip">
        <div class="kpi-left">
            <div class="kpi-label">{label}</div>
            <div class="kpi-main">
                <span class="kpi-value">{value_text}</span>
                <span class="kpi-delta {delta_class}">{delta_text}</span>
            </div>
        </div>
        <div class="kpi-icon" style="background:{accent_color};">{icon_svg}</div>
    </div>
    """, unsafe_allow_html=True)


def render_kpi_cards():
    """Render KPI cards"""
    kpis = data_service.get_kpis()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_kpi_chip(
            label="Today's Money",
            value_text=format_currency(kpis["todays_money"]),
            delta_value=kpis["money_change"],
            delta_text=format_percentage(kpis["money_change"]),
            icon_name="money",
            accent_color="#E5B31A"
        )
    
    with col2:
        render_kpi_chip(
            label="Today's Users",
            value_text=format_number(kpis["todays_users"]),
            delta_value=kpis["users_change"],
            delta_text=format_percentage(kpis["users_change"]),
            icon_name="users",
            accent_color="#E5B31A"
        )
    
    with col3:
        render_kpi_chip(
            label="Today's Users",
            value_text=format_number(kpis["todays_users"]),
            delta_value=kpis["users_change"],
            delta_text=format_percentage(kpis["users_change"]),
            icon_name="users",
            accent_color="#E5B31A"
        )


def _render_sales_chart_only():
    """Render only the sales chart (without checkboxes)"""
    sales_data = data_service.get_sales_data()
    
    fig = go.Figure()
    
    # Define 5 distinct colors for the lines
    colors = [
        '#1f77b4',  # Dark blue - GE
        '#2ca02c',  # Medium green - LG
        '#17becf',  # Light blue/cyan - MABE
        '#ff7f0e',  # Orange - MAYTAG
        '#ffd700'   # Golden yellow - WHIRLPOOL
    ]
    
    # Add only selected series as lines (no fill)
    visible_count = 0
    for i, series in enumerate(sales_data["values"]):
        brand_name = series["name"]
        if st.session_state.selected_brands.get(brand_name, True):
            fig.add_trace(go.Scatter(
                x=sales_data["months"],
                y=series["data"],
                mode='lines',
                name=brand_name,
                line=dict(
                    color=colors[i],
                    width=2.5
                ),
                hovertemplate='<b>%{fullData.name}</b><br>Month: %{x}<br>Value: %{y}<extra></extra>'
            ))
            visible_count += 1
    
    # Only show chart if at least one brand is selected
    if visible_count > 0:
        fig.update_layout(
            title="Sales Overview",
            xaxis_title="Month",
            yaxis_title="Sales",
            hovermode='x unified',
            height=400,
            showlegend=True,
            plot_bgcolor='white',
            paper_bgcolor='white',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,0,0.1)',
                gridwidth=1
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,0,0.1)',
                gridwidth=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Please select at least one brand to display.")


def render_sales_chart():
    """Render sales overview chart with 5 brand lines and dynamic selection"""
    sales_data = data_service.get_sales_data()
    
    # Initialize session state for brand selection
    if 'selected_brands' not in st.session_state:
        st.session_state.selected_brands = {brand["name"]: True for brand in sales_data["values"]}
    
    # Brand selection checkboxes
    st.markdown("**Select Brands to Display:**")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    brand_names = [brand["name"] for brand in sales_data["values"]]
    cols = [col1, col2, col3, col4, col5]
    
    for i, brand_name in enumerate(brand_names):
        with cols[i]:
            st.session_state.selected_brands[brand_name] = st.checkbox(
                brand_name,
                value=st.session_state.selected_brands.get(brand_name, True),
                key=f"brand_{brand_name}"
            )
    
    st.markdown("---")
    
    # Render chart
    _render_sales_chart_only()


def render_brand_category_table():
    """Render brand vs category price comparison table with gradient colors"""
    import pandas as pd
    
    price_data = data_service.get_brand_category_prices()
    
    # Create a pivot table: brands as rows, categories as columns
    df_data = []
    for item in price_data["data"]:
        df_data.append({
            "Brand": item["brand"],
            item["category"]: item["price"]
        })
    
    # Create DataFrame
    df = pd.DataFrame(df_data)
    
    # Group by brand and take the first value (since we have one row per brand-category combination)
    # Actually, we need to pivot properly
    pivot_data = {}
    for item in price_data["data"]:
        brand = item["brand"]
        category = item["category"]
        price = item["price"]
        
        if brand not in pivot_data:
            pivot_data[brand] = {}
        pivot_data[brand][category] = price
    
    # Create DataFrame from pivot data
    df = pd.DataFrame.from_dict(pivot_data, orient='index')
    df.index.name = "Brand"
    df = df.reset_index()
    
    # Reorder columns: Brand first, then categories
    column_order = ["Brand"] + price_data["categories"]
    df = df[column_order]
    
    # Calculate min and max for gradient (before formatting)
    numeric_cols = [col for col in price_data["categories"] if col in df.columns]
    all_values = []
    for col in numeric_cols:
        for v in df[col]:
            if v is not None and pd.notna(v):
                try:
                    all_values.append(float(v))
                except:
                    pass
    
    min_val = min(all_values) if all_values else 0
    max_val = max(all_values) if all_values else 1
    
    # Create styled dataframe with gradient
    def style_gradient(val):
        """Apply gradient color based on value"""
        if val is None or pd.isna(val):
            return 'background-color: white'
        
        try:
            num_val = float(val)
        except:
            return 'background-color: white'
        
        if min_val == max_val:
            return 'background-color: #fff9c4'
        
        # Normalize value between 0 and 1
        normalized = (num_val - min_val) / (max_val - min_val)
        
        # Create gradient from light yellow to golden yellow
        # Light yellow: #fff9c4, Golden yellow: #ffd700
        r1, g1, b1 = 255, 249, 196  # Light yellow
        r2, g2, b2 = 255, 215, 0    # Golden yellow
        
        r = int(r1 + (r2 - r1) * normalized)
        g = int(g1 + (g2 - g1) * normalized)
        b = int(b1 + (b2 - b1) * normalized)
        
        return f'background-color: rgb({r}, {g}, {b})'
    
    # Apply styling to category columns
    styled_df = df.style.applymap(style_gradient, subset=numeric_cols)
    
    # Format prices for display using format()
    def format_price(x):
        if x is not None and pd.notna(x):
            return f"{x:,.0f}"
        return ""
    
    format_dict = {col: format_price for col in numeric_cols}
    styled_df = styled_df.format(format_dict)
    
    st.markdown("### Brand vs Category Price Comparison")
    st.dataframe(styled_df, use_container_width=True, hide_index=True)


def render_dashboard():
    """Render the main dashboard (Performance)"""
    st.title("Dashboard Performance")
    
    # Initialize session state for year and quarter selection
    if 'selected_year' not in st.session_state:
        st.session_state.selected_year = None
    if 'selected_quarter' not in st.session_state:
        st.session_state.selected_quarter = None
    
    # Year and Quarter selectors at the top
    col_year, col_quarter = st.columns(2)
    
    with col_year:
        current_year = datetime.now().year
        available_years = list(range(current_year - 5, current_year + 1))
        available_years.reverse()  # Most recent first
        
        selected_year = st.selectbox(
            "Select Year",
            options=[None] + available_years,
            format_func=lambda x: "All Years" if x is None else str(x),
            index=0 if st.session_state.selected_year is None else available_years.index(st.session_state.selected_year) + 1 if st.session_state.selected_year in available_years else 0,
            key="year_selector"
        )
        st.session_state.selected_year = selected_year
    
    with col_quarter:
        if st.session_state.selected_year is not None:
            quarter_options = [None, 1, 2, 3, 4]
            if st.session_state.selected_quarter is None:
                quarter_index = 0
            else:
                quarter_index = quarter_options.index(st.session_state.selected_quarter) if st.session_state.selected_quarter in quarter_options else 0
            
            selected_quarter = st.selectbox(
                "Select Quarter",
                options=quarter_options,
                format_func=lambda x: "All Quarters" if x is None else f"Q{x}",
                index=quarter_index,
                key="quarter_selector"
            )
            st.session_state.selected_quarter = selected_quarter
        else:
            st.selectbox(
                "Select Quarter",
                options=[None],
                format_func=lambda x: "Select Year First",
                disabled=True,
                key="quarter_selector_disabled"
            )
            st.session_state.selected_quarter = None
    
    st.markdown("---")
    
    # Get sales data with year and quarter filters
    sales_data = data_service.get_sales_data(
        year=st.session_state.selected_year,
        quarter=st.session_state.selected_quarter
    )
    
    # Initialize session state for brand selection (needed to count selected brands)
    if 'selected_brands' not in st.session_state:
        st.session_state.selected_brands = {brand["name"]: True for brand in sales_data["values"]}
    
    # Layout: checkboxes on left, chart on right
    checkbox_col, chart_col = st.columns([1, 4])
    
    brand_names = [brand["name"] for brand in sales_data["values"]]
    
    with checkbox_col:
        st.markdown("**Select Brands to Display:**")
        st.markdown("")  # Add some spacing
        for brand_name in brand_names:
            st.session_state.selected_brands[brand_name] = st.checkbox(
                brand_name,
                value=st.session_state.selected_brands.get(brand_name, True),
                key=f"brand_{brand_name}"
            )
    
    # Count how many brands are selected (after checkboxes update the state)
    selected_count = sum(1 for selected in st.session_state.selected_brands.values() if selected)
    
    # Only show KPIs when exactly 2 brands are selected
    if selected_count == 2:
        # KPIs
        st.markdown("---")
        render_kpi_cards()
        
    
    with chart_col:
        # Sales chart (without checkboxes, as they're already rendered in the left column)
        _render_sales_chart_only()
    
    st.markdown("---")
    
    # Brand vs Category price comparison table
    render_brand_category_table()


def render_prediction_chart():
    """Render prediction chart with historical data, prediction line, and confidence interval"""
    prediction_data = data_service.get_prediction_data()
    
    fig = go.Figure()
    
    # Whirlpool color - golden yellow
    color = '#ffd700'
    
    all_months = prediction_data["months"]
    historical_months = prediction_data["historical_months"]
    prediction_months = prediction_data["prediction_months"]
    
    # Find the index where prediction starts
    prediction_start_idx = len(historical_months)
    
    # Only use Whirlpool brand
    brand_name = "WHIRLPOOL"
    
    if brand_name not in prediction_data["historical"]:
        st.warning(f"Brand {brand_name} not found in prediction data.")
        return
    
    # Historical data
    hist_values = prediction_data["historical"][brand_name]
    hist_months = historical_months
    
    # Prediction data
    pred_values = prediction_data["prediction"][brand_name]
    upper_values = prediction_data["upper_bound"][brand_name]
    lower_values = prediction_data["lower_bound"][brand_name]
    
    # Add historical line (solid)
    fig.add_trace(go.Scatter(
        x=hist_months,
        y=hist_values,
        mode='lines',
        name=f"{brand_name} (Historical)",
        line=dict(
            color=color,
            width=2.5
        ),
        showlegend=False,
        hovertemplate='<b>%{fullData.name}</b><br>Month: %{x}<br>Value: %{y}<extra></extra>'
    ))
    
    # Add prediction line (dashed) - only the prediction part
    fig.add_trace(go.Scatter(
        x=prediction_months,
        y=pred_values,
        mode='lines',
        name=f"{brand_name} (Prediction)",
        line=dict(
            color=color,
            width=2.5,
            dash='dash'
        ),
        hovertemplate='<b>%{fullData.name}</b><br>Month: %{x}<br>Predicted: %{y}<extra></extra>'
    ))
    
    # Add connection line between historical and prediction (thin, same color)
    if hist_values and pred_values:
        fig.add_trace(go.Scatter(
            x=[hist_months[-1], prediction_months[0]],
            y=[hist_values[-1], pred_values[0]],
            mode='lines',
            line=dict(
                color=color,
                width=1,
                dash='dot'
            ),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Create gradient effect for confidence interval
    # Use multiple layers with decreasing opacity to create smooth gradient
    confidence_x = prediction_months
    confidence_upper = upper_values
    confidence_lower = lower_values
    
    # Number of gradient layers (more layers = smoother gradient)
    num_layers = 15
    
    # Create gradient by adding multiple overlapping traces with decreasing opacity
    # Draw from outer to inner so inner layers (drawn last) appear darker
    for layer in range(num_layers - 1, -1, -1):  # Reverse order: outer to inner
        # Calculate how far this layer extends (0 = prediction line, 1 = confidence bounds)
        factor = (layer + 1) / num_layers
        
        # Calculate the boundaries for this layer (from center to factor distance)
        layer_upper = [pred + (upper - pred) * factor for pred, upper in zip(pred_values, confidence_upper)]
        layer_lower = [pred - (pred - lower) * factor for pred, lower in zip(pred_values, confidence_lower)]
        
        # Opacity increases toward center for gradient effect
        # Higher opacity near center (smaller factor), lower at edges (larger factor)
        # Use exponential decay for smooth gradient
        opacity = 0.5 * (1 - factor) ** 2.2  # Smooth gradient from center to edge
        
        if opacity > 0.01:  # Only add layers with visible opacity
            # Create filled area from center to this layer's boundary
            fig.add_trace(go.Scatter(
                x=confidence_x + confidence_x[::-1],
                y=layer_upper + layer_lower[::-1],
                fill='toself',
                fillcolor=f'rgba(255, 215, 0, {opacity:.3f})',  # Golden yellow with gradient opacity
                line=dict(color='rgba(255,255,255,0)'),
                name=f"{brand_name} (Confidence Interval)",
                showlegend=False,
                hoverinfo='skip'
            ))
    
    fig.update_layout(
        title="Sales Prediction with Confidence Interval",
        xaxis_title="Month",
        yaxis_title="Sales",
        hovermode='x unified',
        height=400,
        showlegend=True,
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            gridwidth=1
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            gridwidth=1
        ),
        shapes=[
            # Vertical line to separate historical from prediction
            dict(
                type="line",
                xref="x",
                yref="paper",
                x0=historical_months[-1],
                y0=0,
                x1=historical_months[-1],
                y1=1,
                line=dict(
                    color="gray",
                    width=2,
                    dash="dot"
                )
            )
        ],
        annotations=[
            dict(
                x=historical_months[-1],
                y=0.95,
                xref="x",
                yref="paper",
                text="Historical → Prediction",
                showarrow=False,
                xanchor="right",
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="gray",
                borderwidth=1
            )
        ]
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_prediction_dashboard():
    """Render the prediction dashboard (based on the same structure)"""
    st.title("Prediction")
    
    # Prediction chart with historical data, prediction line, and confidence interval
    render_prediction_chart()
    
    st.markdown("---")
    
    # Brand vs Category price comparison table
    render_brand_category_table()

