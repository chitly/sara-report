import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Page config
st.set_page_config(
    page_title="SaRa Report (v.1.1.0)",
    page_icon="📊",
    layout="wide"
)

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'app_key' not in st.session_state:
    st.session_state.app_key = None

# Title
st.title("📊 SaRa Report (v.1.1.0)")

# API endpoint configuration
API_URL = "https://meetsum.scg-wedo.tech/api/report"


def check_api_access(app_key):
    """
    Test API access with the provided app key
    """
    try:
        headers = {
            'app-key': app_key
        }
        # Use current date for test request
        today = datetime.now()
        params = {
            'from': today.strftime('%Y-%m-%d 23:59:59'),
            'to': today.strftime('%Y-%m-%d 23:59:59')
        }

        response = requests.get(API_URL, params=params, headers=headers)
        return response.status_code == 200
    except:
        return False


# Authentication section
if not st.session_state.authenticated:
    st.markdown("Please enter your password to access the report")
    app_key = st.text_input("Password", type="password")

    if st.button("Login"):
        if check_api_access(app_key):
            st.session_state.authenticated = True
            st.session_state.app_key = app_key
            st.success("Authentication successful!")
            st.rerun()
        else:
            st.error("Invalid password")

    st.stop()  # Stop here if not authenticated

# Main dashboard content (only shown when authenticated)
st.markdown("View and download report data by date")

# Date picker
st.subheader("Select Date")
selected_date = st.date_input(
    "Choose Date",
    datetime.now(),
    key="date_picker"
)


def fetch_report_data(date):
    """
    Fetch report data from API for specific date
    """
    try:
        headers = {
            'app-key': st.session_state.app_key
        }
        params = {
            'from': date.strftime('%Y-%m-%d 00:00:00'),
            'to': date.strftime('%Y-%m-%d 23:59:59')
        }

        response = requests.get(API_URL, params=params, headers=headers)
        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {str(e)}")
        return None


# Add logout button in sidebar
with st.sidebar:
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.app_key = None
        st.rerun()

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
