from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

import os

# ==========================================================
# VERIFY TRAINING OUTPUT
# ==========================================================

def verify_models():

    required_files = [

        "models/flight_price_model.pkl",
        "models/gender_model.pkl",

        "artifacts/hotel_data.pkl",

        "artifacts/flight_encoders.pkl",
        "artifacts/gender_encoder.pkl",
        "artifacts/company_encoder.pkl",

    ]

    missing = []

    for file in required_files:

        if not os.path.exists(file):

            missing.append(file)

    if missing:

        raise FileNotFoundError(
            f"Missing Files : {missing}"
        )

    print("=" * 60)
    print("All Models Generated Successfully")
    print("=" * 60)


# ==========================================================
# DAG CONFIG
# ==========================================================

default_args = {

    "owner": "Husnain",

    "depends_on_past": False,

    "retries": 1,

    "retry_delay": timedelta(minutes=2)

}

# ==========================================================
# DAG
# ==========================================================

dag = DAG(

    dag_id="Travel_Intelligence_Pipeline",

    default_args=default_args,

    description="Travel Intelligence ML Pipeline",

    start_date=datetime(2026, 1, 1),

    schedule="@daily",

    catchup=False,

    tags=["ML", "Travel", "Production"]

)

# ==========================================================
# TASK 1
# ==========================================================

train_models = BashOperator(

    task_id="Train_All_Models",

    bash_command="python /opt/airflow/dags/train.py",

    dag=dag

)

# ==========================================================
# TASK 2
# ==========================================================

verify_training = PythonOperator(

    task_id="Verify_Artifacts",

    python_callable=verify_models,

    dag=dag

)

# ==========================================================
# PIPELINE
# ==========================================================

train_models >> verify_training