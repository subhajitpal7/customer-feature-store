# Customer Feature Store: Intelligent Customer Insights Platform

## 🚀 Project Overview

The Customer Feature Store is a simple data management solution for organizing and serving customer-related features. Built using Feast, it helps teams centralize feature computation and make machine learning workflows more consistent and efficient.

### 🌟 Key Objectives

- **Unified Feature Management**: Centralize customer feature computation and storage
- **Real-time Feature Serving**: Enable sub-millisecond feature retrieval for ML models
- **Data Consistency**: Ensure feature consistency across training and inference
- **Scalable Architecture**: Support growing data volumes and complex feature definitions

### 💡 Core Capabilities

- Seamless offline and online feature storage
- Incremental feature materialization
- Flexible feature retrieval mechanisms
- Robust CLI for feature management
- Easy integration with machine learning workflows

## Project Background

In today's data-driven landscape, organizations struggle with fragmented customer data and inconsistent feature engineering. This feature store addresses these challenges by providing a robust, scalable solution for managing customer features across the entire machine learning lifecycle.

## Features

## Project Structure

```
customer_feature_store/
│
├── src/
│   └── customer_feature_store/
│       ├── core/               # Core feature definitions
│       ├── service/             # Feature service implementation
│       └── cli/                 # Command-line interface
│
├── feature_repo/               # Feast feature repository
│   ├── data/                   # Raw and processed data
│   └── feature_store.yaml      # Feast configuration
│
├── scripts/                    # Utility scripts
│   └── convert_to_parquet.py   # Data conversion utility
│
└── pyproject.toml              # Project dependencies and configuration
```

## Prerequisites

- Python 3.12+
- Redis (for online feature store)
- Feast 0.34+
- `uv` package manager

## Installation

```bash
# Install uv package manager (if not already installed)
pip install uv

# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate

# Install the project
uv pip install -e .
```

## Configuration

The project uses `feature_repo/feature_store.yaml` for Feast configuration:
- Online store: Redis
- Connection: `localhost:6379`

## CLI Commands

### Feature Management

```bash
# Apply feature store components
fs apply

# Materialize features
fs materialize

# Materialize incrementally (optional end date)
fs materialize-incremental
fs materialize-incremental -e "2023-12-31 23:59:59"

# Retrieve online features
fs get-online-features
fs get-online-features -c 101 -f purchase_value
```

## CLI Usage Examples

### Feature Materialization
```bash
# Materialize features
fs materialize
```

### Historical Features Retrieval
```bash
# Retrieve historical features for all customers
fs get-historical-features

# Retrieve historical features within a specific date range
fs get-historical-features --start-date 2023-01-01 --end-date 2023-12-31
```

### Online Features Retrieval
```bash
# Retrieve online features for specific customers
fs get-online-features -c CUST001 -c CUST002

# Retrieve specific features for customers
fs get-online-features -c CUST001 -f purchase_value -f loyalty_score
```

### Online Store Management
```bash
# Clear all data from the online store
fs clear-online-store

# Backup online store to a specific file
fs backup-online-store -f my_backup.rdb
```

### Feature Store Management
```bash
# Apply feature store components
fs apply

# Incrementally materialize features
fs materialize-incremental
```

## Advanced Usage

- Use environment variables for configuration
- Integrate with existing ML pipelines
- Customize feature retrieval based on specific requirements

## Data Conversion

To convert CSV data to Parquet format, use the script in the `scripts` directory:

```bash
python scripts/convert_to_parquet.py
```

## Development

```bash
# Install dev dependencies
uv pip install -e .[dev]
```

## Key Features

- Redis-backed online feature store
- CLI for feature management
- Flexible feature retrieval
- Incremental materialization support
