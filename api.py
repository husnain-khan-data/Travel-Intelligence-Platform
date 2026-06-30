# ==========================================================
# Travel Intelligence Platform
# api.py (FINAL)
# PART - 1
# ==========================================================

from flask import Flask, request, jsonify
import joblib
import pandas as pd

# ==========================================================
# CREATE FLASK APP
# ==========================================================

app = Flask(__name__)

# ==========================================================
# LOAD TRAINED MODELS
# ==========================================================

print("=" * 60)
print("Loading Models...")
print("=" * 60)

flight_model = joblib.load(
    "models/flight_price_model.pkl"
)

gender_model = joblib.load(
    "models/gender_model.pkl"
)

# ==========================================================
# LOAD ARTIFACTS
# ==========================================================

flight_encoders = joblib.load(
    "artifacts/flight_encoders.pkl"
)

flight_features = joblib.load(
    "artifacts/flight_features.pkl"
)

hotel_data = joblib.load(
    "artifacts/hotel_data.pkl"
)

hotel_place_encoder = joblib.load(
    "artifacts/hotel_place_encoder.pkl"
)

hotel_name_encoder = joblib.load(
    "artifacts/hotel_name_encoder.pkl"
)

print("Models Loaded Successfully.")
print("Artifacts Loaded Successfully.\n")

# ==========================================================
# HOME ROUTE
# ==========================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({

        "message": "Travel Intelligence Platform API",

        "status": "Running Successfully"

    })

# ==========================================================
# FLIGHT PRICE PREDICTION API
# ==========================================================

@app.route("/predict-flight", methods=["POST"])
def predict_flight():

    try:

        data = request.get_json()

        # ---------------------------------------------
        # Encode Categorical Features
        # ---------------------------------------------

        from_city = flight_encoders["from"].transform(
            [data["from"]]
        )[0]

        to_city = flight_encoders["to"].transform(
            [data["to"]]
        )[0]

        flight_type = flight_encoders["flightType"].transform(
            [data["flightType"]]
        )[0]

        agency = flight_encoders["agency"].transform(
            [data["agency"]]
        )[0]

        # ---------------------------------------------
        # Create Input DataFrame
        # ---------------------------------------------

        input_data = pd.DataFrame({

            "from": [from_city],

            "to": [to_city],

            "flightType": [flight_type],

            "time": [float(data["time"])],

            "distance": [float(data["distance"])],

            "agency": [agency]

        })

        # Arrange columns in same order as training

        input_data = input_data[flight_features]

        # ---------------------------------------------
        # Prediction
        # ---------------------------------------------

        prediction = flight_model.predict(input_data)[0]

        return jsonify({

            "success": True,

            "predicted_price": round(float(prediction), 2)

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        })
    

# ==========================================================
# HOTEL RECOMMENDATION API
# ==========================================================

@app.route("/recommend-hotels", methods=["POST"])
def recommend_hotels():

    try:

        data = request.get_json()

        place = data["place"]
        max_price = float(data["budget"])
        days = int(data["days"])

        # ---------------------------------------------
        # Encode Place
        # ---------------------------------------------

        encoded_place = hotel_place_encoder.transform(
            [place]
        )[0]

        # ---------------------------------------------
        # Filter Hotels
        # ---------------------------------------------

        recommended_hotels = hotel_data[
            (hotel_data["place"] == encoded_place)
            &
            (hotel_data["price"] <= max_price)
        ].copy()

        # ---------------------------------------------
        # Total Cost
        # ---------------------------------------------

        recommended_hotels["total_cost"] = (
            recommended_hotels["price"] * days
        )

        # ---------------------------------------------
        # Decode Hotel Names
        # ---------------------------------------------

        recommended_hotels["name"] = hotel_name_encoder.inverse_transform(
            recommended_hotels["name"]
        )

        recommended_hotels["place"] = hotel_place_encoder.inverse_transform(
            recommended_hotels["place"]
        )

        # ---------------------------------------------
        # Sort Hotels
        # ---------------------------------------------

        recommended_hotels = recommended_hotels.sort_values(
            by="price"
        )
        # Remove Duplicate Hotel Names
        recommended_hotels = recommended_hotels.drop_duplicates(
            subset=["name"],keep="first")

        # ---------------------------------------------
        # Return Top 10 Hotels
        # ---------------------------------------------

        result = recommended_hotels[
            [
                "name",
                "place",
                "price",
                "days",
                "total_cost"
            ]
        ].head(5)

        return jsonify({

            "success": True,

            "total_hotels": len(result),

            "recommendations": result.to_dict(
                orient="records"
            )

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        })
    

# ==========================================================
# RUN FLASK APPLICATION
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Travel Intelligence Platform API Started")
    print("=" * 60)

    print("\nAvailable Endpoints:\n")

    print("GET  : http://127.0.0.1:5000/")

    print("POST : http://127.0.0.1:5000/predict-flight")

    print("POST : http://127.0.0.1:5000/recommend-hotels")

    print("\nServer Running...\n")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )