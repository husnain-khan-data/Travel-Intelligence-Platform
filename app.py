# ============================================================
# TRAVEL INTELLIGENCE PLATFORM
# app.py (FINAL)
# PART - 1
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
# FLASK API URL
# ============================================================

API_URL = "http://travel_api:5000"

# ============================================================
# LOAD DATASETS
# ============================================================

flights = pd.read_csv("data/flights.csv")
hotels = pd.read_csv("data/hotels.csv")

# ============================================================
# DROPDOWN VALUES FROM DATASET
# ============================================================

from_cities = sorted(flights["from"].dropna().unique())

to_cities = sorted(flights["to"].dropna().unique())

flight_types = sorted(flights["flightType"].dropna().unique())

agencies = sorted(flights["agency"].dropna().unique())

hotel_places = sorted(hotels["place"].dropna().unique())

# ============================================================
# PAGE TITLE
# ============================================================

st.title("✈️ Travel Intelligence Platform")

st.write(
    "Flight Price Prediction & Hotel Recommendation System"
)

st.markdown("---")

# ============================================================
# CHECK API CONNECTION
# ============================================================

def check_api():

    try:

        response = requests.get(API_URL)

        if response.status_code == 200:

            st.success("✅ Flask API Connected")

            return True

        else:

            st.error("❌ Flask API Error")

            return False

    except Exception:

        st.error("❌ Flask API Not Running")

        return False


api_connected = check_api()

st.markdown("---")

# ============================================================
# FLIGHT PRICE PREDICTION
# PART - 2
# ============================================================

st.header("✈️ Flight Price Prediction")

with st.form("flight_prediction_form"):

    col1, col2 = st.columns(2)

    with col1:

        from_city = st.selectbox(
            "From",
            from_cities
        )

        to_city = st.selectbox(
            "To",
            to_cities
        )

        flight_type = st.selectbox(
            "Flight Type",
            flight_types
        )

    with col2:

        agency = st.selectbox(
            "Agency",
            agencies
        )

        time = st.number_input(
            "Travel Time (Hours)",
            min_value=0.5,
            value=2.0,
            step=0.5
        )

        distance = st.number_input(
            "Distance (KM)",
            min_value=1,
            value=500
        )

    predict_button = st.form_submit_button(
        "Predict Flight Price"
    )

# ============================================================
# FLIGHT API CALL
# ============================================================

if predict_button:

    if api_connected:

        payload = {

            "from": from_city,

            "to": to_city,

            "flightType": flight_type,

            "time": float(time),

            "distance": float(distance),

            "agency": agency

        }

        try:

            response = requests.post(

                f"{API_URL}/predict-flight",

                json=payload

            )

            result = response.json()

            if result.get("success"):

                st.success(

                    f"💰 Predicted Flight Price : ₹ {result['predicted_price']:.2f}"

                )

            else:

                st.error(

                    result.get("error", "Prediction Failed")

                )

        except Exception as e:

            st.error(

                f"Error : {str(e)}"

            )

st.markdown("---")

# ============================================================
# HOTEL RECOMMENDATION
# PART - 3
# ============================================================

st.header("🏨 Hotel Recommendation")

with st.form("hotel_recommendation_form"):

    col1, col2 = st.columns(2)

    with col1:

        place = st.selectbox(
            "Destination",
            hotel_places
        )

        budget = st.number_input(
            "Maximum Budget (₹)",
            min_value=100,
            value=5000,
            step=100
        )

    with col2:

        days = st.number_input(
            "Number of Days",
            min_value=1,
            value=2,
            step=1
        )

    recommend_button = st.form_submit_button(
        "Recommend Hotels"
    )

# ============================================================
# HOTEL API CALL
# ============================================================

if recommend_button:

    if api_connected:

        payload = {

            "place": place,

            "budget": float(budget),

            "days": int(days)

        }

        try:

            response = requests.post(

                f"{API_URL}/recommend-hotels",

                json=payload

            )

            result = response.json()

            if result.get("success"):

                st.success(
                    f"Found {result['total_hotels']} Hotels"
                )

                hotels_df = pd.DataFrame(
                    result["recommendations"]
                )

                if hotels_df.empty:

                    st.warning(
                        "No hotels found for the selected filters."
                    )

                else:

                    st.dataframe(
                        hotels_df,
                        use_container_width=True
                    )

            else:

                st.error(
                    result.get(
                        "error",
                        "Recommendation Failed"
                    )
                )

        except Exception as e:

            st.error(
                f"Error : {str(e)}"
            )

st.markdown("---")
# ============================================================
# FOOTER
# PART - 4
# ============================================================

st.markdown("---")

st.caption("Travel Intelligence Platform")

# ============================================================
# END
# ============================================================
