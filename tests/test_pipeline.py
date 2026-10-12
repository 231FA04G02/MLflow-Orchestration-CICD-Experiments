from src.pipeline import validate_data
from src.train import DATA

def test_dataset_validation():
    assert validate_data(DATA) is True
