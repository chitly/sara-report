import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import io

# Page config
st.set_page_config(
    page_title="SaRa Report",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 SaRa Report")
st.markdown("View and download report data by date")

# Date picker
st.subheader("Select Date")
selected_date = st.date_input(
    "Choose Date",
    datetime.now(),
    key="date_picker"
)

# API endpoint configuration
API_URL = "YOUR_API_ENDPOINT_HERE"  # Replace with your actual API endpoint

def fetch_report_data(date):
    """
    Fetch report data from API for specific date
    """
    try:
        params = {
            'date': date.strftime('%Y-%m-%d')
        }
        
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        
        # Assuming API returns JSON data
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

# Fetch button
if st.button("Fetch Data"):
    with st.spinner("Fetching data..."):
        # For demonstration, using sample data
        # Replace this with actual API call in production
        sample_data = {
            'data': [
                {'timestamp': '2024-01-01 09:00:00', 'revenue': 100, 'orders': 5},
                {'timestamp': '2024-01-01 10:00:00', 'revenue': 150, 'orders': 7},
                {'timestamp': '2024-01-01 11:00:00', 'revenue': 200, 'orders': 10},
                {'timestamp': '2024-01-01 12:00:00', 'revenue': 180, 'orders': 8},
                # Add more sample data as needed
            ]
        }
        
        # In production, use:
        # data = fetch_report_data(selected_date)
        data = sample_data
        
        if data:
            # Convert to DataFrame
            df = pd.DataFrame(data['data'])
            
            # Format timestamp column
            df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%H:%M:%S')
            
            # Display data table
            st.subheader(f"Report Data for {selected_date.strftime('%B %d, %Y')}")
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )
            
            # Download button
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"report_data_{selected_date}.csv",
                mime="text/csv",
                key="download_button"
            )
            
            # Summary statistics
            st.subheader("Daily Summary")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total Orders", df['orders'].sum())
            
            with col2:
                st.metric("Total Revenue", f"${df['revenue'].sum():,.2f}")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit ❤️")