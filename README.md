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
  - **Transforms the data** according to the schema.
  - **Loads the data** into a user-specified destination database.

### 4. **Adjustable Sample Rows**
- Users can adjust the number of rows the LLM analyzes for schema inference, ensuring flexibility for different datasets.

