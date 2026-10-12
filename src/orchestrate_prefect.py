
from src.pipeline import validate_data
from src.train import train


def run_pipeline():
    print("Step 1: Validating dataset...")
    validate_data()

    print("\nStep 2: Training model...")
    metrics = train()

    print("\nPipeline completed successfully!")
    print("Metrics:", metrics)


if __name__ == "__main__":
    run_pipeline()
