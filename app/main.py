import streamlit as st
import pandas as pd
import numpy as np
from utils import load_data, create_solar_score
from components import (render_file_uploader, render_sidebar_filters, 
                       render_solar_scorecard, render_data_overview,
                       render_interactive_plots, render_weather_impact)

# Page configuration
st.set_page_config(
    page_title="Solar Farm Analyzer",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B00;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2E86AB;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #FF6B00;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">☀️ Solar Farm Analytics Dashboard</h1>', 
                unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h3>Upload your solar farm data CSV file to analyze solar potential and performance</h3>
        <p>Supports data from Benin, Sierra Leone, Togo, or any solar monitoring system</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = render_file_uploader()
    
    if uploaded_file is not None:
        # Load and process data
        df, message = load_data(uploaded_file)
        
        if df is not None:
            st.success(f" {message}")
            
            # Sidebar filters
            filters = render_sidebar_filters(df)
            
            # Main content area
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "🏆 Overview", "📈 Analysis", "🌦️ Weather", "📋 Data", "💡 Insights"
            ])
            
            with tab1:
                # Solar potential scorecard
                score_data = create_solar_score(df)
                render_solar_scorecard(score_data, uploaded_file.name)
                
                # Quick stats
                col1, col2 = st.columns(2)
                with col1:
                    if 'GHI' in df.columns:
                        st.metric("Average GHI", f"{df['GHI'].mean():.1f} W/m²")
                    if 'Tamb' in df.columns:
                        st.metric("Average Temperature", f"{df['Tamb'].mean():.1f} °C")
                
                with col2:
                    if 'RH' in df.columns:
                        st.metric("Average Humidity", f"{df['RH'].mean():.1f} %")
                    if 'WS' in df.columns:
                        st.metric("Average Wind Speed", f"{df['WS'].mean():.1f} m/s")
            
            with tab2:
                render_interactive_plots(df, filters)
            
            with tab3:
                render_weather_impact(df)
            
            with tab4:
                render_data_overview(df, uploaded_file.name)
            
            with tab5:
                st.header("💡 Business Insights & Recommendations")
                
                if score_data:
                    st.subheader("Solar Potential Assessment")
                    
                    if score_data['total_score'] >= 80:
                        st.success("""
                        **🎯 EXCELLENT POTENTIAL**
                        - This location shows outstanding solar characteristics
                        - High recommendation for solar farm development
                        - Expected high return on investment
                        """)
                    elif score_data['total_score'] >= 60:
                        st.warning("""
                        **📊 GOOD POTENTIAL** 
                        - Viable location for solar investment
                        - Moderate to good energy yield expected
                        - Consider detailed feasibility study
                        """)
                    else:
                        st.error("""
                        **⚠️ MODERATE POTENTIAL**
                        - Lower than optimal solar conditions
                        - Consider alternative locations or technologies
                        - Further analysis recommended
                        """)
                
                # Technology recommendations
                st.subheader("Technology Recommendations")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.info("""
                    **Photovoltaic (PV) Systems**
                    - Suitable for all locations
                    - Lower maintenance requirements
                    - Proven technology
                    """)
                
                with col2:
                    st.info("""
                    **Tracking Systems**
                    - Consider for high DNI locations
                    - 15-25% efficiency improvement
                    - Higher initial investment
                    """)
                
                with col3:
                    st.info("""
                    **Hybrid Solutions**
                    - Combine with storage for reliability
                    - Good for locations with variability
                    - Future-proof investment
                    """)
        
        else:
            st.error(f"❌ {message}")
            st.info("""
            **Expected CSV Format:**
            - Should contain columns like GHI, DNI, DHI, Tamb, RH, WS, etc.
            - Include a timestamp column (Timestamp, Date, etc.)
            - Numeric values for solar and weather measurements
            """)
    
    else:
        # Welcome screen when no file uploaded
        st.markdown("""
        <div style='text-align: center; padding: 4rem; background-color: #444444; border-radius: 10px;'>
            <h2>🚀 Get Started</h2>
            <p>Upload your solar data CSV file to begin analysis</p>
            <p><em>Use the file uploader in the sidebar →</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Example of expected data format
        with st.expander("📋 Expected Data Format"):
            st.markdown("""
            Your CSV file should include columns like:
            
            **Required:**
            - `Timestamp` - Date and time of measurements
            - `GHI` - Global Horizontal Irradiance (W/m²)
            
            **Recommended:**
            - `DNI`, `DHI` - Other irradiance measurements
            - `Tamb` - Ambient temperature (°C)
            - `RH` - Relative humidity (%)
            - `WS` - Wind speed (m/s)
            - `BP` - Barometric pressure (hPa)
            
            **Example data structure:**
            ```
            Timestamp,GHI,DNI,DHI,Tamb,RH,WS,BP
            2024-01-01 06:00:00,45.2,120.5,35.1,22.5,85.2,2.1,1013.2
            2024-01-01 07:00:00,120.8,250.3,45.6,24.1,78.5,2.5,1013.0
            ```
            """)

if __name__ == "__main__":
    main()