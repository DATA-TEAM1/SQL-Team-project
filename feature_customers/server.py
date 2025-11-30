import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import pool

# Load environment variables from .env
load_dotenv()

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DBNAME = os.getenv("DBNAME")

# Initialize a connection pool
connection_pool = None
try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        1,  # min connections
        10,  # max connections
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        database=DBNAME
    )
    print("Connection pool created successfully!")
except Exception as e:
    print(f"Failed to create connection pool: {e}")

# Function to fetch and display customers


def fetch_customers():
    connection = None
    try:
        # Get a connection from the pool
        connection = connection_pool.getconn()
        cursor = connection.cursor()

        # Execute query
        cursor.execute("SELECT * FROM customers;")
        rows = cursor.fetchall()

        # Display results
        if rows:
            for row in rows:
                print(row)
        else:
            print("No customers found.")

        # Close cursor
        cursor.close()

    except Exception as e:
        print(f"Error fetching customers: {e}")

    finally:
        # Return the connection to the pool
        if connection:
            connection_pool.putconn(connection)


# Example usage
if __name__ == "__main__":
    fetch_customers()
    # Close all connections when done
    connection_pool.closeall()
    print("Connection pool closed.")
