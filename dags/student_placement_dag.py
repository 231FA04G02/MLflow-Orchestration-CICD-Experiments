# Optional Airflow example. Copy this file into your Airflow dags/ directory.
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="student_placement_ml_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ml", "student-demo"],
) as dag:
    validate_and_train = BashOperator(
        task_id="validate_and_train",
        bash_command="cd $AIRFLOW_HOME/../mlops_experiments && python -m src.pipeline",
    )
