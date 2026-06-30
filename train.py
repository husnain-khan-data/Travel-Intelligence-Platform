# ==========================================================
# Travel Intelligence Platform
# train.py (FINAL)
# PART - 1
# ==========================================================

import os
import warnings
warnings.filterwarnings("ignore")

import joblib
import mlflow
import mlflow.sklearn

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

# ==========================================================
# CREATE REQUIRED FOLDERS
# ==========================================================

os.makedirs("models", exist_ok=True)
os.makedirs("artifacts", exist_ok=True)
os.makedirs("mlruns", exist_ok=True)

# ==========================================================
# MLFLOW CONFIGURATION
# ==========================================================

mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("Travel_Intelligence_Project")

# ==========================================================
# LOAD DATASETS
# ==========================================================

print("=" * 60)
print("Loading Datasets...")
print("=" * 60)

flights = pd.read_csv("data/flights.csv")
users = pd.read_csv("data/users.csv")
hotels = pd.read_csv("data/hotels.csv")

print("\nFlights Dataset :", flights.shape)
print("Users Dataset   :", users.shape)
print("Hotels Dataset  :", hotels.shape)

# ==========================================================
# BASIC DATA CLEANING
# ==========================================================

flights.drop_duplicates(inplace=True)
users.drop_duplicates(inplace=True)
hotels.drop_duplicates(inplace=True)

flights.dropna(inplace=True)
users.dropna(inplace=True)
hotels.dropna(inplace=True)

# ==========================================================
# DATE COLUMN HANDLING
# ==========================================================

if "date" in flights.columns:
    flights["date"] = pd.to_datetime(
        flights["date"],
        errors="coerce"
    )

if "date" in hotels.columns:
    hotels["date"] = pd.to_datetime(
        hotels["date"],
        errors="coerce"
    )

# ==========================================================
# LABEL ENCODING
# ==========================================================

flight_encoders = {}

flight_columns = [
    "from",
    "to",
    "flightType",
    "agency"
]

for column in flight_columns:

    encoder = LabelEncoder()

    flights[column] = encoder.fit_transform(
        flights[column]
    )

    flight_encoders[column] = encoder

company_encoder = LabelEncoder()
gender_encoder = LabelEncoder()

users["company"] = company_encoder.fit_transform(
    users["company"]
)

users["gender"] = gender_encoder.fit_transform(
    users["gender"]
)

hotel_name_encoder = LabelEncoder()
hotel_place_encoder = LabelEncoder()

hotels["name"] = hotel_name_encoder.fit_transform(
    hotels["name"]
)

hotels["place"] = hotel_place_encoder.fit_transform(
    hotels["place"]
)

print("\nData Cleaning & Encoding Completed Successfully.\n")
# ==========================================================
# FLIGHT PRICE PREDICTION MODEL
# ==========================================================

print("=" * 60)
print("Training Flight Price Prediction Model...")
print("=" * 60)

# Features and Target
flight_features = [
    "from",
    "to",
    "flightType",
    "time",
    "distance",
    "agency"
]

X_flight = flights[flight_features]
y_flight = flights["price"]

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X_flight,
    y_flight,
    test_size=0.20,
    random_state=42
)

# Model
flight_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

# ===========================
# MLFLOW
# ===========================

with mlflow.start_run(run_name="Flight_Price_Model"):

    flight_model.fit(X_train, y_train)

    predictions = flight_model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions)

    print("\nFlight Model Performance")
    print("-" * 40)
    print(f"MAE  : {mae:.2f}")
    print(f"MSE  : {mse:.2f}")
    print(f"RMSE : {rmse:.2f}")
    print(f"R²   : {r2:.4f}")

    mlflow.log_param("Algorithm", "RandomForestRegressor")
    mlflow.log_param("n_estimators", 100)

    mlflow.log_metric("MAE", mae)
    mlflow.log_metric("MSE", mse)
    mlflow.log_metric("RMSE", rmse)
    mlflow.log_metric("R2_Score", r2)

    mlflow.sklearn.log_model(
        flight_model,
        artifact_path="flight_price_model"
    )

# ==========================================================
# SAVE FLIGHT MODEL
# ==========================================================

joblib.dump(
    flight_model,
    "models/flight_price_model.pkl"
)

joblib.dump(
    flight_encoders,
    "artifacts/flight_encoders.pkl"
)

joblib.dump(
    flight_features,
    "artifacts/flight_features.pkl"
)

print("\nFlight Price Model Saved Successfully.\n")
# ==========================================================
# GENDER CLASSIFICATION MODEL
# ==========================================================

