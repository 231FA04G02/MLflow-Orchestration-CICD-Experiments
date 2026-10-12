# MLflow → ML Pipeline → Orchestration → CI/CD Lab

**Dataset:** `student_placement.csv` (400 synthetic student records; not real student data).  
**Goal:** predict a sample placement outcome from CGPA, coding score, aptitude score, number of projects, and internships.

## Experiments covered
1. Dataset inspection and validation
2. Scikit-learn preprocessing + Logistic Regression pipeline
3. MLflow parameter, metric, and model tracking
4. Pipeline orchestration with Prefect (optional)
5. Example Apache Airflow DAG (optional; requires a configured Airflow installation)
6. CI with GitHub Actions: install dependencies, run tests, and execute the training pipeline

## Setup (Python 3.10/3.11 recommended)
Open a terminal in this project folder:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python -m src.pipeline
```

The run creates `artifacts/placement_model.joblib`, `artifacts/metrics.json`, and local MLflow run data in `mlruns/`.

## View MLflow results
After one successful training run:

```bash
mlflow ui --backend-store-uri ./mlruns --host 127.0.0.1 --port 5000
```
Open `http://127.0.0.1:5000`, choose experiment `student-placement`, and inspect run parameters, metrics, and model artifacts.

## Run the orchestrated pipeline
Prefect example (install requirements first):
```bash
python -m src.orchestrate_prefect
```
The task/flow run is orchestrated by Prefect. For a UI, Prefect's local server/work-pool setup may vary by Prefect version.

Airflow is an **optional example**, not automatically configured. Put `dags/student_placement_dag.py` in a working Airflow deployment's DAG folder, and adjust the `bash_command` to your project path/environment. Airflow is most straightforward on Linux/WSL or Docker.

## CI/CD workflow
1. Create a GitHub repository and push this project to the `main` branch.
2. GitHub Actions automatically installs requirements, runs `pytest`, and runs the ML pipeline.
3. See **GitHub → Actions → ML CI** for the logs.
4. This demo implements CI and automated model training. It does **not** automatically deploy a model to production; deployment would need a target platform and credentials.

Example Git commands:
```bash
git init
git add .
git commit -m "Complete MLflow and ML pipeline experiments"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

## Experiment record to write in your lab notebook
- **Aim:** Build and track a reproducible ML pipeline and automate checks.
- **Algorithm:** Logistic Regression.
- **Split:** 80% train / 20% test; fixed random seed 42; stratified split.
- **Input features:** cgpa, coding_score, aptitude_score, projects, internships.
- **Target:** placed (0 = not placed, 1 = placed).
- **Metrics:** accuracy, precision, recall, F1, ROC-AUC. Actual values are generated when you run the code and are saved to `artifacts/metrics.json`.
- **Result:** Record the metrics from your own execution; do not copy invented values.

## Important notes
- The data is synthetic for learning only and does not represent real placement outcomes.
- This bundle is a working starter project, but you must install dependencies and execute it in your environment. Capture your own screenshots and be ready to explain each step.
- Exact orchestration tool requirements may differ from the tools demonstrated by your instructor.
