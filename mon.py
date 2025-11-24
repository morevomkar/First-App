# Economic Indicators Dashboard with Streamlit
# Install required packages: pip install streamlit pandas plotly fredapi

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from fredapi import Fred
import os

# FRED API Configuration
# Get your free API key from: https://fred.stlouisfed.org/docs/api/api_key.html
FRED_API_KEY = os.environ.get('FRED_API_KEY', 'your_api_key_here')

@st.cache_data(ttl=3600)
def fetch_economic_data(indicator, start_date, end_date):
    """Fetch data from FRED API"""
    try:
        fred = Fred(api_key=FRED_API_KEY)
        data = fred.get_series(indicator, start_date, end_date)
        return data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

def create_plot(data, title, yaxis_title):
    """Create interactive plotly chart"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data.values,
        mode='lines',
        name=title,
        line=dict(color='#1f77b4', width=2)
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title=yaxis_title,
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig

def calculate_statistics(data):
    """Calculate key statistics"""
    if data is None or len(data) == 0:
        return {}
    
    return {
        'Current': data.iloc[-1],
        'Previous': data.iloc[-2] if len(data) > 1 else None,
        'Change': data.iloc[-1] - data.iloc[-2] if len(data) > 1 else None,
        'Max': data.max(),
        'Min': data.min(),
        'Mean': data.mean(),
        'Std Dev': data.std()
    }

# Streamlit App
def main():
    st.set_page_config(page_title="Economic Indicators Dashboard", layout="wide")
    
    st.title("📊 Economic Indicators Dashboard")
    st.markdown("Real-time data from Federal Reserve Economic Data (FRED)")
    
    # Sidebar for date selection
    st.sidebar.header("Settings")
    
    years_back = st.sidebar.slider("Years of historical data", 1, 20, 5)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years_back*365)
    
    # Economic indicators mapping
    indicators = {
        'CPI': {
            'id': 'CPIAUCSL',
            'name': 'Consumer Price Index (CPI)',
            'unit': 'Index 1982-84=100'
        },
        'PPI': {
            'id': 'PPIACO',
            'name': 'Producer Price Index (PPI)',
            'unit': 'Index 1982=100'
        },
        'Interest Rate': {
            'id': 'FEDFUNDS',
            'name': 'Federal Funds Effective Rate',
            'unit': 'Percent'
        }
    }
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 CPI", "🏭 PPI", "💰 Interest Rate", "📊 Comparison"])
    
    # Tab 1: CPI
    with tab1:
        st.header("Consumer Price Index (CPI)")
        st.markdown("Measures the average change in prices paid by consumers for goods and services")
        
        cpi_data = fetch_economic_data(indicators['CPI']['id'], start_date, end_date)
        
        if cpi_data is not None:
            col1, col2, col3 = st.columns(3)
            stats = calculate_statistics(cpi_data)
            
            with col1:
                st.metric("Current CPI", f"{stats['Current']:.2f}", 
                         f"{stats['Change']:.2f}" if stats['Change'] else None)
            with col2:
                st.metric("Average", f"{stats['Mean']:.2f}")
            with col3:
                st.metric("Range", f"{stats['Min']:.2f} - {stats['Max']:.2f}")
            
            fig = create_plot(cpi_data, "Consumer Price Index", indicators['CPI']['unit'])
            st.plotly_chart(fig, use_container_width=True)
            
            # YoY Change
            cpi_pct = cpi_data.pct_change(periods=12) * 100
            fig_pct = create_plot(cpi_pct, "CPI Year-over-Year % Change", "Percent")
            st.plotly_chart(fig_pct, use_container_width=True)
    
    # Tab 2: PPI
    with tab2:
        st.header("Producer Price Index (PPI)")
        st.markdown("Measures the average change in selling prices received by producers")
        
        ppi_data = fetch_economic_data(indicators['PPI']['id'], start_date, end_date)
        
        if ppi_data is not None:
            col1, col2, col3 = st.columns(3)
            stats = calculate_statistics(ppi_data)
            
            with col1:
                st.metric("Current PPI", f"{stats['Current']:.2f}", 
                         f"{stats['Change']:.2f}" if stats['Change'] else None)
            with col2:
                st.metric("Average", f"{stats['Mean']:.2f}")
            with col3:
                st.metric("Range", f"{stats['Min']:.2f} - {stats['Max']:.2f}")
            
            fig = create_plot(ppi_data, "Producer Price Index", indicators['PPI']['unit'])
            st.plotly_chart(fig, use_container_width=True)
            
            # YoY Change
            ppi_pct = ppi_data.pct_change(periods=12) * 100
            fig_pct = create_plot(ppi_pct, "PPI Year-over-Year % Change", "Percent")
            st.plotly_chart(fig_pct, use_container_width=True)
    
    # Tab 3: Interest Rate
    with tab3:
        st.header("Federal Funds Effective Rate")
        st.markdown("The interest rate at which banks lend reserve balances to other banks overnight")
        
        rate_data = fetch_economic_data(indicators['Interest Rate']['id'], start_date, end_date)
        
        if rate_data is not None:
            col1, col2, col3 = st.columns(3)
            stats = calculate_statistics(rate_data)
            
            with col1:
                st.metric("Current Rate", f"{stats['Current']:.2f}%", 
                         f"{stats['Change']:.2f}%" if stats['Change'] else None)
            with col2:
                st.metric("Average", f"{stats['Mean']:.2f}%")
            with col3:
                st.metric("Range", f"{stats['Min']:.2f}% - {stats['Max']:.2f}%")
            
            fig = create_plot(rate_data, "Federal Funds Effective Rate", indicators['Interest Rate']['unit'])
            st.plotly_chart(fig, use_container_width=True)
    
    # Tab 4: Comparison
    with tab4:
        st.header("Comparative Analysis")
        
        cpi_data = fetch_economic_data(indicators['CPI']['id'], start_date, end_date)
        ppi_data = fetch_economic_data(indicators['PPI']['id'], start_date, end_date)
        rate_data = fetch_economic_data(indicators['Interest Rate']['id'], start_date, end_date)
        
        # Normalize data for comparison
        fig = go.Figure()
        
        if cpi_data is not None:
            cpi_norm = (cpi_data - cpi_data.mean()) / cpi_data.std()
            fig.add_trace(go.Scatter(x=cpi_norm.index, y=cpi_norm.values, 
                                     mode='lines', name='CPI (normalized)'))
        
        if ppi_data is not None:
            ppi_norm = (ppi_data - ppi_data.mean()) / ppi_data.std()
            fig.add_trace(go.Scatter(x=ppi_norm.index, y=ppi_norm.values, 
                                     mode='lines', name='PPI (normalized)'))
        
        if rate_data is not None:
            rate_norm = (rate_data - rate_data.mean()) / rate_data.std()
            fig.add_trace(go.Scatter(x=rate_norm.index, y=rate_norm.values, 
                                     mode='lines', name='Interest Rate (normalized)'))
        
        fig.update_layout(
            title='Normalized Comparison of Economic Indicators',
            xaxis_title='Date',
            yaxis_title='Standard Deviations from Mean',
            hovermode='x unified',
            template='plotly_white',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Correlation matrix
        st.subheader("Correlation Analysis")
        df_combined = pd.DataFrame({
            'CPI': cpi_data,
            'PPI': ppi_data,
            'Interest Rate': rate_data
        })
        
        corr_matrix = df_combined.corr()
        
        fig_corr = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.values,
            texttemplate='%{text:.2f}',
            textfont={"size": 16}
        ))
        
        fig_corr.update_layout(
            title='Correlation Matrix',
            height=400
        )
        
        st.plotly_chart(fig_corr, use_container_width=True)
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.info("""
    *Data Source:* Federal Reserve Economic Data (FRED)
    
    *API Key Required:* Get your free key at https://fred.stlouisfed.org/
    
    Set environment variable: FRED_API_KEY
    """)

if _name_ == "_main_":
    main()


# ==============================================================================
# GITHUB REPOSITORY STRUCTURE
# ==============================================================================
"""
Create the following files in your repository:

1. app.py (this file)
2. requirements.txt
3. README.md
4. .gitignore
5. config.toml (for Streamlit configuration)

--- requirements.txt ---
streamlit==1.28.0
pandas==2.1.0
plotly==5.17.0
fredapi==0.5.1

--- README.md ---
# Economic Indicators Dashboard

A real-time dashboard displaying CPI, PPI, and Federal Funds Rate data using FRED API.

## Setup

1. Clone the repository
2. Install dependencies: pip install -r requirements.txt
3. Get a free FRED API key from https://fred.stlouisfed.org/
4. Set environment variable: export FRED_API_KEY=your_key_here
5. Run: streamlit run app.py

## Deployment

Deploy to Streamlit Cloud:
1. Push code to GitHub
2. Go to https://share.streamlit.io/
3. Connect your repository
4. Add FRED_API_KEY to secrets

--- .gitignore ---
_pycache_/
*.py[cod]
*$py.class
.env
.venv
venv/
*.log
.streamlit/secrets.toml

--- .streamlit/config.toml ---
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
"""
