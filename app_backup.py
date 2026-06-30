# ============================================================
# TRAVEL INTELLIGENCE PLATFORM
# Streamlit Frontend
# PART 1
# ============================================================

import streamlit as st
import requests
import pandas as pd

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Travel Intelligence Platform",
    page_icon="✈️",
    layout="wide"
)

# ============================================================
# API URL
# ============================================================

API_URL = "http://127.0.0.1:5000"

# ============================================================
# PAGE TITLE
# ============================================================

st.title("✈️ Travel Intelligence Platform")

st.markdown("---")

st.write(
    """
Welcome to the Travel Intelligence Platform.

This application provides:

✅ Flight Price Prediction

✅ Hotel Recommendation

Powered by:
- Streamlit
- Flask API
- Machine Learning
"""
)

st.markdown("---")

# ============================================================
# HELPER FUNCTION
# ============================================================

def check_api():

    try:

        response = requests.get(API_URL)

        if response.status_code == 200:

            st.success("✅ Flask API Connected")

            return True

        else:

            st.error("API Returned Error")

            return False

    except:

        st.error("❌ Flask API Not Running")

        return False


api_connected = check_api()

st.markdown("---")

# ============================================================
# FLIGHT PRICE PREDICTION
# PART 2
# ============================================================

st.header("✈️ Flight Price Prediction")

with st.form("flight_form"):

    col1, col2 = st.columns(2)

    with col1:

        source = st.selectbox(
            "Source City",
            [
                "Delhi",
                "Mumbai",
                "Bangalore",
                "Chennai",
                "Hyderabad",
                "Kolkata"
            ]
        )

        destination = st.selectbox(
            "Destination City",
            [
                "Delhi",
                "Mumbai",
                "Bangalore",
                "Chennai",
                "Hyderabad",
                "Kolkata"
            ]
        )

        airline = st.selectbox(
            "Airline",
            [
                "Indigo",
                "Air India",
                "SpiceJet",
                "Vistara",
                "GO FIRST"
            ]
        )

    with col2:

        stops = st.selectbox(
            "Stops",
            [
                0,
                1,
                2
            ]
        )

        duration = st.number_input(
            "Duration (Hours)",
            min_value=1.0,
            max_value=30.0,
            value=2.0
        )

        days_left = st.slider(
            "Days Left",
            1,
            60,
            10
        )

    predict_btn = st.form_submit_button("Predict Flight Price")

# ============================================================
# CALL FLASK API
# ============================================================

if predict_btn:

    if api_connected:

        payload = {

            "source_city": source,
            "destination_city": destination,
            "airline": airline,
            "stops": stops,
            "duration": duration,
            "days_left": days_left

        }

        try:

            response = requests.post(
                f"{API_URL}/predict-flight",
                json=payload
            )

            result = response.json()

            st.success(
                f"Predicted Flight Price : ₹ {result['predicted_price']:.2f}"
            )

        except Exception as e:

            st.error(str(e))

st.markdown("---")

# ============================================================
# HOTEL RECOMMENDATION
# PART 3
# ============================================================

st.header("🏨 Hotel Recommendation System")

with st.form("hotel_form"):

    city = st.selectbox(
        "Select City",
        [
            "Delhi",
            "Mumbai",
            "Bangalore",
            "Hyderabad",
            "Chennai",
            "Kolkata"
        ]
    )

    hotel_type = st.selectbox(
        "Hotel Type",
        [
            "Budget",
            "Standard",
            "Premium",
            "Luxury"
        ]
    )

    max_price = st.number_input(
        "Maximum Budget (₹)",
        min_value=1000,
        max_value=50000,
        value=5000
    )

    rating = st.slider(
        "Minimum Rating",
        1.0,
        5.0,
        4.0,
        0.5
    )

    recommend_btn = st.form_submit_button("Recommend Hotels")

# ============================================================
# CALL HOTEL API
# ============================================================

if recommend_btn:

    if api_connected:

        payload = {

            "city": city,
            "hotel_type": hotel_type,
            "budget": max_price,
            "rating": rating

        }

        try:

            response = requests.post(
                f"{API_URL}/recommend-hotels",
                json=payload
            )

            hotels = response.json()["recommended_hotels"]

            st.success("Top Recommended Hotels")

            st.dataframe(hotels)

        except Exception as e:

            st.error(str(e))

st.markdown("---")
# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    ### 📌 About This Project

    **Travel Intelligence Platform**

    This project demonstrates an end-to-end Machine Learning application.

    ✔ Flight Price Prediction

    ✔ Hotel Recommendation

    ✔ Flask REST API

    ✔ Streamlit Frontend

    ✔ MLflow Integration

    ✔ Docker Ready

    """
)

# ============================================================
# SIDEBAR INFO
# ============================================================

st.sidebar.markdown("---")

st.sidebar.subheader("Project Status")

st.sidebar.success("Backend Connected" if api_connected else "Backend Offline")

st.sidebar.write("Python : 3.11")

st.sidebar.write("Framework : Streamlit")

st.sidebar.write("API : Flask")

st.sidebar.write("ML Models : Scikit-Learn")

st.sidebar.write("Tracking : MLflow")

st.sidebar.write("Deployment : Docker")

# ============================================================
# END
# ============================================================