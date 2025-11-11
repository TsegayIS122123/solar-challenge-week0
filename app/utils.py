import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

def load_data(uploaded_file):
    """Load and preprocess uploaded CSV file"""
    try:
        df = pd.read_csv(uploaded_file)
        
        # Auto-detect timestamp column
        timestamp_cols = ['Timestamp', 'timestamp', 'Date', 'date', 'Time', 'time']
        for col in timestamp_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
                df.set_index(col, inplace=True)
                break
        
        # Create time-based features
        df['Hour'] = df.index.hour
        df['Month'] = df.index.month
        df['DayOfWeek'] = df.index.dayofweek
        
        return df, f"Successfully loaded {len(df)} rows with {len(df.columns)} columns"
    
    except Exception as e:
        return None, f"Error loading file: {str(e)}"

def create_solar_score(df):
    """Calculate comprehensive solar potential score"""
    if 'GHI' not in df.columns:
        return None
    
    scores = {}
    
    # Energy Potential (40%)
    energy_score = df['GHI'].mean()
    scores['energy'] = energy_score
    
    # Consistency (30%) - lower variability is better
    if df['GHI'].std() > 0:
        consistency = (1 - (df['GHI'].std() / df['GHI'].mean())) * 100
        scores['consistency'] = max(consistency, 0)
    
    # Reliability (20%) - percentage of optimal hours
    optimal_threshold = df['GHI'].quantile(0.7)
    reliability = (df['GHI'] > optimal_threshold).mean() * 100
    scores['reliability'] = reliability
    
    # Weather Resilience (10%)
    weather_score = 100
    if 'RH' in df.columns:
        high_humidity = (df['RH'] > 85).mean() * 100
        weather_score -= high_humidity * 0.5
    
    scores['weather'] = max(weather_score, 0)
    
    # Normalize and calculate total score
    max_energy = max(energy_score, 500)  # Reasonable max
    normalized_scores = {
        'energy': (energy_score / max_energy) * 40,
        'consistency': (scores['consistency'] / 100) * 30,
        'reliability': (reliability / 100) * 20,
        'weather': (scores['weather'] / 100) * 10
    }
    
    total_score = sum(normalized_scores.values())
    
    return {
        'total_score': total_score,
        'components': normalized_scores,
        'raw_scores': scores
    }

def create_ghi_distribution(df):
    """Create GHI distribution plot"""
    fig = px.histogram(df, x='GHI', 
                      title='Global Horizontal Irradiance Distribution',
                      labels={'GHI': 'GHI (W/m²)'},
                      color_discrete_sequence=['#FF6B00'])
    fig.update_layout(showlegend=False)
    return fig

def create_time_series(df, column):
    """Create interactive time series plot"""
    fig = px.line(df, y=column, 
                 title=f'{column} Time Series',
                 labels={column: f'{column} ({get_units(column)})', 'index': 'Timestamp'})
    fig.update_traces(line_width=1)
    return fig

def create_correlation_heatmap(df):
    """Create correlation heatmap for numeric columns"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    corr_matrix = df[numeric_cols].corr()
    
    fig = px.imshow(corr_matrix, 
                   title='Correlation Matrix',
                   color_continuous_scale='RdBu_r',
                   aspect="auto")
    return fig

def create_daily_pattern(df):
    """Create daily pattern visualization"""
    if 'GHI' in df.columns and 'Hour' in df.columns:
        hourly_pattern = df.groupby('Hour')['GHI'].agg(['mean', 'std']).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hourly_pattern['Hour'], y=hourly_pattern['mean'],
                               mode='lines+markers', name='Average GHI',
                               line=dict(color='#FF6B00', width=3)))
        
        fig.add_trace(go.Scatter(x=hourly_pattern['Hour'], 
                               y=hourly_pattern['mean'] + hourly_pattern['std'],
                               mode='lines', name='+1 STD',
                               line=dict(color='gray', width=1, dash='dash')))
        
        fig.add_trace(go.Scatter(x=hourly_pattern['Hour'], 
                               y=hourly_pattern['mean'] - hourly_pattern['std'],
                               mode='lines', name='-1 STD',
                               line=dict(color='gray', width=1, dash='dash'),
                               fill='tonexty'))
        
        fig.update_layout(title='Daily Solar Pattern with Variability',
                         xaxis_title='Hour of Day',
                         yaxis_title='GHI (W/m²)')
        return fig
    return None

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