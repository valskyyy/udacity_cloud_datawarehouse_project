import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries

def drop_tables(cur, conn):
    """
    Drops all tables defined in the drop_table_queries list.

    This function iterates over predefined DROP TABLE SQL statements
    and executes them sequentially to reset the database schema.
    Each query is validated to ensure it is not empty before execution.

    Parameters
    ----------
    cur : psycopg2.cursor
        Cursor object connected to the Redshift database.
    conn : psycopg2.connection
        Active connection to the Redshift database.
    """
    for i, query in enumerate(drop_table_queries):
        if not query or not query.strip():
            raise ValueError(f"Empty DROP query at index {i}: {repr(query)}")
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates all tables defined in the create_table_queries list.

    This function executes CREATE TABLE statements to build
    the staging, fact, and dimension tables required for the
    Sparkify analytics star schema.

    Parameters
    ----------
    cur : psycopg2.cursor
        Cursor object connected to the Redshift database.
    conn : psycopg2.connection
        Active connection to the Redshift database.
    """
    for i, query in enumerate(create_table_queries):
        if not query or not query.strip():
            raise ValueError(f"Empty CREATE query at index {i}: {repr(query)}")
        cur.execute(query)
        conn.commit()


def main():
    """
    Entry point for table creation workflow.

    This function:
    - Reads Redshift connection parameters from the dwh.cfg file
    - Establishes a connection to the Redshift cluster
    - Drops existing tables if they exist
    - Creates new staging and analytics tables
    - Closes the database connection
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()