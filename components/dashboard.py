"""
Dashboard component with KPIs, charts, and metrics
"""
import streamlit as st
import plotly.graph_objects as go
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


def render_sales_chart():
    """Render sales overview chart"""
    sales_data = data_service.get_sales_data()
    
    fig = go.Figure()
    
    # Add first series
    fig.add_trace(go.Scatter(
        x=sales_data["months"],
        y=sales_data["values"][0]["data"],
        fill='tozeroy',
        mode='lines',
        name=sales_data["values"][0]["name"],
        line=dict(color='rgba(255, 107, 53, 0.6)'),
        fillcolor='rgba(255, 107, 53, 0.3)'
    ))
    
    # Add second series
    fig.add_trace(go.Scatter(
        x=sales_data["months"],
        y=sales_data["values"][1]["data"],
        fill='tonexty',
        mode='lines',
        name=sales_data["values"][1]["name"],
        line=dict(color='rgba(247, 147, 30, 0.6)'),
        fillcolor='rgba(247, 147, 30, 0.3)'
    ))
    
    fig.update_layout(
        title="Sales overview (+5) more in 2021",
        xaxis_title="Month",
        yaxis_title="Sales",
        hovermode='x unified',
        height=400,
        showlegend=True,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig, width='stretch')


def render_active_users():
    """Render active users metrics"""
    st.markdown("### Active Users (+23) than last week")
    
    metrics = data_service.get_active_users()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Users", format_number(metrics["users"]))
    
    with col2:
        st.metric("Clicks", format_number(metrics["clicks"]))
    
    with col3:
        st.metric("Sales", format_currency(metrics["sales"]))
    
    with col4:
        st.metric("Items", format_number(metrics["items"]))


def render_dashboard():
    """Render the main dashboard"""
    st.title("Dashboardd")
    
    # KPIs
    render_kpi_cards()
    
    st.markdown("---")
    
    # Sales chart
    render_sales_chart()
    
    st.markdown("---")
    
    # Active users
    render_active_users()

