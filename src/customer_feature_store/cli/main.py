# Standard library imports
from typing import Optional, List
from datetime import datetime
from zoneinfo import ZoneInfo

# Third-party imports
import click
import pandas as pd

# Local imports
from customer_feature_store.service.feature_service import FeatureService
from customer_feature_store.config import get_data_path

@click.group()
def cli():
    """Feature Store CLI"""
    pass

@cli.command()
def apply():
    """Apply feature store components"""
    service = FeatureService()
    service.apply_feature_store()
    click.echo("✅ Feature store components applied successfully.")

@cli.command()
def materialize():
    """Materialize features"""
    service = FeatureService()
    service.materialize_features()
    click.echo("✅ Features materialized successfully.")

@cli.command()
@click.option('--end-date', '-e', help='End date for incremental materialization (YYYY-MM-DD HH:MM:SS)')
def materialize_incremental(end_date):
    """Incrementally materialize features"""
    service = FeatureService()
    end = datetime.fromisoformat(end_date) if end_date else None
    service.materialize_incremental(end_date=end)
    click.echo("✅ Incremental materialization completed.")

@cli.command()
@click.option('--start-date', '-s', help='Start date for feature retrieval (YYYY-MM-DD)')
@click.option('--end-date', '-e', help='End date for feature retrieval (YYYY-MM-DD)')
def get_historical_features(start_date, end_date):
    """Retrieve historical features"""
    service = FeatureService()
    historical_features = service.get_historical_features(
        start_date=start_date, 
        end_date=end_date
    )
    click.echo(historical_features)

@cli.command()
@click.option('--customer-ids', '-c', multiple=True, help='Customer IDs to retrieve features for')
@click.option('--features', '-f', multiple=True, help='Specific features to retrieve')
def get_features(customer_ids, features):
    """Retrieve online features"""
    service = FeatureService()
    customer_ids = list(customer_ids) if customer_ids else None
    features = list(features) if features else None
    
    online_features = service.get_online_features(
        customer_ids=customer_ids, 
        features=features
    )
    click.echo(online_features)

if __name__ == "__main__":
    cli()