print("=" * 60)
print("Training Gender Classification Model...")
print("=" * 60)

# Features and Target

gender_features = [
    "company",
    "age"
]

X_gender = users[gender_features]
y_gender = users["gender"]

# Train Test Split

X_train_gender, X_test_gender, y_train_gender, y_test_gender = train_test_split(
    X_gender,
    y_gender,
    test_size=0.20,
    random_state=42
)

# Model

gender_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

# ===========================
# MLFLOW
# ===========================

with mlflow.start_run(run_name="Gender_Classification_Model"):

    gender_model.fit(
        X_train_gender,
        y_train_gender
    )

    gender_predictions = gender_model.predict(
        X_test_gender
    )

    accuracy = accuracy_score(
        y_test_gender,
        gender_predictions
    )

    precision = precision_score(
        y_test_gender,
        gender_predictions,
        average="weighted"
    )

    recall = recall_score(
        y_test_gender,
        gender_predictions,
        average="weighted"
    )

    f1 = f1_score(
        y_test_gender,
        gender_predictions,
        average="weighted"
    )

    print("\nGender Model Performance")
    print("-" * 40)
    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")

    mlflow.log_param(
        "Algorithm",
        "RandomForestClassifier"
    )

    mlflow.log_param(
        "n_estimators",
        100
    )

    mlflow.log_metric(
        "Accuracy",
        accuracy
    )

    mlflow.log_metric(
        "Precision",
        precision
    )

    mlflow.log_metric(
        "Recall",
        recall
    )

    mlflow.log_metric(
        "F1_Score",
        f1
    )

    mlflow.sklearn.log_model(
        gender_model,
        artifact_path="gender_classification_model"
    )

# ==========================================================
# SAVE GENDER MODEL
# ==========================================================

joblib.dump(
    gender_model,
    "models/gender_model.pkl"
)

joblib.dump(
    company_encoder,
    "artifacts/company_encoder.pkl"
)

joblib.dump(
    gender_encoder,
    "artifacts/gender_encoder.pkl"
)

joblib.dump(
    gender_features,
    "artifacts/gender_features.pkl"
)

print("\nGender Classification Model Saved Successfully.\n")

# ==========================================================
# HOTEL RECOMMENDATION DATA PREPARATION
# ==========================================================

print("=" * 60)
print("Preparing Hotel Recommendation Data...")
print("=" * 60)

hotel_data = hotels.copy()

hotel_data = hotel_data.sort_values(
    by=["place", "price"]
)

hotel_data.reset_index(
    drop=True,
    inplace=True
)

joblib.dump(
    hotel_data,
    "artifacts/hotel_data.pkl"
)

joblib.dump(
    hotel_place_encoder,
    "artifacts/hotel_place_encoder.pkl"
)

joblib.dump(
    hotel_name_encoder,
    "artifacts/hotel_name_encoder.pkl"
)

print("\nHotel Recommendation Data Saved Successfully.\n")
# ==========================================================
# TRAINING COMPLETED
# ==========================================================

print("=" * 60)
print("Saving Final Artifacts...")
print("=" * 60)

# Save Encoders

joblib.dump(
    flight_encoders,
    "artifacts/flight_encoders.pkl"
)

joblib.dump(
    company_encoder,
    "artifacts/company_encoder.pkl"
)

joblib.dump(
    gender_encoder,
    "artifacts/gender_encoder.pkl"
)

joblib.dump(
    hotel_name_encoder,
    "artifacts/hotel_name_encoder.pkl"
)

joblib.dump(
    hotel_place_encoder,
    "artifacts/hotel_place_encoder.pkl"
)

# Save Feature Names

joblib.dump(
    flight_features,
    "artifacts/flight_features.pkl"
)

joblib.dump(
    gender_features,
    "artifacts/gender_features.pkl"
)

print("\nAll Artifacts Saved Successfully.")

# ==========================================================
# FINAL SUMMARY
# ==========================================================

print("\n" + "=" * 60)
print("TRAVEL INTELLIGENCE PLATFORM")
print("=" * 60)

print("Flight Price Prediction Model   : Completed")
print("Gender Classification Model     : Completed")
print("Hotel Recommendation Data       : Completed")

print("\nModels Saved Inside:")
print("models/")

print("\nArtifacts Saved Inside:")
print("artifacts/")

print("\nMLflow Tracking:")
print("mlruns/")

print("\nTraining Completed Successfully.")
print("=" * 60)