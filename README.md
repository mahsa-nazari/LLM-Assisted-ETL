# ETL Dashboard with LLM-Powered Schema Inference

## Overview

ETL (Extract, Transform, Load) processes are critical in moving and transforming data from source systems to destination databases. However, they often come with significant challenges, especially when:
- **The source data is messy**: Missing column names, incorrect data formats, and lack of restrictions are common issues.
- **The dataset is large**: Manually cleaning and preparing large datasets is time-intensive and prone to errors.
- **Technical expertise is limited**: Non-technical users struggle with data preparation and schema design.

In such scenarios, **Large Language Models (LLMs)** offer a transformative approach by automating schema inference and simplifying ETL workflows. 

This **ETL Dashboard** provides a simple, intuitive platform where users can:
- Automatically generate a **proposed schema** by analyzing the first few rows of a CSV file.
- Review, edit, and approve the schema.
- Seamlessly execute the ETL process to a destination database of their choice.

---

## Features

### 1. **LLM-Powered Schema Inference**
- The LLM reads the first few rows of the uploaded CSV file (adjustable sample size).
- It proposes a schema that includes:
  - Column names.
  - Data types (e.g., `string`, `integer`, `date`).
  - Constraints such as:
    - Whether the field is required (`required`).
    - Whether the field must be unique (`unique`).
    - Primary key identification (`primary_key`).

### 2. **Schema Customization**
- Users can review and modify the proposed schema before proceeding.
- Changes can include:
  - Renaming columns.
  - Adjusting data types.
  - Setting constraints such as:
    - Required fields.
    - Unique constraints.
    - Primary keys.


### 3. **Effortless ETL Execution**
- Once the schema is approved, the system:
  - **Transforms the data** intelligently based on the approved schema:
    - For **unique columns**, any repeated values are automatically resolved by appending a unique identifier, ensuring data integrity without manual intervention.
    - For **required fields**, missing values (null or empty) are automatically filled with either `NaN` or a user-defined default value, maintaining consistency and minimizing errors downstream.
  - **Optimizes the data** to align with the constraints defined in the schema, reducing the need for manual pre-processing.
  - **Loads the processed data** into the destination database of your choice, ensuring a seamless transition from raw to structured data.


### 4. **Adjustable Sample Rows**
- Users can adjust the number of rows the LLM analyzes for schema inference, ensuring flexibility for different datasets.

## Setup and Run the Dashboard

### Prerequisites
- **Python 3.8+**
- **PostgreSQL** (or other supported destination databases)
- An OpenAI API key for LLM integration.

### Steps

**1. Clone this repository and navigate to the directory**:
   ```bash
   git clone https://github.com/mahsa-nazari/LLM-Assisted-ETL.git
   cd etl-dashboard
   ```

**2. Install dependencies**:
   ```bash
pip install -r requirements.txt
   ```

**3. Run the setup script to start the dashboard**:
   ```bash
./setup_and_run_dashboard.sh
   ```

**4. 4. **Access the dashboard** at [http://127.0.0.1:5000](http://127.0.0.1:5000).


### Dashboard Usage

1. **Upload a CSV File**  
   - Go to the **"Upload CSV"** section.  
   - Upload your source CSV file.

2. **Set Destination Database**  
   - Configure the connection details for your destination database (e.g., host, port, username, password).

3. **Configure OpenAI API**  
   - Add your OpenAI API key in the **"Settings"** section.  
   - Optionally, select the model from the list of valid models provided.

4. **Schema Inference**  
   - Click **"Infer Schema"** to let the LLM analyze your data and propose a schema.  
   - Adjust the number of rows analyzed if needed.

5. **Review and Edit Schema**  
   - Navigate to the **"View/Edit Schema"** section to review the schema proposed by the LLM.  
   - Make any necessary modifications in the **"Edit Schema"** section. Adjustments can include changing field types, renaming columns, or altering other schema attributes.  
   - After making changes, ensure you click **"Update Schema"** to save and apply your edits.  
   - Use the **"Samples to Analyze"** option to adjust the number of rows the LLM analyzes for schema generation. The default is set to 5 rows.  
   - When you change the number of samples, the updated schema will be displayed in the **"Edit Schema"** section. Review it carefully, and if it meets your requirements, don't forget to click **"Update Schema"** to finalize the changes.  
     - *Note:* Increasing the number of samples may lead to a more accurate schema but could also result in higher API costs.

6. **Execute ETL**  
   - After finalizing and approving the schema, initiate the ETL process by clicking **"Apply to PostgreSQL"**. This action will load the data into your configured destination database.

### Logs and Monitoring  
   - Logs for each step of the process are displayed on the dashboard. Regularly check these logs to ensure the workflow is progressing as expected.  
   - The system incorporates multiple fallback mechanisms to handle errors and prevent crashes, enhancing user experience. Reviewing logs allows you to identify and resolve potential issues efficiently.


