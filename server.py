import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DBNAME = os.getenv("DBNAME")
SSLMODE = os.getenv("SSLMODE", "require")


def get_connection():
    return psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME,
        sslmode=SSLMODE
    )

# ---------------------------------------------------------
# GENERIC FETCH FUNCTION
# ---------------------------------------------------------


def _fetch_all(query: str) -> List[Dict[str, Any]]:
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
    print(f"\n===== {title} =====")
    if not rows:
        print("No data found.")
        return
    for i, row in enumerate(rows, start=1):
        print(f"{i}. {row}")


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
# TASK 3 - WHERE CLAUSE
# ---------------------------------------------------------


def fetch_task3_movies_after_2015():
    rows = _fetch_all(
        "SELECT * FROM public.movies WHERE <MOVIE_YEAR_COLUMN> > 2015;")
    _print_rows("TASK3_MOVIES_AFTER_2015", rows)
    return rows


def fetch_task3_customers_from_canada():
    rows = _fetch_all(
        "SELECT * FROM public.customers WHERE <CUSTOMER_COUNTRY_COLUMN> = 'Canada';")
    _print_rows("TASK3_CUSTOMERS_FROM_CANADA", rows)
    return rows


def fetch_task3_rentings_rating_ge_4():
    rows = _fetch_all(
        "SELECT * FROM public.rentings WHERE <RENTING_RATING_COLUMN> >= 4;")
    _print_rows("TASK3_RENTINGS_RATING_GE_4", rows)
    return rows


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


def print_task3_movies_after_2015():
    fetch_task3_movies_after_2015()


def print_task3_customers_from_canada():
    fetch_task3_customers_from_canada()


def print_task3_rentings_rating_ge_4():
    fetch_task3_rentings_rating_ge_4()


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
    print("8. Task 3 - Movies after 2015")
    print("9. Task 3 - Customers from Canada")
    print("10. Task 3 - Rentings rating >= 4")

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
    elif choice == "8":
        print_task3_movies_after_2015()
    elif choice == "9":
        print_task3_customers_from_canada()
    elif choice == "10":
        print_task3_rentings_rating_ge_4()
    elif choice == "0":
        print("Exiting...")
    else:
        print("Invalid option, try again.")

# Task 1 – Generic Function


def run_query(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()

# Task 2 – SELECT queries
# ...

# Task 3 – WHERE
# ...

# Task 4 – Aggregations
# ...

# ============================
# Task 5 – GROUP BY
# ============================


query_movies_per_genre = """
SELECT genre, COUNT(*) 
FROM movies
GROUP BY genre;
"""

result = run_query( cursor, query_movies_per_genre)

for row in result:
    print(f"Genre: {row[0]} | Movie Count: {row[1]}")
