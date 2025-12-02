"""
Dashboard component with KPIs, charts, and metrics
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import config
from services.run_model import predict_price_scenario_xgb_from_pickle
from services.data_service import DataService
from services.sellout_kpis import get_sellout_kpis
from utils.helpers import format_currency, format_currency_millions, format_number, format_percentage

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


def render_kpi_chip(label: str, value_text: str, delta_value: float, delta_text: str, icon_name: str = "users", accent_color: str = "#E5B31A", layout: str = "standard", large_delta: bool = False) -> None:
    """
    Render a single KPI as a chip-style card
    
    Args:
        label: Label text for the KPI
        value_text: Formatted value to display
        delta_value: Numeric delta value (for color determination)
        delta_text: Formatted delta text to display
        icon_name: Icon name (not currently used but kept for compatibility)
        accent_color: Accent color (not currently used but kept for compatibility)
        layout: "standard" for label above value, "horizontal" for value left, label right
        large_delta: If True, make delta text larger (for percentage display)
    """
    
    delta_class = "positive" if delta_value >= 0 else "negative"
    delta_size_class = "kpi-delta-large" if large_delta else ""
    
    if layout == "horizontal":
        # Horizontal layout: value on left (large), label on right
        st.markdown(f"""
        <div class="kpi-chip kpi-chip-horizontal">
            <div class="kpi-horizontal-content">
                <span class="kpi-value kpi-value-large">{value_text}</span>
                <div class="kpi-horizontal-right">
                    <div class="kpi-label kpi-label-horizontal">{label}</div>
                    <span class="kpi-delta {delta_class} {delta_size_class}">{delta_text}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Standard layout: label above, value and delta below
        # If large_delta is True, make the value_text (percentage) large and prominent
        if large_delta:
            st.markdown(f"""
            <div class="kpi-chip">
                <div class="kpi-left">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-main">
                        <span class="kpi-value kpi-value-large {delta_class}">{value_text}</span>
                        <span class="kpi-delta-small">{delta_text}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="kpi-chip">
                <div class="kpi-left">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-main">
                        <span class="kpi-value">{value_text}</span>
                        <span class="kpi-delta {delta_class} {delta_size_class}">{delta_text}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_kpi_cards():
    """Render KPI cards for Sellout dashboard"""
    try:
        kpis = get_sellout_kpis()
    except Exception as e:
        st.error(f"Error loading sellout KPIs: {e}")
        return
    
    col1, col2, col3, col4 = st.columns(4, gap="small")
    
    # KPI 1: Items sold this year
    with col1:
        articles_value = format_number(kpis["articles_this_year"])
        render_kpi_chip(
            label="Items Sold",
            value_text=articles_value,
            delta_value=0.0,
            delta_text=f"Year {kpis['current_year']}",
            icon_name="users",
            accent_color="#E5B31A",
            layout="standard"
        )
    
    # KPI 2: Total sales (items × price) - layout horizontal
    with col2:
        sales_value = format_currency_millions(kpis["sales_this_year"])
        render_kpi_chip(
            label="Total Sales",
            value_text=sales_value,
            delta_value=0.0,
            delta_text=f"Year {kpis['current_year']}",
            icon_name="money",
            accent_color="#E5B31A",
            layout="horizontal"
        )
    
    # KPI 3: Items delta vs previous year (large percentage only)
    with col3:
        articles_delta_pct = kpis["articles_delta_percentage"]
        delta_percentage_text = format_percentage(articles_delta_pct) if articles_delta_pct != 0.0 else "N/A"
        render_kpi_chip(
            label="Items Delta",
            value_text=delta_percentage_text,
            delta_value=articles_delta_pct,
            delta_text=f"vs {kpis['previous_year']}",
            icon_name="users",
            accent_color="#E5B31A",
            layout="standard",
            large_delta=True
        )
    
    # KPI 4: Sales delta vs previous year (large percentage only)
    with col4:
        sales_delta_pct = kpis["sales_delta_percentage"]
        delta_percentage_text = format_percentage(sales_delta_pct) if sales_delta_pct != 0.0 else "N/A"
        render_kpi_chip(
            label="Sales Delta",
            value_text=delta_percentage_text,
            delta_value=sales_delta_pct,
            delta_text=f"vs {kpis['previous_year']}",
            icon_name="money",
            accent_color="#E5B31A",
            layout="standard",
            large_delta=True
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
    
    
    


def render_prediction_chart(selected_sku: str, forecast_date_range, predictions_df: pd.DataFrame):
    """Render the prediction chart with time on x-axis and one line per Trading Partner with orange gradients."""
    if predictions_df is None or predictions_df.empty:
        st.info("No prediction data available to plot.")
        return
    
    chart_df = predictions_df.copy()
    
    # Convert Predicted_Date to datetime if it's a string
    if chart_df['Predicted_Date'].dtype == 'object':
        chart_df['Predicted_Date'] = pd.to_datetime(chart_df['Predicted_Date'])
    
    # Sort by date and TP
    chart_df = chart_df.sort_values(['Predicted_Date', 'TP'])
    
    # Get unique list of TPs
    unique_tps = sorted(chart_df['TP'].unique())
    num_tps = len(unique_tps)
    
    # Create orange gradient for different TPs
    # Orange colors from lightest to darkest
    orange_gradient = [
        '#FFE5CC',  # Very light
        '#FFD4A3',  # Light
        '#FFC380',  # Medium-light
        '#FFB259',  # Medium
        '#FFA033',  # Medium-dark
        '#FF8F0D',  # Dark
        '#FF7F00',  # Very dark
        '#FF6B35',  # Intense orange
        '#FF5722',  # Reddish orange
        '#FF4500'   # Red orange
    ]
    
    # If there are more TPs than colors, repeat the gradient
    if num_tps > len(orange_gradient):
        orange_gradient = orange_gradient * ((num_tps // len(orange_gradient)) + 1)
    
    fig = go.Figure()
    
    # Add a line for each TP
    for idx, tp in enumerate(unique_tps):
        tp_data = chart_df[chart_df['TP'] == tp].copy()
        tp_data = tp_data.sort_values('Predicted_Date')
        
        color = orange_gradient[idx % len(orange_gradient)]
        
        fig.add_trace(go.Scatter(
            x=tp_data['Predicted_Date'],
            y=tp_data['Predicted_Real_Price'].astype(float),
            mode='lines+markers',
            name=tp,
            line=dict(color=color, width=4),
            marker=dict(size=10, color=color, line=dict(color='white', width=1.5)),
            hovertemplate=f'<b>{tp}</b><br>Date: %{{x|%Y-%m-%d}}<br>Price: $%{{y:,.2f}}<br>SKU: {selected_sku}<extra></extra>'
        ))
    
    # Calculate price range
    max_price = chart_df['Predicted_Real_Price'].astype(float).max()
    min_price = chart_df['Predicted_Real_Price'].astype(float).min()
    price_range = max_price - min_price
    y_max = max_price + (price_range * 0.1) if price_range > 0 else max_price * 1.1
    y_min = min_price - (price_range * 0.1) if price_range > 0 else 0
    
    # Format date range for the title
    if isinstance(forecast_date_range, tuple) and len(forecast_date_range) == 2:
        start_date = forecast_date_range[0].strftime("%Y-%m-%d") if hasattr(forecast_date_range[0], "strftime") else str(forecast_date_range[0])
        end_date = forecast_date_range[1].strftime("%Y-%m-%d") if hasattr(forecast_date_range[1], "strftime") else str(forecast_date_range[1])
        date_label = f"{start_date} to {end_date}"
    else:
        date_label = str(forecast_date_range)
    
    fig.update_layout(
        title=f"Predicted Price Over Time by Trading Partner - {selected_sku}",
        xaxis_title="Time",
        yaxis_title="Predicted Price",
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
            gridwidth=1,
            type='date'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            gridwidth=1,
            range=[y_min, y_max]
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_prediction_table(predictions_df: pd.DataFrame):
    """Show raw prediction results for transparency."""
    if predictions_df is None or predictions_df.empty:
        return
    
    display_cols = ['SKU', 'TP', 'CATEGORY', 'Predicted_Date', 'Predicted_Real_Price', 'Adjusted_for_Inflation']
    table_df = predictions_df[display_cols].copy()
    table_df['Predicted_Real_Price'] = table_df['Predicted_Real_Price'].map(lambda x: f"${x:,.2f}")
    
    st.markdown("### Prediction Output")
    st.dataframe(table_df, use_container_width=True, hide_index=True)


def render_prediction_dashboard():
    """Render the prediction dashboard with focused SKU/date range inputs and chart"""
    st.title("Prediction")
    
    if 'prediction_inputs' not in st.session_state:
        today = datetime.today().date()
        st.session_state.prediction_inputs = {
            "sku": config.DEFAULT_SKUS[0],
            "date_range": (today, today + timedelta(days=30))
        }
        st.session_state.prediction_ran = False
    if 'prediction_results' not in st.session_state:
        st.session_state.prediction_results = None
    
    col1, col2 = st.columns([2, 1], gap="medium")
    
    with col1:
        selected_sku = st.selectbox(
            "SKU",
            options=config.DEFAULT_SKUS,
            key="prediction_sku"
        )
    
    with col2:
        today = datetime.today().date()
        default_range = st.session_state.prediction_inputs.get("date_range", (today, today + timedelta(days=30)))
        forecast_date_range = st.date_input(
            "Forecast Range",
            value=default_range,
            key="prediction_forecast_date_range"
        )
    
    run_col, _ = st.columns([1, 4])
    with run_col:
        if st.button("Run Prediction", type="primary", use_container_width=True, key="prediction_run_button"):
            with st.spinner("Running XGBoost prediction..."):
                try:
                    # Convert date range to tuple of strings
                    if isinstance(forecast_date_range, tuple) and len(forecast_date_range) == 2:
                        date_range_str = (
                            forecast_date_range[0].strftime("%Y-%m-%d"),
                            forecast_date_range[1].strftime("%Y-%m-%d")
                        )
                    else:
                        # If there's only one date, create a one-day range
                        single_date = forecast_date_range if isinstance(forecast_date_range, datetime) else forecast_date_range[0]
                        date_str = single_date.strftime("%Y-%m-%d")
                        date_range_str = (date_str, date_str)
                    
                    predictions_df = predict_price_scenario_xgb_from_pickle(
                        sku_list=[selected_sku],
                        date_input=date_range_str
                    )
                    if predictions_df is None or predictions_df.empty:
                        st.warning("No predictions returned for the selected SKU.")
                        st.session_state.prediction_ran = False
                        st.session_state.prediction_results = None
                    else:
                        st.session_state.prediction_inputs = {
                            "sku": selected_sku,
                            "date_range": forecast_date_range
                        }
                        st.session_state.prediction_results = predictions_df
                        st.session_state.prediction_ran = True
                except Exception as exc:
                    st.error(f"Prediction failed: {exc}")
                    st.session_state.prediction_ran = False
                    st.session_state.prediction_results = None
    
    predictions_df = st.session_state.prediction_results
    if st.session_state.get("prediction_ran") and predictions_df is not None:
        inputs = st.session_state.prediction_inputs
        render_prediction_chart(inputs["sku"], inputs["date_range"], predictions_df)
    else:
        st.info("Select a SKU, a date range and run the prediction to see the model result.")
    
    
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
