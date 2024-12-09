from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import pandas as pd
from app.transform import transform_data, load_data_to_postgres
from app.llm_utils import infer_schema_logic
import logging
import json
from sqlalchemy.sql import text
from logging.handlers import RotatingFileHandler
from openai import OpenAI

app = Flask(__name__)
app.secret_key = "dev_secret_key"

# Configure logging
LOG_FILE = os.path.join(os.path.abspath(os.getcwd()), "app.log")
log_handler = RotatingFileHandler(LOG_FILE, maxBytes=100000, backupCount=10)
log_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)


if not os.path.exists(LOG_FILE):
    open(LOG_FILE, "w").close()

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filemode="a"
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


SCHEMA_FILE = "schema.json"
TABLE_NAME = "harmonized_data"
API_KEY_FILE = "api_key.txt"


def test_api_connection(client):
    """
    Tests the connection to the OpenAI API.
    Logs whether the connection is successful.
    """
    try:
        model = session.get("selected_model", "gpt-3.5-turbo")  # Default to gpt-3.5-turbo
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Test the OpenAI API connection."}
            ],
        )
        if response:
            logging.info(f"Successfully connected to the OpenAI API using model {model}.")
        else:
            logging.error(f"Connection to the OpenAI API failed: Empty response from model {model}.")
    except Exception as e:
        logging.error(f"Connection to the OpenAI API failed: {e}")

@app.before_request
def clear_flash_messages():
    session.pop('_flashes', None)
def load_api_key():
    """Load the API key from a file during app startup."""
    if os.path.exists(API_KEY_FILE):
        try:
            with open(API_KEY_FILE, "r") as f:
                api_key = f.read().strip()
                if api_key:
                    session["openai_api_key"] = api_key  # Load into session
                    app.logger.info("API key loaded from file successfully.")
        except Exception as e:
            app.logger.error(f"Failed to load API key from file: {e}")



@app.route("/")
def index():
    """Dashboard home page."""
    try:
        with open(LOG_FILE, "r") as f:
            logs = f.read().replace("\n", "<br>")
    except FileNotFoundError:
        logs = "No logs available."
    return render_template("index.html", logs=logs)

@app.route("/save_api_key", methods=["POST"])
def save_api_key():
    """Save the OpenAI API key."""
    try:
        api_key = request.form.get("api_key")
        selected_model = request.form.get("model")
        if not api_key:
            flash("API Key cannot be empty.")
            app.logger.error("Attempt to save empty API key.")
            return redirect(url_for("index"))

        # Save the API key to the file
        with open(API_KEY_FILE, "w") as f:
            f.write(api_key)
            
        # Store the API key in the session
        session["openai_api_key"] = api_key
        # Log success
        app.logger.info("OpenAI API key was updated successfully.")

        # Store the selected model in the session
        if selected_model:
            session["selected_model"] = selected_model 
            app.logger.info(f"Model '{selected_model}' selected and saved.")
        else:
            session["selected_model"] = "gpt-3.5-turbo"  # Default model
            app.logger.info("No model selected. Defaulting to 'gpt-3.5-turbo'.")


    except Exception as e:
        app.logger.error(f"Failed to save API key: {e}")

    return redirect(url_for("index"))

@app.route("/set_destination_db", methods=["GET", "POST"])
def set_destination_db():
    if request.method == "POST":
        # Get the form data
        db_host = request.form.get("db_host")
        db_name = request.form.get("db_name")
        db_user = request.form.get("db_user")
        db_password = request.form.get("db_password")
        db_port = request.form.get("db_port", "5432")  # Default port to 5432 if not provided

        # Validate input fields
        if not all([db_host, db_name, db_user, db_password]):
            flash("All fields are required to set the destination database.")
            return redirect(request.url)

        # Save the destination DB connection details in the session
        session["destination_db"] = {
            "host": db_host,
            "name": db_name,
            "user": db_user,
            "password": db_password,
            "port": db_port,
        }

        app.logger.info("Database connection info saved.")
        return redirect(url_for("index"))

    return render_template("set_destination_db.html")


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")
        if not file:
            flash("No file part found. Please upload a valid file.")
            return render_template("upload.html")
        if file.filename == '':
            flash("No file selected. Please choose a file to upload.")
            return render_template("upload.html")
        if not file.filename.endswith('.csv'):
            flash("Invalid file type. Please upload a CSV file.")
            return render_template("upload.html")
        
        # Saving the file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        try:
            file.save(file_path)
        except Exception as e:
            flash(f"Error saving file: {e}")
            return render_template("upload.html")
        
        session["uploaded_file_path"] = file_path
        file_size = os.path.getsize(file_path)
        app.logger.info(f"File '{file.filename}' uploaded successfully, size: {file_size} bytes")
        return redirect(url_for("index"))
    return render_template("upload.html")

@app.route("/infer_schema", methods=["POST"])
def infer_schema():
    csv_file_path = session.get("uploaded_file_path")
    if not csv_file_path or not os.path.exists(csv_file_path):
        flash("No uploaded file found. Please upload a file first.")
        return redirect(url_for("index"))
    app.logger.info(f"Starting Inferring Schema for: {csv_file_path} ...")
    try:
        api_key = session["openai_api_key"]
        if not api_key: 
            raise ValueError("API key missing. Please set it before proceeding.")  
        client = OpenAI(api_key=api_key)

        model = session.get("selected_model", "gpt-3.5-turbo")
        app.logger.info(f"Using model: {model}")

        schema_mapping = infer_schema_logic(csv_file_path, client, model=model) 
        session["schema_mapping"] = schema_mapping 
        with open(SCHEMA_FILE, "w") as f:
            json.dump(schema_mapping, f, indent=4)
        app.logger.info("Schema inferred and saved successfully.")
        return redirect(url_for("schema"))
    
    except Exception as e:
        app.logger.error(f"Failed to infer schema: {e}")
        flash(f"Schema inference failed: {e}")

        # Fallback: Load the last saved schema if available
        if os.path.exists(SCHEMA_FILE):
            try:
                with open(SCHEMA_FILE, "r") as f:
                    session["schema_mapping"] = json.load(f)
                app.logger.info("Loaded the last saved schema as a fallback.")
                flash("Using the last saved schema as a fallback.")
            except Exception as fallback_error:
                app.logger.error(f"Fallback schema loading failed: {fallback_error}")
                flash("No valid schema available. Please retry after fixing the error.")
        return redirect(url_for("index"))

