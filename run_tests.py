# data_validation_tool/run_tests.py

import great_expectations as gx
from great_expectations.data_context import get_context
from great_expectations.data_context.types.base import DataContextConfig
from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.exceptions import DataContextError
import os

def run_tests(ge_dataset):
    context_config = DataContextConfig(
        config_version=2,
        datasources={
            "my_pandas_datasource": {
                "class_name": "Datasource",
                "execution_engine": {
                    "class_name": "PandasExecutionEngine"
                },
                "data_connectors": {
                    "default_runtime_data_connector_name": {
                        "class_name": "RuntimeDataConnector",
                        "batch_identifiers": ["default_identifier_name"]
                    }
                }
            }
        },
        stores={
            "expectations_store": {
                "class_name": "ExpectationsStore"
            },
            "validations_store": {
                "class_name": "ValidationsStore"
            },
            "evaluation_parameter_store": {
                "class_name": "EvaluationParameterStore"
            },
            "checkpoint_store": {
                "class_name": "CheckpointStore"
            }
        },
        expectations_store_name="expectations_store",
        validations_store_name="validations_store",
        evaluation_parameter_store_name="evaluation_parameter_store",
        checkpoint_store_name="checkpoint_store",
        data_docs_sites={
            "local_site": {
                "class_name": "SiteBuilder",
                "show_how_to_buttons": True,
                "store_backend": {
                    "class_name": "TupleFilesystemStoreBackend",
                    "base_directory": os.path.abspath("reports/")
                },
                "site_index_builder": {
                    "class_name": "DefaultSiteIndexBuilder"
                }
            }
        },
    )

    # Create a DataContext from the configuration
    context = gx.get_context(project_config=context_config)

    # Save the expectation suite to the context
    suite = ge_dataset._expectation_suite
    context.save_expectation_suite(expectation_suite=suite)

    # Create a RuntimeBatchRequest for validation
    batch_request = RuntimeBatchRequest(
        datasource_name="my_pandas_datasource",
        data_connector_name="default_runtime_data_connector_name",
        data_asset_name="default_data_asset_name",
        runtime_parameters={"batch_data": ge_dataset},
        batch_identifiers={"default_identifier_name": "default_identifier"}
    )

    try:
        # Get a Validator
        validator = context.get_validator(
            batch_request=batch_request,
            expectation_suite_name=suite.expectation_suite_name
        )
    except DataContextError as e:
        print(f"Error: {e}")
        return

    # Run validation
    results = validator.validate()

    # Build and open data docs
    context.build_data_docs()
    context.open_data_docs()

    return results
