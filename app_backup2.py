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
# FLASK API URL
# ============================================================

API_URL = "http://127.0.0.1:5000"

# ============================================================
# PAGE TITLE
# ============================================================

st.title("✈️ Travel Intelligence Platform")

st.markdown("---")

st.write(
    """
Welcome to the **Travel Intelligence Platform**.

This application provides:

- ✈️ Flight Price Prediction
- 🏨 Hotel Recommendation
"""
)

# ============================================================
# CHECK FLASK API
# ============================================================

def check_api():

    try:

        response = requests.get(API_URL)

        if response.status_code == 200:

            st.success("✅ Flask API Connected")

            return True

        else:

            st.error("❌ API Running But Returned Error")

            return False

    except:

        st.error("❌ Flask API Not Running")

        return False


api_connected = check_api()

st.markdown("---")
# ============================================================
# FLIGHT PRICE PREDICTION
# ============================================================

st.header("✈️ Flight Price Prediction")

with st.form("flight_prediction_form"):

    col1, col2 = st.columns(2)

    with col1:

        from_city = st.text_input(
            "From City"
        )

        to_city = st.text_input(
            "To City"
        )

        flight_type = st.selectbox(

            "Flight Type",

            [

                "Economic",

                "Premium"

            ]

        )

    with col2:

        time = st.number_input(

            "Flight Time (Hours)",

            min_value=1.0,

            value=2.0

        )

        distance = st.number_input(

            "Distance (KM)",

            min_value=1,

            value=500

        )

        agency = st.text_input(

            "Agency"

        )

    predict_button = st.form_submit_button(

        "Predict Flight Price"

    )

# ============================================================
# CALL FLASK API
# ============================================================

if predict_button:

    if api_connected:

        payload = {

            "from": from_city,

            "to": to_city,

            "flightType": flight_type,

            "time": time,

            "distance": distance,

            "agency": agency

        }

        try:

            response = requests.post(

                f"{API_URL}/predict-flight",

                json=payload

            )

            result = response.json()

            if result["success"]:

                st.success(

                    f"Predicted Flight Price : ₹ {result['predicted_price']:.2f}"

                )

            else:

                st.error(

                    result["error"]

                )

        except Exception as e:

            st.error(

                str(e)

            )

st.markdown("---")
# ============================================================
# HOTEL RECOMMENDATION
# ============================================================

st.header("🏨 Hotel Recommendation")

with st.form("hotel_recommendation_form"):

    place = st.text_input(
        "Destination"
    )

    budget = st.number_input(
        "Maximum Budget (₹)",
        min_value=500,
        value=5000
    )

    days = st.number_input(
        "Number of Days",
        min_value=1,
        value=2
    )

    recommend_button = st.form_submit_button(
        "Recommend Hotels"
    )

# ============================================================
# CALL HOTEL API
# ============================================================

if recommend_button:

    if api_connected:

        payload = {

            "place": place,

            "budget": budget,

            "days": days

        }

        try:

            response = requests.post(

                f"{API_URL}/recommend-hotels",

                json=payload

            )

            result = response.json()

            if result["success"]:

                st.success(

                    f"{result['total_hotels']} Hotels Found"

                )

                st.dataframe(

                    pd.DataFrame(

                        result["recommendations"]

                    ),

                    use_container_width=True

                )

            else:

                st.error(

                    result["error"]

                )

        except Exception as e:

            st.error(

                str(e)

            )

st.markdown("---")
# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption("Travel Intelligence Platform")

# ============================================================
# END
# ============================================================