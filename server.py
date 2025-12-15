import os
from typing import Any, Dict, List
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

# ---------------------------------------------------------
# GENERIC FETCH FUNCTION
# ---------------------------------------------------------
def _fetch_all(query: str) -> List[Dict[str, Any]]:
    """
    Executes a SELECT query and returns all rows as a list of dicts.
    """
    conn = None
    try:
        conn = get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return rows
    except Exception as e:
        print(f"Error while fetching data: {e}")
        return []
    finally:
        if conn:
            conn.close()


def _print_rows(title: str, rows: List[Dict[str, Any]]):
    """Pretty print results."""
    print(f"\n===== {title} =====")
    if not rows:
        print("No data found.")
        return
    for i, row in enumerate(rows, start=1):
        print(f"{i}. {row}")


# ---------------------------------------------------------
# TABLE FETCHERS
# ---------------------------------------------------------
def fetch_actors():
    rows = _fetch_all("SELECT * FROM public.actors;")
    _print_rows("ACTORS", rows)
    return rows


def fetch_actsin():
    rows = _fetch_all("SELECT * FROM public.actsin;")
    _print_rows("ACTSIN", rows)
    return rows


def fetch_customers():
    rows = _fetch_all("SELECT * FROM public.customers;")
    _print_rows("CUSTOMERS", rows)
    return rows


def fetch_log_activity():
    rows = _fetch_all("SELECT * FROM public.log_activity;")
    _print_rows("LOG_ACTIVITY", rows)
    return rows


def fetch_movies():
    rows = _fetch_all("SELECT * FROM public.movies;")
    _print_rows("MOVIES", rows)
    return rows


def fetch_rentings():
    rows = _fetch_all("SELECT * FROM public.rentings;")
    _print_rows("RENTINGS", rows)
    return rows


def fetch_view_actor_summary():
    rows = _fetch_all("SELECT * FROM public.view_actor_summary;")
    _print_rows("VIEW_ACTOR_SUMMARY", rows)
    return rows


# ---------------------------------------------------------
# PRINTER FUNCTIONS (Separated per table)
# ---------------------------------------------------------
def print_database_actors():
    fetch_actors()


def print_database_actsin():
    fetch_actsin()


def print_database_customers():
    fetch_customers()


def print_database_log_activity():
    fetch_log_activity()


def print_database_movies():
    fetch_movies()


def print_database_rentings():
    fetch_rentings()


def print_database_view_actor_summary():
    fetch_view_actor_summary()



# ---------------------------------------------------------
# MENU
# ---------------------------------------------------------
def show_menu():
    print("\n=== SELECT DATABASE TO DISPLAY ===")
    print("1. Actors")
    print("2. Actsin")
    print("3. Customers")
    print("4. Log Activity")
    print("5. Movies")
    print("6. Rentings")
    print("7. View Actor Summary")
    print("0. Exit")


if __name__ == "__main__":
    show_menu()
    choice = input("\nEnter your choice: ")

    if choice == "1":
        print_database_actors()
    elif choice == "2":
        print_database_actsin()
    elif choice == "3":
        print_database_customers()
    elif choice == "4":
        print_database_log_activity()
    elif choice == "5":
        print_database_movies()
    elif choice == "6":
        print_database_rentings()
    elif choice == "7":
        print_database_view_actor_summary()
    elif choice == "0":
        print("Exiting...")
    else:
        print("Invalid option, try again.")


