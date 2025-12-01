import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


def get_connection():
    """
    Open a connection to the Supabase Postgres database
    using values stored in the .env file.
    """
    USER = os.getenv("user")
    PASSWORD = os.getenv("password")
    HOST = os.getenv("host")
    PORT = os.getenv("port", "5432")
    DBNAME = os.getenv("dbname")
    SSLMODE = os.getenv("sslmode", "require")

    conn = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME,
        sslmode=SSLMODE
    )
    return conn


def fetch_actsin():
    try:
        # Connect to your PostgreSQL database
        connection = get_connection()
        
        cursor = connection.cursor()
        
        # Query to fetch data from the actsin table
        fetch_query = "SELECT * FROM actsin;"
        
        cursor.execute(fetch_query)
        
        # Fetch all rows from the executed query
        results = cursor.fetchall()
        
        # Display the results
        for row in results:
            print(row)
    
    except Exception as error:
        print(f"Error fetching data from PostgreSQL table: {error}")
    
    finally:
        # Close the database connection and cursor
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_all_actors():
    """
    Fetch and display all rows from the 'actors' table.
    """
    query = "SELECT * FROM public.actors;"
    table_name = "actors"

    conn = None
    try:
        conn = get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()

            print(f"\n=== {table_name.upper()} ===")
            print(f"Total rows: {len(rows)}")

            for row in rows:
                print(row)

            return rows

    except Exception as e:
        print(f"Error while fetching data from '{table_name}': {e}")
        return []

    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    # Requirement: feature/actors must only run actors function
    get_all_actors()
    fetch_actsin()
