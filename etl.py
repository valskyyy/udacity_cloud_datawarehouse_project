import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries

def load_staging_tables(cur, conn):
    """
    Loads raw data from S3 into Redshift staging tables.

    This function executes COPY commands to ingest JSON-formatted
    song and log data from Amazon S3 into Redshift staging tables.
    Each COPY query is validated before execution.

    Parameters
    ----------
    cur : psycopg2.cursor
        Cursor object connected to the Redshift database.
    conn : psycopg2.connection
        Active connection to the Redshift database.
    """
    for i, query in enumerate(copy_table_queries):
        if not query or not query.strip():
            raise ValueError(f"Empty COPY query at index {i}: {repr(query)}")
        cur.execute(query)
        conn.commit()

def insert_tables(cur, conn):
    """
    Transforms and inserts data from staging tables into analytics tables.

    This function executes INSERT statements that populate the
    fact and dimension tables of the star schema using data
    from the staging tables.
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()

def main():
    """
    Entry point for the ETL pipeline.

    This function:
    - Reads Redshift connection parameters from the dwh.cfg file
    - Connects to the Redshift cluster
    - Loads data from S3 into staging tables
    - Transforms and inserts data into fact and dimension tables
    - Closes the database connection
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()

if __name__ == "__main__":
    main()