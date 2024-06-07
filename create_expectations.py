# data_validation_tool/create_expectations.py

from great_expectations.core.expectation_suite import ExpectationSuite
from great_expectations.dataset.pandas_dataset import PandasDataset
import pandas as pd


def create_default_expectations(file_path):
    try:
        # Load the CSV file into a Pandas DataFrame
        dataset = pd.read_csv(file_path, delimiter=' ', on_bad_lines='skip')
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

    # Initialize the ExpectationSuite
    suite = ExpectationSuite("default_suite")
    ge_dataset = PandasDataset(dataset, expectation_suite=suite)

    # Iterate through the columns and create expectations based on data types
    for column_name in dataset.columns:
        column_dtype = dataset[column_name].dtype

        # Expect the column to exist
        ge_dataset.expect_column_to_exist(column_name)

        # Create expectations based on data type
        if pd.api.types.is_numeric_dtype(column_dtype):
            ge_dataset.expect_column_values_to_be_in_type_list(column_name, ["int", "float"])
            ge_dataset.expect_column_values_to_be_between(column_name, min_value=0, max_value=100)
            ge_dataset.expect_column_values_to_not_be_null(column_name)
        elif pd.api.types.is_string_dtype(column_dtype):
            ge_dataset.expect_column_values_to_be_in_type_list(column_name, ["object"])
            ge_dataset.expect_column_values_to_not_be_null(column_name)
        elif pd.api.types.is_datetime64_any_dtype(column_dtype):
            ge_dataset.expect_column_values_to_be_in_type_list(column_name, ["datetime64"])
            ge_dataset.expect_column_values_to_not_be_null(column_name)
        else:
            # For other data types, add general expectations if needed
            ge_dataset.expect_column_values_to_not_be_null(column_name)

    return ge_dataset