@app.route("/delete_logs", methods=["POST"])
def delete_logs():
    """Delete all logs from the log file."""
    try:
        with open(LOG_FILE, "w") as f:
            f.truncate(0)  # Clear the log file
    except Exception as e:
        flash(f"Failed to delete logs: {e}")
        app.logger.error(f"Error deleting logs: {e}")
    return redirect(url_for("index"))


@app.route("/schema", methods=["GET", "POST"])
def schema():
    """
    View/Edit schema and manage sample rows for schema inference.

    - Allows editing and saving schema.
    - Handles applying schema changes to PostgreSQL.
    - Updates the number of sample rows for schema inference.
    """
    schema_mapping = session.get("schema_mapping", {})
    schema_mapping_updated_sample_rows = None  # Holds inferred schema for Edit Schema
    sample_rows = session.get("sample_rows", 5)  # Default to 5 sample rows
    # Load existing schema if available
    if "schema_mapping" not in session:
        if os.path.exists(SCHEMA_FILE):
            try:
                with open(SCHEMA_FILE, "r") as f:
                    session["schema_mapping"] = json.load(f)  # Load schema into session
            except (FileNotFoundError, json.JSONDecodeError) as e:
                app.logger.error(f"Error loading schema: {e}")
                session["schema_mapping"] = {}  # Default to empty schema
                flash("Failed to load existing schema. Please check the schema file.")

    if request.method == "POST":
        if "save_schema" in request.form:
            # Save updated schema
            try:
                new_schema = request.form.get("schema")
                schema_mapping = json.loads(new_schema)
                session["schema_mapping"] = schema_mapping
                with open(SCHEMA_FILE, "w") as f:
                    json.dump(schema_mapping, f, indent=4)
                app.logger.info("Schema updated and saved successfully.")
            except json.JSONDecodeError as e:
                app.logger.error(f"Invalid JSON schema provided: {e}")
                flash("Invalid schema format. Please provide valid JSON.")

        elif "apply_postgres" in request.form:
            # Apply schema to the database
            destination_db = session.get("destination_db")
            if not destination_db:
                flash("Destination database connection details are missing. Please set them first.")
                return redirect(url_for("set_destination_db"))

            db_uri = (
                f"postgresql://{destination_db['user']}:{destination_db['password']}@"
                f"{destination_db['host']}:{destination_db['port']}/{destination_db['name']}"
            )

            csv_file_path = session.get("uploaded_file_path", "")
            if not csv_file_path:
                flash("No CSV file uploaded. Please upload a file before applying schema changes.")
                return redirect(url_for("upload_file"))

            app.logger.info("Initiating ETL pipeline...")
            try:
                transformed_df = transform_data(csv_file_path, schema_mapping)
                load_data_to_postgres(transformed_df, TABLE_NAME, db_uri)
                app.logger.info("ETL pipeline executed successfully.")
            except Exception as e:
                app.logger.error(f"Pipeline execution failed: {e}")
                flash(f"Pipeline execution failed: {e}")

        elif "update_sample_rows" in request.form:
            # Update sample rows for schema inference
            try:
                new_sample_rows = request.form.get("sample_rows")
                
                if new_sample_rows.isdigit() and int(new_sample_rows) > 2 and int(new_sample_rows) != 5:
                    sample_rows = int(new_sample_rows)  # Update only if valid
                    session["sample_rows"] = sample_rows  # Save updated value in session

                    csv_file_path = session.get("uploaded_file_path", "")
                    if not csv_file_path:
                        flash("No CSV file uploaded. Please upload a file first.")
                        return redirect(url_for("upload_file"))

                    # Infer schema using the updated number of sample rows
                    api_key = session["openai_api_key"]
                    client = OpenAI(api_key=api_key)
                    model = session.get("selected_model", "gpt-3.5-turbo")
                    schema_mapping_updated_sample_rows = infer_schema_logic(csv_file_path, client, model, sample_rows)
                    flash(f"Schema inferred using {sample_rows} sample rows successfully!")
                    app.logger.info(f"Schema updated with {sample_rows} sample rows.")
                else:
                    app.logger.info("Invalid sample rows value. No action taken.")
                    flash("Invalid sample rows value. Please enter a valid number greater than 0.")
            except Exception as e:
                app.logger.error(f"Error updating sample rows: {e}")
                flash(f"Failed to update schema using {sample_rows} rows: {e}")
    if not isinstance(sample_rows, int) or sample_rows <= 0:
        sample_rows = 5  # Default to 5 if invalid
    # Render the schemas properly
    return render_template(
        "schema.html",
        schema=json.dumps(
            schema_mapping_updated_sample_rows if schema_mapping_updated_sample_rows else schema_mapping,
            indent=4
        ),  # For Edit Schema
        current_schema=json.dumps(schema_mapping, indent=4),  # For Current Schema
        sample_rows=sample_rows
    )

if __name__ == "__main__":
    app.run(debug=True)
