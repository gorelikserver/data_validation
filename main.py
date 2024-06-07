# data_validation_tool/main.py

from create_expectations import create_default_expectations
from run_tests import run_tests
import os


def main(file_name):
    # Specify the folder where datasets are stored
    folder_path = "datasets"

    # Construct the full file path
    file_path = os.path.join(folder_path, file_name)

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    # Create expectations and run tests
    ge_dataset = create_default_expectations(file_path)
    if ge_dataset is not None:
        results = run_tests(ge_dataset)
        print(results)
    else:
        print("Failed to create expectations due to errors in loading the dataset.")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python main.py <dataset_file_name>")
        sys.exit(1)
    file_name = sys.argv[1]
    main(file_name)
