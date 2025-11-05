"""
Dashboard component with KPIs, charts, and metrics
"""
import streamlit as st
import plotly.graph_objects as go
from services.data_service import DataService
from utils.helpers import format_currency, format_number, format_percentage

data_service = DataService()


def render_kpi_cards():
    """Render KPI cards"""
    kpis = data_service.get_kpis()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Today's Money",
            value=format_currency(kpis["todays_money"]),
            delta=format_percentage(kpis["money_change"])
        )
    
    with col2:
        st.metric(
            label="Today's Users",
            value=format_number(kpis["todays_users"]),
            delta=format_percentage(kpis["users_change"])
        )
    
    with col3:
        st.metric(
            label="Today's Users",
            value=format_number(kpis["todays_users"]),
            delta=format_percentage(kpis["users_change"])
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
    st.title("Dashboard")
    
    # KPIs
    render_kpi_cards()
    
    st.markdown("---")
    
    # Sales chart
    render_sales_chart()
    
    st.markdown("---")
    
    # Active users
    render_active_users()

