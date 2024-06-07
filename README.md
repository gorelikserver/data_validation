# Data Validation Tool

## Overview

This project is a data validation tool built using Great Expectations to validate datasets (CSV, JSON, Parquet, etc.) stored in Databricks delta tables. The tool loads a dataset, creates default expectations based on the data types of the columns, runs these tests, and generates a validation report.

## Project Structure

```plaintext
data_validation_tool/
├── datasets/
│   ├── example.csv
│   ├── example.json
│   └── example.parquet
├── expectations/
├── reports/
├── create_expectations.py
├── run_tests.py
├── main.py
├── README.md
└── requirements.txt
