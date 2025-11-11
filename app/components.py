import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def render_file_uploader():
    """Render file uploader component"""
    st.sidebar.header("📁 Data Upload")
    
    uploaded_file = st.sidebar.file_uploader(
        "Upload Solar Data CSV",
        type=['csv'],
        help="Upload your solar farm data CSV file"
    )
    
    return uploaded_file

def render_sidebar_filters(df):
    """Render interactive filters in sidebar"""
    st.sidebar.header("🔧 Filters & Controls")
    
    # Date range filter
    if hasattr(df.index, 'min'):
        min_date = df.index.min()
        max_date = df.index.max()
        
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
    
    # Column selector for analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    selected_columns = st.sidebar.multiselect(
        "Select Metrics to Analyze",
        options=numeric_cols,
        default=numeric_cols[:3] if len(numeric_cols) >= 3 else numeric_cols
    )
    
    # Analysis type selector
    analysis_type = st.sidebar.selectbox(
        "Analysis Focus",
        ["Solar Potential", "Weather Impact", "Time Patterns", "Data Quality"]
    )
    
    return {
        'selected_columns': selected_columns,
        'analysis_type': analysis_type
    }

def render_solar_scorecard(score_data, filename):
    """Render solar potential scorecard"""
    if not score_data:
        return
    
    st.header("🏆 Solar Potential Assessment")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Overall Score",
            value=f"{score_data['total_score']:.1f}/100",
            delta="High Potential" if score_data['total_score'] > 70 else "Moderate"
        )
    
    with col2:
        st.metric(
            label="Energy Potential",
            value=f"{score_data['components']['energy']:.1f}/40"
        )
    
    with col3:
        st.metric(
            label="Consistency",
            value=f"{score_data['components']['consistency']:.1f}/30"
        )
    
    with col4:
        st.metric(
            label="Reliability",
            value=f"{score_data['components']['reliability']:.1f}/20"
        )
    
    # Score breakdown
    st.subheader("Score Components")
    components = score_data['components']
    fig = go.Figure(data=[
        go.Bar(name='Score', x=list(components.keys()), y=list(components.values()))
    ])
    fig.update_layout(title="Solar Potential Score Breakdown")
    st.plotly_chart(fig, use_container_width=True)

def render_data_overview(df, filename):
    """Render data overview section"""
    st.header("📊 Data Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", f"{len(df):,}")
    
    with col2:
        st.metric("Columns", len(df.columns))
    
    with col3:
        st.metric("Date Range", f"{df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}")
    
    with col4:
        missing = df.isnull().sum().sum()
        st.metric("Missing Values", f"{missing:,}")
    
    # Show dataframe
    with st.expander("View Raw Data"):
        st.dataframe(df, use_container_width=True)
    
    # Column info
    with st.expander("Column Information"):
        col_info = pd.DataFrame({
            'Column': df.columns,
            'Data Type': df.dtypes,
            'Non-Null Count': df.count(),
            'Null Count': df.isnull().sum()
        })
        st.dataframe(col_info, use_container_width=True)

def render_interactive_plots(df, filters):
    """Render interactive visualization section"""
    st.header("📈 Interactive Analysis")
    
    # Plot type selector
    plot_type = st.selectbox(
        "Select Plot Type",
        ["Time Series", "Distribution", "Correlation", "Scatter Plot", "Daily Pattern"]
    )
    
    if plot_type == "Time Series":
        col = st.selectbox("Select Metric", filters['selected_columns'])
        fig = px.line(df, y=col, title=f"{col} Time Series")
        st.plotly_chart(fig, use_container_width=True)
    
    elif plot_type == "Distribution":
        col = st.selectbox("Select Metric", filters['selected_columns'])
        fig = px.histogram(df, x=col, title=f"{col} Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    elif plot_type == "Correlation":
        if len(filters['selected_columns']) >= 2:
            corr_matrix = df[filters['selected_columns']].corr()
            fig = px.imshow(corr_matrix, title="Correlation Matrix")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Select at least 2 metrics for correlation analysis")
    
    elif plot_type == "Scatter Plot":
        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox("X-Axis", filters['selected_columns'])
        with col2:
            y_axis = st.selectbox("Y-Axis", filters['selected_columns'])
        
        fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
        st.plotly_chart(fig, use_container_width=True)
    
    elif plot_type == "Daily Pattern":
        if 'GHI' in df.columns and 'Hour' in df.columns:
            daily_avg = df.groupby('Hour')['GHI'].mean()
            fig = px.line(x=daily_avg.index, y=daily_avg.values, 
                         title="Average Daily GHI Pattern")
            fig.update_layout(xaxis_title="Hour of Day", yaxis_title="GHI (W/m²)")
            st.plotly_chart(fig, use_container_width=True)

def render_weather_impact(df):
    """Render weather impact analysis"""
    if 'GHI' not in df.columns:
        return
    
    st.header("🌦️ Weather Impact Analysis")
    
    # Weather variables to check
    weather_vars = ['Tamb', 'RH', 'WS', 'BP', 'Precipitation']
    available_weather = [var for var in weather_vars if var in df.columns]
    
    if available_weather:
        col = st.selectbox("Select Weather Variable", available_weather)
        
        # Scatter plot with trendline
        fig = px.scatter(df, x=col, y='GHI', 
                        trendline="lowess",
                        title=f"GHI vs {col}",
                        labels={col: f"{col} ({get_units(col)})", 'GHI': 'GHI (W/m²)'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Correlation value
        correlation = df['GHI'].corr(df[col])
        st.info(f"Correlation between GHI and {col}: **{correlation:.3f}**")

def get_units(column_name):
    """Return units for column names"""
    units_map = {
        'GHI': 'W/m²', 'DNI': 'W/m²', 'DHI': 'W/m²', 
        'ModA': 'W/m²', 'ModB': 'W/m²',
        'Tamb': '°C', 'TModA': '°C', 'TModB': '°C',
        'RH': '%', 'WS': 'm/s', 'WSgust': 'm/s', 'BP': 'hPa',
        'WD': '°N', 'Precipitation': 'mm/min'
    }
    return units_map.get(column_name, '')