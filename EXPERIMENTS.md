# Practical record: experiments and viva notes

## 1. MLflow
**Aim:** Track model parameters, metrics, and artifacts.
**Procedure:** Run `python -m src.pipeline`; then `mlflow ui --backend-store-uri ./mlruns`.
**Observe:** experiment name, run ID, logged parameters, evaluation metrics, model artifact.
**Viva:** MLflow Tracking records parameters, code versions, metrics, and artifacts to compare runs.

## 2. Data validation
**Aim:** Catch missing columns, empty data, or invalid target values before training.
**Procedure:** `python -c "from src.pipeline import validate_data; validate_data()"`.
**Expected:** validation passed message.

## 3. ML pipeline
**Aim:** Combine preprocessing and model training into a repeatable sklearn Pipeline.
**Procedure:** `python -m src.pipeline`.
**Stages:** read/validate data → split → impute/scale → fit classifier → evaluate → save/log model.

## 4. Notebook-to-pipeline conversion
Move notebook cells into reusable functions (`validate_data`, `build_pipeline`, `train`) in `src/`. The command-line entry point makes execution repeatable.

## 5. Orchestration
**Prefect:** `python -m src.orchestrate_prefect`. Flow connects validation and training tasks and defines retry behavior.
**Airflow alternative:** `dags/student_placement_dag.py` is an example DAG. It requires a configured Airflow environment and path adjustment.

## 6. CI/CD
**Aim:** Automatically test code and run the ML pipeline on pushes and pull requests.
**Procedure:** Push to GitHub `main`; inspect Actions workflow. Tests run before training.
**Scope:** CI and automated training are included. Production CD/deployment is not configured because no deployment target was specified.

## Common viva questions
1. **What is MLflow?** An open-source platform for tracking ML experiments and managing model artifacts/lifecycle.
2. **What is a parameter vs metric?** Parameters are chosen settings; metrics measure model performance.
3. **What is an ML pipeline?** A connected sequence of data preparation, training, and evaluation steps.
4. **Why split data?** To estimate performance on unseen examples.
5. **What is orchestration?** Scheduling, ordering, retrying, and monitoring pipeline tasks.
6. **Prefect vs Airflow?** Both orchestrate workflows; they differ in APIs, deployment model, and operational setup.
7. **What is CI?** Automated checks when code changes.
8. **What is CD?** Automated delivery/deployment after checks; deployment is not configured in this demo.
9. **Why use a fixed random state?** To make data splitting reproducible.
10. **Why use precision and recall?** Accuracy alone can hide class imbalance; precision and recall describe different error trade-offs.
