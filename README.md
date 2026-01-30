# Sparkify ELT

## Project Overview

This project implements a complete ETL pipeline to build a cloud-based **data warehouse on Amazon Redshift** for a the music streaming company called **Sparkify**.

Sparkify stores raw data in **Amazon S3** (JSON files) and wants to analyze user listening behavior.  
The objective is to load this data into Redshift, transform it, and expose it through a **star schema** optimized for analytical queries.

---

## Architecture


```text
S3 (song_data, log_data)
   |
   | COPY
   v
Redshift Staging Tables (staging_events, staging_songs)
   |
   | INSERT / TRANSFORM
   v
Redshift Analytics Tables (songplays + dimensions)
```

---

## Datasets

### Song Dataset
- S3 path: `s3://udacity-dend/song_data`
- Contains metadata about songs and artists
- One JSON file per song

### Log Dataset
- S3 path: `s3://udacity-dend/log_data`
- Contains user activity logs
- Only events with `page = 'NextSong'` are used

### Log JSON Metadata
- `s3://udacity-dend/log_json_path.json`
- Used by Redshift COPY to parse log JSON files

---

## Data Model (Star Schema)

### Fact Table
**songplays**
- One record per song play event
- Built from log data joined with song metadata

### Dimension Tables
- **users**: user attributes
- **songs**: song attributes
- **artists**: artist attributes
- **time**: time attributes derived from timestamps


---

## Repository Structure

- `create_tables.py`  
  Drops and recreates all staging and analytics tables in Redshift

- `etl.py`  
  Loads data from S3 into staging tables and inserts transformed data into final tables

- `sql_queries.py`  
  Centralized SQL definitions:
  - DROP TABLE statements
  - CREATE TABLE statements
  - COPY commands
  - INSERT statements

- `dwh.cfg`  
  Local configuration file containing Redshift credentials, IAM role ARN, and S3 paths
  (in the .gitignore)

---

## Configuration

The project uses a local configuration file `dwh.cfg`:

```ini
[CLUSTER]
HOST=<redshift-endpoint>
DB_NAME=dev
DB_USER=<db-user>
DB_PASSWORD=<db-password>
DB_PORT=5439
[IAM_ROLE]
ARN=<iam-role-arn>
[S3]
LOG_DATA='s3://udacity-dend/log_data'
LOG_JSONPATH='s3://udacity-dend/log_json_path.json'
SONG_DATA='s3://udacity-dend/song_data'
```


The Redshift cluster must have an IAM role attached with read access to S3.

---

## How to Run the Project

### Step 1: Create Tables
Drops and recreates all tables (staging + analytics):

`python create_tables.py`


### Step 2: Run ETL Pipeline
Loads data into staging tables and populates the star schema:

`python etl.py`


Both scripts complete without output if successful.

---

## Data Validation

After running the ETL, validate the data using the following queries:

```ini
SELECT COUNT() FROM staging_events;
SELECT COUNT() FROM staging_songs;
SELECT COUNT() FROM songplays;
SELECT COUNT() FROM users;
SELECT COUNT() FROM songs;
SELECT COUNT() FROM artists;
SELECT COUNT(*) FROM time;
```


Expected behavior:
- Staging tables are non-empty
- Final tables are non-empty
- `songplays` only contains `NextSong` events

---

## Conclusion

This project demonstrates a complete, production-style ETL pipeline using:
- Amazon S3 for data storage
- Amazon Redshift for cloud data warehousing
- A star schema optimized for analytical workloads

The pipeline is modular, idempotent, and follows standard enterprise data engineering practices.