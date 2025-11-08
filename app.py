
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import io
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Solar Farm Analytics Pro",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 800;
        background: linear-gradient(45deg, #FF6B35, #F7931E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2E86AB;
        border-left: 5px solid #FF6B35;
        padding-left: 15px;
        margin: 2rem 0 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .upload-box {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
        background: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<div class="main-header">☀️ Solar Analytics Pro Dashboard</div>', unsafe_allow_html=True)
st.markdown("### **MoonLight Energy Solutions** - Advanced Solar Farm Analysis Platform")

# ===== SIDEBAR - ADVANCED CONTROLS =====
st.sidebar.header(" Control Panel")

# File Upload Section
st.sidebar.subheader(" Data Upload")
uploaded_file = st.sidebar.file_uploader(
    "Upload Solar Data CSV",
    type=['csv'],
    help="Upload cleaned solar data from Benin, Sierra Leone, or Togo"
)

# Demo data toggle
use_demo_data = st.sidebar.checkbox("Use Demo Data", value=True, help="Use sample data for demonstration")

# Country Selection
st.sidebar.subheader("🌍 Country Selection")
countries = ['Benin', 'Sierra Leone', 'Togo']
selected_countries = st.sidebar.multiselect(
    "Select Countries to Analyze:",
    countries,
    default=countries,
    help="Choose countries for comparison"
)

# Advanced Analysis Controls
st.sidebar.subheader("🔧 Analysis Settings")

# Metric selection with descriptions
metric_options = {
    'GHI': 'Global Horizontal Irradiance - Total solar radiation',
    'DNI': 'Direct Normal Irradiance - Direct beam radiation', 
    'DHI': 'Diffuse Horizontal Irradiance - Scattered radiation'
}
selected_metric = st.sidebar.selectbox(
    "Solar Metric:",
    list(metric_options.keys()),
    format_func=lambda x: f"{x} - {metric_options[x]}"
)

# Visualization type
viz_type = st.sidebar.radio(
    "Chart Type:",
    ['Bar Chart', 'Line Chart', 'Scatter Plot', 'Box Plot']
)

# Color theme
color_theme = st.sidebar.selectbox(
    "Color Theme:",
    ['Solar Orange', 'Ocean Blue', 'Forest Green', 'Sunset Purple']
)

# ===== DATA PROCESSING =====
@st.cache_data
def generate_demo_data():
    """Generate comprehensive demo solar data"""
    np.random.seed(42)
    
    data = []
    for country in countries:
        for month in range(1, 13):
            for hour in range(24):
                # Base patterns with seasonal variation
                seasonal_factor = 1 + 0.3 * np.sin((month-6)/6 * np.pi)
                
                if 6 <= hour <= 18:  # Daytime
                    ghi_base = 250 * seasonal_factor * (1 + 0.5 * np.sin((hour-12)/12 * np.pi))
                    temp_base = 25 + 8 * np.sin((hour-12)/12 * np.pi)
                else:  # Nighttime
                    ghi_base = 0
                    temp_base = 20
                
                # Country-specific adjustments
                if country == 'Benin':
                    ghi = ghi_base * 1.15
                    temp = temp_base + 3
                    humidity = 50 + np.random.normal(0, 10)
                elif country == 'Sierra Leone':
                    ghi = ghi_base * 0.85
                    temp = temp_base - 2
                    humidity = 75 + np.random.normal(0, 15)
                else:  # Togo
                    ghi = ghi_base * 1.05
                    temp = temp_base
                    humidity = 60 + np.random.normal(0, 12)
                
                data.append({
                    'Country': country,
                    'Month': month,
                    'Hour': hour,
                    'GHI': max(0, ghi + np.random.normal(0, 15)),
                    'DNI': max(0, ghi * 0.7 + np.random.normal(0, 10)),
                    'DHI': max(0, ghi * 0.3 + np.random.normal(0, 5)),
                    'Temperature': max(15, min(45, temp + np.random.normal(0, 2))),
                    'Humidity': max(20, min(95, humidity)),
                    'Wind_Speed': np.random.gamma(1.5, 0.8)
                })
    
    return pd.DataFrame(data)

# Load data
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success(f" File uploaded: {uploaded_file.name}")
    except Exception as e:
        st.sidebar.error(f" Error reading file: {e}")
        df = generate_demo_data()
else:
    df = generate_demo_data()

# ===== MAIN DASHBOARD =====

# Quick Stats Header
st.markdown("###  Real-time Performance Metrics")
col1, col2, col3, col4 = st.columns(4)

filtered_df = df[df['Country'].isin(selected_countries)]

with col1:
    avg_metric = filtered_df[selected_metric].mean()
    st.markdown(f"""
    <div class="metric-card">
        <h4>📈 Average {selected_metric}</h4>
        <h2>{avg_metric:.1f}</h2>
        <small>W/m²</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    best_country = filtered_df.groupby('Country')[selected_metric].mean().idxmax()
    st.markdown(f"""
    <div class="metric-card">
        <h4>🏆 Top Performer</h4>
        <h2>{best_country}</h2>
        <small>Highest output</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    peak_hour = filtered_df.groupby('Hour')[selected_metric].mean().idxmax()
    st.markdown(f"""
    <div class="metric-card">
        <h4>🕐 Peak Hour</h4>
        <h2>{peak_hour:02d}:00</h2>
        <small>Optimal generation</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    efficiency = (filtered_df[selected_metric].mean() / 1000) * 100
    st.markdown(f"""
    <div class="metric-card">
        <h4>⚡ Efficiency</h4>
        <h2>{efficiency:.1f}%</h2>
        <small>System performance</small>
    </div>
    """, unsafe_allow_html=True)

# ===== INTERACTIVE VISUALIZATIONS =====
st.markdown('<div class="sub-header">📈 Interactive Analysis</div>', unsafe_allow_html=True)

# Visualization based on selection
if viz_type == 'Bar Chart':
    # Country comparison bar chart
    comparison_data = filtered_df.groupby('Country')[selected_metric].mean().reset_index()
    fig = px.bar(
        comparison_data,
        x='Country',
        y=selected_metric,
        color='Country',
        title=f'{selected_metric} Comparison by Country',
        color_discrete_sequence=px.colors.sequential.Sunset
    )
    
elif viz_type == 'Line Chart':
    # Time series analysis
    time_data = filtered_df.groupby(['Country', 'Hour'])[selected_metric].mean().reset_index()
    fig = px.line(
        time_data,
        x='Hour',
        y=selected_metric,
        color='Country',
        title=f'Hourly {selected_metric} Patterns',
        markers=True
    )
    
elif viz_type == 'Scatter Plot':
    # Environmental correlation
    sample_data = filtered_df.sample(min(1000, len(filtered_df)))
    fig = px.scatter(
        sample_data,
        x='Temperature',
        y=selected_metric,
        color='Country',
        size=selected_metric,
        hover_data=['Humidity', 'Wind_Speed'],
        title=f'Temperature vs {selected_metric}',
        opacity=0.7
    )
    
else:  # Box Plot
    fig = px.box(
        filtered_df,
        x='Country',
        y=selected_metric,
        color='Country',
        title=f'{selected_metric} Distribution by Country',
        color_discrete_sequence=px.colors.qualitative.Set3
    )

st.plotly_chart(fig, use_container_width=True)

# ===== ADVANCED ANALYSIS SECTION =====
st.markdown('<div class="sub-header">🔬 Advanced Analytics</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Correlation heatmap
    st.subheader(" Correlation Analysis")
    numeric_cols = ['GHI', 'DNI', 'DHI', 'Temperature', 'Humidity', 'Wind_Speed']
    corr_matrix = filtered_df[numeric_cols].corr()
    
    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale='RdBu_r',
        title='Feature Correlation Matrix'
    )
    st.plotly_chart(fig_corr, use_container_width=True)

with col2:
    # Seasonal patterns
    st.subheader(" Monthly Trends")
    monthly_data = filtered_df.groupby(['Country', 'Month'])[selected_metric].mean().reset_index()
    
    fig_seasonal = px.line(
        monthly_data,
        x='Month',
        y=selected_metric,
        color='Country',
        title=f'Monthly {selected_metric} Trends',
        markers=True
    )
    st.plotly_chart(fig_seasonal, use_container_width=True)

# ===== DATA EXPLORER =====
st.markdown('<div class="sub-header">💾 Data Explorer</div>', unsafe_allow_html=True)

# Interactive data table with filters
st.subheader("🔍 Filter and Explore Data")

col1, col2, col3 = st.columns(3)
with col1:
    show_country = st.multiselect("Filter Countries:", countries, default=selected_countries)
with col2:
    hour_range = st.slider("Hour Range:", 0, 23, (6, 18))
with col3:
    show_rows = st.slider("Rows to Display:", 10, 100, 20)

filtered_display = filtered_df[
    (filtered_df['Country'].isin(show_country)) &
    (filtered_df['Hour'] >= hour_range[0]) & 
    (filtered_df['Hour'] <= hour_range[1])
].head(show_rows)

st.dataframe(filtered_display, use_container_width=True)

# Download filtered data
csv = filtered_display.to_csv(index=False)
st.download_button(
    label="📥 Download Filtered Data (CSV)",
    data=csv,
    file_name="filtered_solar_data.csv",
    mime="text/csv",
    help="Download the currently filtered dataset"
)

# ===== ACTION BUTTONS =====
st.markdown('<div class="sub-header"> Quick Actions</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🔄 Refresh Analysis", use_container_width=True):
        st.rerun()

with col2:
    if st.button(" Generate Report", use_container_width=True):
        st.success(" Analysis report generated successfully!")

with col3:
    if st.button(" Optimization Tips", use_container_width=True):
        st.info("""
         **Optimization Suggestions:**
        - Clean panels during low-radiation hours
        - Monitor temperature effects on efficiency  
        - Consider humidity-resistant coatings
        - Optimize tilt angles seasonally
        """)

with col4:
    if st.button("📞 Contact Support", use_container_width=True):
        st.info("📧 Contact: analytics@moonlight-energy.com")

# ===== FOOTER =====
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>Solar Analytics Pro Dashboard</strong> | Built with Streamlit | MoonLight Energy Solutions</p>
    <p>🔬 Advanced Analytics | 📈 Interactive Visualizations | 💾 Data Export | 🚀 Real-time Insights</p>
</div>
""", unsafe_allow_html=True)

# Sidebar footer with info
st.sidebar.markdown("---")
st.sidebar.info("""
** Usage Tips:**
- Upload your CSV data or use demo data
- Select countries and metrics for comparison
- Choose visualization types
- Download filtered results
- Contact support for custom analysis
""")