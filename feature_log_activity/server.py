import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables from .env (in project root)
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


def get_all_log_activity():
    """
    Fetch and display all rows from the 'log_activity' table.

    Requirement:
    "Create a function that fetch log_activity table and display the results"
    """
    query = "SELECT * FROM public.log_activity;"
    table_name = "log_activity"

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
    # Run only the log_activity
 get_all_log_activity()

