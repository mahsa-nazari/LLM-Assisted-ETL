from openai import OpenAI
import logging
import pandas as pd
import json
import re


def infer_schema_logic(file_path, client, model, sample_rows=5):
    """
    Uses LLM (OpenAI) to infer the schema of a CSV file.

    Args:
        file_path (str): Path to the CSV file.
        sample_rows (int): Number of rows to sample for schema inference.

    Returns:
        dict: Schema mapping where keys are source column names and values are dictionaries with `name` and `type`.
    """
    logger = logging.getLogger(__name__)  

    # Load the CSV file
    df = pd.read_csv(file_path)

    sample_data = df.head(sample_rows).to_dict(orient="records")

    # Construct the prompt for the LLM
    prompt = f"""
    Analyze the following dataset and infer a schema for mapping source columns to a target structure.
    Provide the output as a JSON object where each source column maps to a dictionary containing:
    - "name": the target column name
    - "type": the data type (e.g., "string", "integer", "float", "date")
    - "constraints": a dictionary with additional validation details, such as:
        - "required": whether the column must have a value (true/false)
        - "unique": whether the values in the column must be unique (true/false)
    - "primary_key": whether this column is the primary key for the dataset (true/false).
    
    Make sure to identify the primary key accurately if the dataset contains an obvious unique identifier.
    Dataset sample:
    {sample_data}
    Example response:
    {{
        "ColumnA": {{
            "name": "full_name",
            "type": "string",
            "constraints": {{"required": true, "unique": false}},
            "primary_key": false
        }},
        "ColumnB": {{
            "name": "age",
            "type": "integer",
            "constraints": {{"required": true, "unique": false}},
            "primary_key": false
        }},
        "ColumnC": {{
            "name": "transaction_id",
            "type": "integer",
            "constraints": {{"required": true, "unique": true}},
            "primary_key": true
        }}
    }}
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=1024
        )

        logger.debug(f"Raw OpenAI API response: {response}")  


        message_content = response.choices[0].message.content

        if not message_content:
            raise ValueError("OpenAI API returned an empty response.")

        # Extract JSON
        json_match = re.search(r"\{.*\}", message_content, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON object found in the response.")
        raw_schema_mapping = json.loads(json_match.group())

        schema_mapping = {}
        for column, target in raw_schema_mapping.items():
            if isinstance(target, dict) and "name" in target and "type" in target:
                schema_mapping[column] = target
            else:
                logger.warning(f"Unexpected format for column '{column}': {target}")
                schema_mapping[column] = {"name": column.lower(), "type": "string"}  # Fallback

        return schema_mapping
    except Exception as e:
        raise RuntimeError(f"Error during schema inference: {e}")
