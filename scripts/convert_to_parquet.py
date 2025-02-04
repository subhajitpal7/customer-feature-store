import pandas as pd
import os
import pyarrow.parquet as pq
import pyarrow as pa

def convert_csv_to_parquet(csv_path, parquet_path=None):
    """
    Convert CSV file to Parquet format with comprehensive configuration
    
    Args:
        csv_path (str): Path to the input CSV file
        parquet_path (str, optional): Path to save the Parquet file. 
                                      If None, uses the same path with .parquet extension
    """
    # Validate input file
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Input CSV file not found: {csv_path}")
    
    # Determine Parquet output path
    if parquet_path is None:
        parquet_path = csv_path.rsplit('.', 1)[0] + '.parquet'
    
    # Read CSV with explicit parsing
    df = pd.read_csv(
        csv_path, 
        parse_dates=['purchase_timestamp'],
        infer_datetime_format=True
    )
    
    # Ensure data types are consistent
    df['customer_id'] = df['customer_id'].astype('int64')
    df['purchase_value'] = df['purchase_value'].astype('float64')
    df['loyalty_score'] = df['loyalty_score'].astype('float32')
    
    # Convert to PyArrow Table
    table = pa.Table.from_pandas(df)
    
    # Write Parquet file with Snappy compression
    pq.write_table(
        table, 
        parquet_path, 
        compression='snappy'
    )
    
    # Verify Parquet file
    parquet_file = pq.ParquetFile(parquet_path)
    print("\nParquet File Details:")
    print(f"Path: {parquet_path}")
    print(f"Rows: {parquet_file.metadata.num_rows}")
    print(f"Columns: {parquet_file.metadata.num_columns}")
    print("\nColumn Types:")
    print(parquet_file.schema)
    
    return parquet_path

def main():
    # Input CSV path
    csv_path = "feature_repo/data/test_task_data.csv"
    
    try:
        # Convert to Parquet
        parquet_path = convert_csv_to_parquet(csv_path)
        print(f"\n✅ Successfully converted to Parquet: {parquet_path}")
    
    except Exception as e:
        print(f"❌ Conversion Failed: {e}")
        raise

if __name__ == "__main__":
    main()
