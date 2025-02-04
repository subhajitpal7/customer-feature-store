# Standard library imports
import os
from typing import Optional, List
from datetime import datetime
from zoneinfo import ZoneInfo

# Data manipulation
import pandas as pd
import redis

# Feast imports
from feast import FeatureStore

# Local imports
from customer_feature_store.core.feature_definitions import (
    customer, customer_source, customer_feature_view
)
from customer_feature_store.config import config, get_data_path

class FeatureService:
    def __init__(self, repo_path: str = None):
        """Initialize Feature Service with Feast Feature Store"""
        if repo_path is None:
            repo_path = config.get_config('data', 'feature_repo_path')
        self.store = FeatureStore(repo_path=repo_path)
        self.redis_client = None
        try:
            redis_host = config.get_config('redis', 'host')
            redis_port = config.get_config('redis', 'port')
            self.redis_client = redis.Redis(host=redis_host, port=int(redis_port))
            self.redis_client.ping()
            print("✅ Redis connection established successfully.")
        except Exception as e:
            print(f"⚠️ Could not establish Redis connection: {e}")
            self.redis_client = None

    def apply_feature_store(self):
        """Apply feature store entities, sources, and views"""
        self.store.apply([customer, customer_source, customer_feature_view])

    def materialize_features(self, start_date: Optional[pd.Timestamp] = None, end_date: Optional[pd.Timestamp] = None):
        """Materialize features for a given time range"""
        df = pd.read_csv(get_data_path('test_task_data'))
        if start_date is None:
            start_date = df['purchase_timestamp'].min().to_pydatetime().replace(tzinfo=ZoneInfo('Europe/Athens'))
        if end_date is None:
            end_date = df['purchase_timestamp'].max().to_pydatetime().replace(tzinfo=ZoneInfo('Europe/Athens'))
        self.store.materialize(feature_views=["customer_features"], start_date=start_date, end_date=end_date)

    def materialize_incremental(self, end_date: Optional[pd.Timestamp] = None):
        """Incrementally materialize features"""
        if end_date is None:
            end_date = pd.Timestamp.now(tz='UTC')
        self.store.materialize_incremental(end_date=end_date)

    def get_historical_features(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, features: Optional[List[str]] = None):
        """Retrieve historical features for a given time range"""
        df = pd.read_csv(get_data_path('test_task_data'))
        if start_date is not None:
            df = df[df['purchase_timestamp'] >= start_date]
        if end_date is not None:
            df = df[df['purchase_timestamp'] <= end_date]
        entity_df = df.groupby('customer_id')['purchase_timestamp'].min().reset_index()
        entity_df.columns = ['customer_id', 'event_timestamp']
        if features is None:
            features = ["customer_features:purchase_value", "customer_features:loyalty_score"]
        historical_features = self.store.get_historical_features(entity_df=entity_df, features=features)
        return historical_features.to_df()

    def get_online_features(self, customer_ids: Optional[List[str]] = None, features: Optional[List[str]] = None):
        """Retrieve online features for specified customers"""
        if customer_ids is None:
            df = pd.read_csv(get_data_path('test_task_data'))
            customer_ids = df['customer_id'].unique().astype(str).tolist()
        entity_rows = [{"customer_id": str(cid)} for cid in customer_ids]
        if features is None:
            features = ["customer_features:purchase_value", "customer_features:loyalty_score"]
        online_features = self.store.get_online_features(features=features, entity_rows=entity_rows)
        return online_features.to_df()

    def backup_online_store(self, backup_file: str = 'online_store_backup.rdb'):
        """Create a backup of the online store"""
        if self.redis_client:
            self.redis_client.save()
            print(f"✅ Online store backed up to {backup_file}")
        else:
            print("⚠️ Redis connection not available.")

    def clear_online_store(self):
        """Clear all data from the online store"""
        if self.redis_client:
            self.redis_client.flushdb()
            print("✅ Online store (Redis) cleared successfully.")
        else:
            print("⚠️ Redis connection not available.")
