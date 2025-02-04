from datetime import timedelta

from feast import (
    Entity,
    FeatureView,
    Field,
    FileSource,
    ValueType
)
from feast.types import Float32, Float64, Int64

from customer_feature_store.config import config

# Define the entity (customer)
customer = Entity(
    name="customer",
    join_keys=["customer_id"],
    description="Customer identifier"
)

# Define the file source for our dataset
customer_source = FileSource(
    name="customer_data_source",
    path=config.get_data_path('test_task_data').replace('.csv', '.parquet'),
    timestamp_field="purchase_timestamp"
)

# Define feature view
customer_feature_view = FeatureView(
    name="customer_features",
    entities=[customer],
    ttl=timedelta(days=30),  # Cache features for 30 days
    schema=[
        Field(name="purchase_value", dtype=Float64),
        Field(name="loyalty_score", dtype=Float32)
    ],
    online=True,
    source=customer_source,
    tags={
        "team": "customer_analytics",
        "data_type": "transactional"
    }
)
