# ETL Dashboard with LLM-Powered Schema Inference

## Overview

ETL (Extract, Transform, Load) processes are critical in moving and transforming data from source systems to destination databases. However, they often come with significant challenges, especially when:
- **Missing Column Names**: Sometimes, column names are missing and require analyzing the context of the data to assign appropriate names.
- **The source data is messy**: Missing column names, incorrect data formats, and lack of restrictions are common issues.
- **The dataset is large**: Manually cleaning and preparing large datasets is time-intensive and prone to errors.
- **Technical expertise is limited**: Non-technical users often struggle with data preparation, schema design, and executing ETL (Extract, Transform, Load) processes efficiently.

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
  - **Provides step-by-step logs and warnings** for each stage of the transformation process, enabling users to track potential issues effectively.

### 4. **Adjustable Sample Rows**
- Users can adjust the number of rows the LLM analyzes for schema inference, ensuring flexibility for different datasets.

---
## Setup and Run the Dashboard

### Running Locally
#### Prerequisites
- **Python 3.8+**
- **pip** 
- **PostgreSQL**: A running PostgreSQL instance (local or on a remote server).
- An OpenAI API key for LLM integration.

**1. Clone this repository and navigate to the directory**:
   ```bash
   git clone https://github.com/mahsa-nazari/LLM-Assisted-ETL.git
   cd etl-dashboard
   ```

**2. Make the Setup Script Executable**:

```bash
chmod +x setup_and_run_dashboard.sh
```

**4. Run the setup script to start the dashboard**:

   ```bash
./setup_and_run_dashboard.sh
   ```

**5. Access the dashboard** at [http://127.0.0.1:5000](http://127.0.0.1:5000).

### Running with Docker
#### Prerequisites
- **Docker** 
- **PostgreSQL**: A running PostgreSQL instance (local or on a remote server).
- An OpenAI API key for LLM integration.

**1. Clone this repository and navigate to the directory**:
   ```bash
   git clone https://github.com/mahsa-nazari/LLM-Assisted-ETL.git
   cd etl-dashboard
   ```

**2.Start the Service**:
```bash
    docker-compose up -d
```
This will:
   - Pull the Docker image from Docker Hub.
   - Start the application with the default port 5001 mapped to the container.

**3. Access the dashboard** at [http://127.0.0.1:5001](http://127.0.0.1:5001).
- **Note**: You can change port 5001 in the docker-compose file but avoid using port 5000 to prevent potential conflicts if you also wish to run the dashboard locally.
  
**5. To monitor the logs from the running container**:
```bash
    docker-compose logs
   ```

**6. Stopping and removing the container, networks and volumes**:
```bash
    docker-compose down
    docker-compose down --volumes
   ```
---
### Dashboard Usage

1. **Upload a CSV File**  
   - Go to the **"Upload CSV"** section.  
   - Upload your source CSV file.

2. **Set Destination Database**  
   - Configure the connection details for your destination database (e.g., host, port, username, password). 
   - You can configure the dashboard to connect to a PostgreSQL database on your local machine or a remote server. This is how you can fill the "Host" field correctly:
      - For **local databases**, use "localhost" if running locally or "host.docker.internal"( for Linux, use your machine's IP address) if running in docker. 
      - For **remote servers**, enter the server's IP address or domain name in the "Host" field.

3. **Configure OpenAI API**   
   - Optionally, select the model from the list of valid models provided.
   - Add your OpenAI API key and press **"Save API Key and Model"**. 

4. **Schema Inference**  
   - Click **"Infer Schema"** to let the LLM analyze your data and propose a schema. After Schema is created the dashboard navigates you to **Review and Edit Schema** page to review the schema proposed by the LLM.

5. **Review and Edit Schema**  
   - Make any necessary modifications in the **"Edit Schema"** section. Adjustments can include any change as far as it is a valid schema.
   - After making changes, ensure you click **"Update Schema"** to save and apply your edits.  
   - Use the **"Samples to Analyze"** option to adjust the number of rows the LLM analyzes for schema generation. The default is set to 5 rows.  
   - When you change the number of samples, the updated schema will be displayed in the **"Edit Schema"** section. Review it carefully, and if it meets your requirements, don't forget to click **"Update Schema"** to finalize the changes.  
     - *Note:* Increasing the number of samples may lead to a more accurate schema but could also result in higher API costs.

6. **Execute ETL**  
   - After finalizing and approving the schema, initiate the ETL process by clicking **"Apply to PostgreSQL"**. This action will load the data into your configured destination database.

### Logs and Monitoring  
   - Logs for each step of the process are displayed on the dashboard. Regularly check these logs to ensure the workflow is progressing as expected.  
   - The system incorporates multiple fallback mechanisms to handle errors and prevent crashes, enhancing user experience. Reviewing logs allows you to identify and resolve potential issues efficiently.


