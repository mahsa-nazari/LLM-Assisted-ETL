import pandas as pd
from sqlalchemy import create_engine
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def validate_schema_mapping(schema_mapping):
    """Validate the schema mapping structure."""
    if not all(isinstance(target, dict) and "name" in target and "type" in target for target in schema_mapping.values()):
        raise ValueError(
            f"Invalid schema_mapping format. Expected a dictionary of dictionaries with 'name' and 'type' keys."
        )

def map_data_type(dtype):
    """Map target schema type to Pandas transformation."""
    type_mapping = {
        "date": lambda x: pd.to_datetime(x, errors="coerce"),
        "float": lambda x: pd.to_numeric(x, errors="coerce"),
        "integer": lambda x: pd.to_numeric(x, errors="coerce", downcast="integer"),
        "string": lambda x: x.astype(str),
    }
    return type_mapping.get(dtype, lambda x: x)

def transform_data(file_path, schema_mapping):
    """
    Transforms the input CSV data based on the provided schema mapping.

    Args:
        file_path (str): Path to the input CSV file.
        schema_mapping (dict): Mapping of source columns to target schema.

    Returns:
        pd.DataFrame: Transformed DataFrame.
    """
    try:
        # Validate schema mapping
        validate_schema_mapping(schema_mapping)
        logging.info("Schema mapping validated.")

        # Load the CSV file
        df = pd.read_csv(file_path)
        logging.info(f"Loaded data from {file_path}, shape: {df.shape}")

        # Handle missing columns by adding them with NaN values
        for col in schema_mapping.keys():
            if col not in df.columns:
                logging.warning(f"Column {col} is missing in the CSV. Filling with NaN.")
                df[col] = pd.NA

        # Rename columns based on schema mapping
        df.rename(columns={src: target["name"] for src, target in schema_mapping.items()}, inplace=True)

        # Handle schema constraints and transformations
        for target_column, target_info in schema_mapping.items():
            column_name = target_info["name"]
            dtype = target_info["type"]
            constraints = target_info.get("constraints", {})

            # Apply data type mapping
            df[column_name] = map_data_type(dtype)(df[column_name])

            # Handle required fields
            if constraints.get("required", False):
                missing_count = df[column_name].isna().sum()
                if missing_count > 0:
                    logging.warning(f"Column {column_name} has {missing_count} missing values.")
                    df[column_name].fillna("MISSING", inplace=True)  # Default fill value for missing required fields
                    logging.info(f"Filled missing values in {column_name} with 'MISSING'.")

            # Handle unique constraints 
            if constraints.get("unique", False):
                duplicates = df[column_name].duplicated(keep=False)
                if duplicates.any():
                    duplicate_indices = df[duplicates].index
                    for i in duplicate_indices:
                        new_value = f"{df.loc[i, column_name]}_{i}"
                        logging.warning(
                            f"Duplicate value found in column {column_name} at row {i}. Rewriting to {new_value}."
                        )
                        df.at[i, column_name] = new_value

            # Handle primary key constraints 
            if target_info.get("primary_key", False):
                if df[column_name].isna().any():
                    raise ValueError(f"Primary key column {column_name} contains missing values.")
                if df[column_name].duplicated().any():
                    raise ValueError(f"Primary key column {column_name} contains duplicate values.")

        # Log the final transformation summary
        logging.info(f"Transformation completed successfully. Final data shape: {df.shape}")
        return df

    except Exception as e:
        logging.error(f"Error during transformation: {e}")
        raise


def load_data_to_postgres(df, table_name, connection_uri):
    """
    Loads the transformed data into PostgreSQL.

    Args:
        df (pd.DataFrame): Transformed DataFrame.
        table_name (str): Target PostgreSQL table name.
        connection_uri (str): PostgreSQL connection URI.
    """
    try:
        engine = create_engine(connection_uri)
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        logging.info(f"Data loaded into PostgreSQL table '{table_name}'.")
    except Exception as e:
        logging.error(f"Error loading data into PostgreSQL: {e}")
        raise
