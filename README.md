# Apache Airflow Installation Guide

This guide walks you through the process of setting up Apache Airflow in a virtual environment with PostgreSQL as the backend database.

## Prerequisites

- Python 3.11 (You can adjust this to a compatible version)
- PostgreSQL installed
- Basic familiarity with the command line

## Installation Steps

### 1. Create a Virtual Environment

```bash
cd /path/to/your/desired/folder
python3.11 -m venv airflow-env
source airflow-env/bin/activate
```

### 2. Install Apache Airflow and PostgreSQL Dependencies

```bash
pip install apache-airflow[postgres]
```

### 4. Create PostgreSQL Database and User

```bash
sudo -u postgres psql
CREATE DATABASE your_db_name;
CREATE USER your_db_user WITH ENCRYPTED PASSWORD 'your_db_password';
ALTER USER your_db_user CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_user;
\q
```

### 5. Configure Airflow to Use PostgreSQL

Create or modify `airflow.cfg` in your Airflow home directory:

[core]
sql_alchemy_conn = postgresql+psycopg2://your_db_user:your_db_password@localhost/your_db_name
executor = LocalExecutor

[webserver]
web_server_host = 0.0.0.0
web_server_port = 8080

[scheduler]
dag_dir_list_interval = 300

[logging]
# Configure logging settings if needed

6. Initialize Airflow Database

```bash
airflow db init
```

7. Start Airflow Webserver and Scheduler

```bash
airflow webserver --port 8080
airflow scheduler
```
8. Access Airflow UI

Open a web browser and navigate to http://localhost:8080 to access the Airflow UI.

For any issues or advanced configurations, refer to the official Airflow documentation.
