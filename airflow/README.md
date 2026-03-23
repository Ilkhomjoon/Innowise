# Airflow Data Processing & MongoDB Loading Pipeline

This project is a local deployment of a data processing pipeline using **Apache Airflow, Python, Pandas, and MongoDB**, fully containerized using **Docker** and **uv** (for fast dependency management).

### Technologies Used
* **Orchestration:** Apache Airflow
* **Data Processing:** Python, Pandas
* **Database:** MongoDB
* **Containerization:** Docker, Docker Compose
* **Environment Management:** uv

## How to Run the Project

**1. Start the Docker Containers:**
Open your terminal in the project directory and run:
```bash
docker-compose up --build -d
```

**2. Configure Airflow Connections:**
Access the Airflow UI at `http://localhost:8080` (Credentials: `admin` / `admin`). Navigate to **Admin -> Connections** and add the following:
* `fs_default` (Connection Type: File)
* `mongo_default` (Connection Type: MongoDB, Host: mongo, Port: 27017)

**3. Trigger the Pipeline:**
Place the raw data file (`airflow_data.csv`) into the `data/` directory. The Airflow FileSensor will automatically detect the file and trigger the processing pipeline.

---

## Pipeline Architecture (DAGs)

**1_data_processing_dag (Data Cleaning & Transformation):**
* **Sensor:** Waits for the file to appear in the directory.
* **Branching:** Checks whether the file is empty or contains data.
* **TaskGroup (Processing):** Replaces "null" values with "-", sorts the data by `created_date`, and cleans the `content` column by removing emojis and unnecessary characters, leaving only text and punctuation.

**2_load_to_mongodb_dag (MongoDB Loader):**
* Uses **Dataset Data-aware scheduling** to trigger automatically once the processing DAG successfully finishes.
* Reads the cleaned dataset and loads it into the `airflow_data` collection inside the `innowise_db` database.

![DAG Architecture](images/Screenshot%202026-03-23%20174806.png)

---

## MongoDB Aggregation Results

After successfully loading the data, the following complex aggregation queries were executed and verified via MongoDB Compass:

**1. Top 5 frequently occurring comments:**
![Top 5 Comments](images/Screenshot%202026-03-23%20174456.png)

**2. All entries where the "content" field is less than 5 characters long:**
![Short Content](images/Screenshot%202026-03-23%20174510.png)

**3. Average rating for each day (Result in Timestamp format):**
![Average Rating](images/Screenshot%202026-03-23%20174519.png)

---
*Completed by Ilkhomjon Ibragimov*
