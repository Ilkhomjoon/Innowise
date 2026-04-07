# ✈️ Airline ETL Pipeline: Snowflake & Apache Airflow

## Project Overview
This project implements an automated, robust ETL (Extract, Transform, Load) pipeline using **Apache Airflow** (via Astro CLI) and **Snowflake**. It processes raw airline flight data, cleanses it, and aggregates it into business-ready metrics using the Medallion Data Architecture (Bronze, Silver, Gold).

## Tech Stack
* **Orchestration:** Apache Airflow (Docker / Astro CLI)
* **Data Warehouse:** Snowflake
* **Languages:** Python, SQL

## Data Architecture (Medallion)
The pipeline is designed with 3 distinct layers to ensure data quality and traceability:
1. **STAGE_1_RAW (Bronze):** Ingests raw CSV data (`flights.csv`) from Snowflake's internal stage. It dynamically handles column mismatches and enclosed commas.
2. **STAGE_2_CORE (Silver):** Cleanses data, enforces correct data types, and leverages Snowflake `STREAMS` for Change Data Capture (CDC). Includes an `AUDIT_LOG` table for execution tracking.
3. **STAGE_3_ANALYTICS (Gold):** Aggregates data to calculate final business metrics (e.g., total passengers and average age per flight status) for reporting.

## Project Structure
* `dags/` - Contains the Airflow DAG (`pipeline.py`) that orchestrates the SQL executions.
* `snowflake_setup.sql` - Complete SQL script to initialize Snowflake databases, schemas, tables, formats, and stored procedures.
* `requirements.txt` - Python dependencies (Snowflake providers for Airflow).
* `Dockerfile` / `airflow_settings.yaml` - Astro CLI configurations for the local Airflow container environment.

## How to Run
1. Execute `snowflake_setup.sql` in your Snowflake worksheet to set up the Data Warehouse.
2. Upload the raw `flights.csv` file to your Snowflake internal stage (`AIRLINE_STAGE`).
3. Start the local Airflow environment using Astro CLI:
   ```bash
   astro dev start 
   ```
4. Set up the Snowflake connection (snowflake_default) in the Airflow UI.  
5. Trigger the snowflake_airline_etl DAG and monitor the execution!

## Result images

![Airflow dag](images\image1.png)

![SQL Execution](images\image.png)