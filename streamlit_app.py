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
API_URL = "https://meetsum.scg-wedo.tech/report"


def fetch_report_data(date):
    """
    Fetch report data from API for specific date
    """
    try:
        headers = {
            'app-key': 'botv'
        }
        params = {
            'from': date.strftime('%Y-%m-%d 00:00:00'),
            'to': date.strftime('%Y-%m-%d 23:59:59')
        }

        response = requests.get(API_URL, params=params, headers=headers)
        response.raise_for_status()

        # Assuming API returns JSON data
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {str(e)}")
        return None


# Fetch button
if st.button("Fetch Data"):
    with st.spinner("Fetching data..."):
        data = fetch_report_data(selected_date)

        if data:
            try:
                # Convert to DataFrame
                df = pd.DataFrame(data)

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

                # Display total number of records
                st.info(f"Total records: {len(df)}")

            except Exception as e:
                st.error(f"Error processing data: {str(e)}")
                if data:
                    st.json(data)  # Display raw JSON for debugging

# Footer
st.markdown("---")
st.markdown("Built with Nattapong Ousirimaneechai ❤️")
