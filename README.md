# Customer Feature Store

A feature store for managing and serving customer-related features using Feast.

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
fs get-features
fs get-features -c 101 -f purchase_value
```

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

## License

[Specify your license]