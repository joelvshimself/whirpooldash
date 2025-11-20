"""
Dashboard component with KPIs, charts, and metrics
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
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
    </div>
    """, unsafe_allow_html=True)


def render_kpi_cards():
    """Render KPI cards"""
    kpis = data_service.get_kpis()
    col1, col2, col3, col4 = st.columns(4, gap="small")
    
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
    
    with col4:
        render_kpi_chip(
            label="Today's Users",
            value_text=format_number(kpis["todays_users"]),
            delta_value=kpis["users_change"],
            delta_text=format_percentage(kpis["users_change"]),
            icon_name="users",
            accent_color="#E5B31A"
        )


def _render_sales_chart_only():
    """Render sales chart for Latin American retailers"""
    # Months for the last 12 months
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Retailers with chaotic/inconsistent sales data
    # Coppel (orange) always has the highest values to stand out
    retailers_data = {
        "Coppel": [180, 165, 195, 175, 188, 205, 192, 178, 210, 195, 202, 215],  # Highest, chaotic
        "Elektra": [120, 98, 135, 112, 125, 142, 118, 105, 148, 132, 140, 155],  # More chaotic
        "Bodega Aurrera": [85, 102, 78, 95, 108, 82, 115, 90, 105, 118, 92, 110],  # More chaotic
        "Walmart": [100, 115, 95, 110, 125, 108, 118, 105, 128, 120, 115, 130]  # More chaotic
    }
    
    fig = go.Figure()
    
    # Highlight color for Coppel (orange/yellow)
    highlight_color = '#FF6B35'  # Orange
    gray_color = '#9CA3AF'  # Gray for other retailers
    
    # Add all retailers as lines with markers
    for retailer_name, sales_values in retailers_data.items():
        # Use highlight color for Coppel, gray for others
        is_highlighted = retailer_name == "Coppel"
        line_color = highlight_color if is_highlighted else gray_color
        line_width = 7 if is_highlighted else 5
        
        fig.add_trace(go.Scatter(
            x=months,
            y=sales_values,
            mode='lines+markers',
            name=retailer_name,
            line=dict(
                color=line_color,
                width=line_width
            ),
            marker=dict(
                symbol='circle',
                size=13,  # Double the size (was 10, now 20)
                color=line_color,
                line=dict(
                    color='white',
                    width=2
                )
            ),
            hovertemplate='<b>%{fullData.name}</b><br>Month: %{x}<br>Sales: %{y}<extra></extra>'
        ))
    
    fig.update_layout(
        title="Sales Overview",
        xaxis_title="Month",
        yaxis_title="Sales",
        hovermode='x unified',
        height=550,
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


def _render_brand_bar_chart():
    """Render a stacked bar chart by categories with appliance types"""
    # Categories
    categories = ["fridges", "ranges", "range hood", "washing machine", "dryers"]
    
    # Appliance types: Fridges, Ranges, Washing Machines, Dryers
    # Invented data: [fridges, ranges, washing_machines, dryers]
    sales_data = {
        "fridges": [4.0, 3.5, 2.5, 1.8],      # Total: 11.8
        "ranges": [5.0, 4.2, 3.8, 2.5],      # Total: 15.5
        "range hood": [4.5, 3.8, 2.8, 2.0],      # Total: 13.1
        "washing machine": [6.0, 5.2, 4.5, 3.2],      # Total: 18.9 (highest)
        "dryers": [3.5, 3.0, 2.2, 1.5]       # Total: 10.2
    }
    
    # Calculate totals to find the highest
    totals = {cat: sum(sales_data[cat]) for cat in categories}
    max_category = max(totals, key=totals.get)
    
    # Colors
    highlight_color = '#FF6B35'  # Orange for highlighted category
    highlight_colors = ['#FF6B35', '#FF8C5A', '#FFA07A', '#FFB88C']  # Orange shades
    gray_colors = ['#9CA3AF', '#B0B8C4', '#C4CBD6', '#D8DEE3']  # Gray shades
    
    # Create figure with go.Figure for better control
    fig = go.Figure()
    
    # Segment names (4 segments per category)
    segment_names = ["Segment 1", "Segment 2", "Segment 3", "Segment 4"]
    
    # Add each segment as a stacked bar
    for i, segment_name in enumerate(segment_names):
        values = [sales_data[cat][i] for cat in categories]
        colors = [highlight_colors[i] if cat == max_category else gray_colors[i] for cat in categories]
        
        fig.add_trace(go.Bar(
            name=segment_name,
            x=categories,
            y=values,
            marker_color=colors
        ))
    
    # Set barmode to stack
    fig.update_layout(barmode='stack')
    
    # Update layout
    fig.update_layout(
        title="Total Sales by Category",
        xaxis_title="Category",
        yaxis_title="Sales",
        height=550,
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,  # Hide legend/segment buttons
        xaxis=dict(
            showgrid=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            gridwidth=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)


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
    st.title("Sellout")
    st.header("Home Appliances- Training Partner Offer")
    
    render_kpi_cards()
    
    # Layout: line chart (70%) and bar chart (30%)
    chart_col, bar_col = st.columns([0.7, 0.3])
    
    with chart_col:
        _render_sales_chart_only()
    
    with bar_col:
        _render_brand_bar_chart()
    
    
    


def render_prediction_chart():
    """Render prediction chart with multiple lines, one highlighted in yellow"""
    # Invented data for multiple prediction lines
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Forecasting starts at index 9 (October)
    forecast_start_idx = 9
    historical_months = months[:forecast_start_idx]
    prediction_months = months[forecast_start_idx:]
    
    # Multiple prediction models/lines with invented data
    predictions = {
        "Model A": {
            "historical": [120, 125, 130, 128, 135, 140, 138, 142, 145],
            "prediction": [148, 150, 152],
            "color": "#FFD700",  # Yellow - highlighted
            "highlighted": True
        },
        "Model B": {
            "historical": [110, 115, 120, 118, 125, 130, 128, 132, 135],
            "prediction": [138, 140, 142],
            "color": "#9CA3AF",  # Gray
            "highlighted": False
        },
        "Model C": {
            "historical": [100, 105, 110, 108, 115, 120, 118, 122, 125],
            "prediction": [128, 130, 132],
            "color": "#9CA3AF",  # Gray
            "highlighted": False
        },
        "Model D": {
            "historical": [115, 120, 125, 123, 130, 135, 133, 137, 140],
            "prediction": [143, 145, 147],
            "color": "#9CA3AF",  # Gray
            "highlighted": False
        }
    }
    
    fig = go.Figure()
    
    # Add lines for each model
    for model_name, model_data in predictions.items():
        hist_values = model_data["historical"]
        pred_values = model_data["prediction"]
        line_color = model_data["color"]
        is_highlighted = model_data["highlighted"]
        line_width = 7 if is_highlighted else 5
        
        # Combine historical and prediction for full line
        all_values = hist_values + pred_values
        all_months = historical_months + prediction_months
        
        # Add historical part (solid line)
        fig.add_trace(go.Scatter(
            x=historical_months,
            y=hist_values,
            mode='lines',
            name=model_name,
            line=dict(
                color=line_color,
                width=line_width
            ),
            hovertemplate='<b>%{fullData.name}</b><br>Month: %{x}<br>Value: %{y}<extra></extra>'
        ))
        
        # Add prediction part (dotted line)
        fig.add_trace(go.Scatter(
            x=prediction_months,
            y=pred_values,
            mode='lines',
            name=f"{model_name} (Forecast)",
            line=dict(
                color=line_color,
                width=line_width,
                dash='dot'
            ),
            showlegend=False,
            hovertemplate='<b>%{fullData.name}</b><br>Month: %{x}<br>Predicted: %{y}<extra></extra>'
        ))
        
        # Add connection line between historical and prediction
        if hist_values and pred_values:
            fig.add_trace(go.Scatter(
                x=[historical_months[-1], prediction_months[0]],
                y=[hist_values[-1], pred_values[0]],
                mode='lines',
                line=dict(
                    color=line_color,
                    width=line_width,
                    dash='dot'
                ),
                showlegend=False,
                hoverinfo='skip'
            ))
    
    # Update layout
    forecast_start_month = historical_months[-1]
    
    fig.update_layout(
        title="Sales Prediction with Confidence Interval",
        xaxis_title="Month",
        yaxis_title="Sales",
        hovermode='x unified',
        height=550,  # Same height as Sellout chart
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
            # Vertical line to mark the start of forecasting
            dict(
                type="line",
                xref="x",
                yref="paper",
                x0=forecast_start_month,
                y0=0,
                x1=forecast_start_month,
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
                x=forecast_start_month,
                y=0.95,
                xref="x",
                yref="paper",
                text="Forecasting",
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
    """Render the prediction dashboard with dropdowns and full-width chart"""
    st.title("Prediction")
    
    # Three dropdown buttons in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        dropdown1 = st.selectbox(
            "Select Option 1",
            options=["Option A", "Option B", "Option C"],
            key="prediction_dropdown_1"
        )
    
    with col2:
        dropdown2 = st.selectbox(
            "Select Option 2",
            options=["Option X", "Option Y", "Option Z"],
            key="prediction_dropdown_2"
        )
    
    with col3:
        dropdown3 = st.selectbox(
            "Select Option 3",
            options=["Option 1", "Option 2", "Option 3"],
            key="prediction_dropdown_3"
        )
    
    
    # Prediction chart with historical data, prediction line, and confidence interval
    # Full width chart
    render_prediction_chart()
    

    
    # Model Evaluation component
    render_model_evaluation()


def render_model_evaluation():
    """Render model evaluation metrics as a simple two-column table with colors"""
    st.markdown("### Model Evaluation")
    
    # Invented evaluation metrics data - simple name and value pairs
    metrics_data = [
        {"Metric": "R²", "Value": 0.94},
        {"Metric": "MAE", "Value": 10.3},
        {"Metric": "RMSE", "Value": 15.6},
        {"Metric": "F1", "Value": 0.91}
    ]
    
    df = pd.DataFrame(metrics_data)
    
    # Store original values for color calculation
    original_values = df["Value"].copy()
    
    # Format values for display
    for idx, row in df.iterrows():
        if row["Metric"] in ["R²", "F1"]:
            df.at[idx, "Value"] = f"{row['Value']:.3f}"
        else:
            df.at[idx, "Value"] = f"{row['Value']:.2f}"
    
    # Apply styling to Value column
    def style_row(row):
        """Style the Value cell in each row"""
        idx = row.name
        metric_name = metrics_data[idx]["Metric"]
        original_val = original_values.iloc[idx]
        
        if metric_name in ["R²", "F1"]:
            # Higher is better - green gradient (already 0-1 scale)
            normalized = original_val
        elif metric_name == "MAE":
            # Lower is better - normalize and invert (10.3 is best, assume max is ~25)
            normalized = max(0, min(1, 1 - (original_val / 25)))
        elif metric_name == "RMSE":
            # Lower is better - normalize and invert (15.6 is best, assume max is ~30)
            normalized = max(0, min(1, 1 - (original_val / 30)))
        else:
            return ['', '']
        
        r = int(144 + (34 - 144) * normalized)
        g = int(238 + (139 - 238) * normalized)
        b = int(144 + (34 - 144) * normalized)
        color = "white" if normalized > 0.7 else "black"
        
        return ['', f'background-color: rgb({r}, {g}, {b}); color: {color}']
    
    styled_df = df.style.apply(style_row, axis=1)
    
    st.dataframe(styled_df, use_container_width=True, height=200, hide_index=True)
