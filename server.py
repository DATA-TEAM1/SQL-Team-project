import os
import time
import json
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional, Iterable, Tuple

import psycopg2
from psycopg2 import Error as PsycopgError
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

# -------------------------------------------------------------------
# DB CONFIG
# -------------------------------------------------------------------
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DBNAME = os.getenv("DBNAME")
SSLMODE = os.getenv("SSLMODE", "require")

# Bonus: show query time by default if env var is set to "1"
SHOW_QUERY_TIME = os.getenv("SHOW_QUERY_TIME", "0") == "1"

# Bonus: keep last results in memory so we can export them
_LAST_RESULT: List[Dict[str, Any]] = []


def _require_env():
    missing = [k for k, v in {
        "USER": USER,
        "PASSWORD": PASSWORD,
        "HOST": HOST,
        "PORT": PORT,
        "DBNAME": DBNAME,
    }.items() if not v]
    if missing:
        raise ValueError(
            "Missing required .env variables: "
            + ", ".join(missing)
            + ". Please set them in your .env file."
        )


def get_connection():
    """Create and return a DB connection."""
    _require_env()
    return psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME,
        sslmode=SSLMODE,
    )


# -------------------------------------------------------
# Task 1 – Generic Function (all queries go through here)
# -------------------------------------------------------
def run_query(cursor, query):
    """
    Executes ANY SQL query and returns results for SELECT queries.

    Task 9 requirement:
    - If SQL is invalid, catch exception, print friendly message, and do NOT crash.
    """
    global _LAST_RESULT

    start = time.perf_counter()
    try:
        cursor.execute(query)

        # For SELECT queries: cursor.description is not None
        if cursor.description is not None:
            rows = cursor.fetchall()

            # Ensure plain dicts (RealDictRow -> dict)
            _LAST_RESULT = [dict(r) for r in rows]

            if SHOW_QUERY_TIME:
                elapsed_ms = (time.perf_counter() - start) * 1000
                print(f"[Query time: {elapsed_ms:.2f} ms]")

            return _LAST_RESULT

        # Non-SELECT query (INSERT/UPDATE/DELETE/DDL)
        cursor.connection.commit()
        _LAST_RESULT = []
        return []

    except PsycopgError as e:
        # Rollback so the connection stays usable after an error
        try:
            cursor.connection.rollback()
        except Exception:
            pass

        # Friendly message (pgerror can be None)
        msg = getattr(e, "pgerror", None) or str(e)
        print("\n[SQL ERROR] Your query could not be executed.")
        print(f"Details: {msg.strip()}")
        _LAST_RESULT = []
        return []

    except Exception as e:
        try:
            cursor.connection.rollback()
        except Exception:
            pass
        print("\n[ERROR] Unexpected error while executing query.")
        print(f"Details: {e}")
        _LAST_RESULT = []
        return []


# -------------------------------------------------------
# Generic fetch function (keeps the style used in your file)
# -------------------------------------------------------
def _fetch_all(query: str) -> List[Dict[str, Any]]:
    conn = None
    try:
        conn = get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            return run_query(cur, query)
    finally:
        if conn:
            conn.close()


# ============================
# Task 8 – Output Formatting
# ============================
def _format_value(v: Any) -> str:
    if v is None:
        return "NULL"
    if isinstance(v, float):
        return f"{v:.2f}"
    return str(v)


def _print_rows(title: str, rows: List[Dict[str, Any]], max_rows: int = 20) -> None:
    """Pretty, labeled printing for any list of dict rows."""
    print(f"\n===== {title} =====")
    if not rows:
        print("No data found.")
        return

    # Print up to max_rows rows (avoid flooding terminal)
    to_show = rows[:max_rows]
    for i, row in enumerate(to_show, start=1):
        parts = [f"{k}: {_format_value(v)}" for k, v in row.items()]
        print(f"{i}. " + " | ".join(parts))

    if len(rows) > max_rows:
        print(f"... ({len(rows) - max_rows} more rows not shown)")


# -------------------------------------------------------
# Task Bonus – Save last results to a file
# -------------------------------------------------------
def save_last_result_json(filepath: str = "last_result.json") -> None:
    if not _LAST_RESULT:
        print("No last result to save.")
        return
    Path(filepath).write_text(json.dumps(_LAST_RESULT, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved last result to {filepath}")


def save_last_result_csv(filepath: str = "last_result.csv") -> None:
    if not _LAST_RESULT:
        print("No last result to save.")
        return
    headers = sorted({k for row in _LAST_RESULT for k in row.keys()})
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(_LAST_RESULT)
    print(f"Saved last result to {filepath}")


# ============================
# Task 2 – SELECT queries
# ============================
def get_all_movies(cursor):
    query = "SELECT * FROM movies;"
    return run_query(cursor, query)


def get_all_customers(cursor):
    query = "SELECT * FROM customers;"
    return run_query(cursor, query)


def get_all_actors(cursor):
    query = "SELECT * FROM actors;"
    return run_query(cursor, query)


# ---------------------------------------------------------
# Convenience fetchers (already used by your menu)
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


# ============================
# Task 3 – WHERE Clause
# ============================
def fetch_task3_movies_after_2015():
    rows = _fetch_all("SELECT * FROM public.movies WHERE year_of_release > 2015;")
    _print_rows("TASK3_MOVIES_AFTER_2015", rows)
    return rows


def fetch_task3_customers_from_canada():
    rows = _fetch_all("SELECT * FROM public.customers WHERE country = 'Canada';")
    _print_rows("TASK3_CUSTOMERS_FROM_CANADA", rows)
    return rows


def fetch_task3_rentings_rating_ge_4():
    rows = _fetch_all("SELECT * FROM public.rentings WHERE rating >= 4;")
    _print_rows("TASK3_RENTINGS_RATING_GE_4", rows)
    return rows


# ============================
# Task 4 – Aggregation Functions
# ============================
def get_total_movies(cursor):
    query = """
    SELECT COUNT(movie_id) AS total_movies
    FROM movies;
    """
    return run_query(cursor, query)


def get_total_customers(cursor):
    query = """
    SELECT COUNT(customer_id) AS total_customers
    FROM customers;
    """
    return run_query(cursor, query)


def get_average_movie_rating(cursor):
    query = """
    SELECT AVG(rating) AS avg_rating
    FROM rentings
    WHERE rating IS NOT NULL;
    """
    return run_query(cursor, query)


# ============================
# Task 5 – GROUP BY
# ============================
def get_number_of_movies_per_genre(cursor):
    query = """
    SELECT
        genre,
        COUNT(movie_id) AS movie_count
    FROM movies
    GROUP BY genre
    ORDER BY movie_count DESC;
    """
    return run_query(cursor, query)


def get_number_of_customers_per_country(cursor):
    query = """
    SELECT
        country,
        COUNT(customer_id) AS customer_count
    FROM customers
    GROUP BY country
    ORDER BY customer_count DESC;
    """
    return run_query(cursor, query)


def get_number_of_rentings_per_movie(cursor):
    query = """
    SELECT
        m.title,
        COUNT(r.renting_id) AS renting_count
    FROM movies m
    JOIN rentings r
        ON r.movie_id = m.movie_id
    GROUP BY m.title
    ORDER BY renting_count DESC;
    """
    return run_query(cursor, query)


# ============================
# Task 6 – JOIN Queries
# ============================
def get_movies_with_avg_rating(cursor):
    query = """
    SELECT
      movie_id,
      title,
      avg_rating
    FROM movies
    ORDER BY avg_rating DESC NULLS LAST;
    """
    return run_query(cursor, query)


def get_actors_with_movie_count(cursor):
    query = """
    SELECT
      a.actor_id,
      a.name AS actor_name,
      COUNT(ac.movie_id) AS movie_count
    FROM actors a
    LEFT JOIN actsin ac ON ac.actor_id = a.actor_id
    GROUP BY a.actor_id, a.name
    ORDER BY movie_count DESC;
    """
    return run_query(cursor, query)


def get_customers_with_rentals_count(cursor):
    query = """
    SELECT
      c.customer_id,
      c.name AS customer_name,
      COUNT(r.renting_id) AS rentals_count
    FROM customers c
    LEFT JOIN rentings r ON r.customer_id = c.customer_id
    GROUP BY c.customer_id, c.name
    ORDER BY rentals_count DESC;
    """
    return run_query(cursor, query)


# ============================
# Task 7 – HAVING Clause
# ============================
def get_genres_with_more_than_3_movies(cursor):
    query = """
    SELECT
        genre,
        COUNT(movie_id) AS total_movies
    FROM movies
    GROUP BY genre
    HAVING COUNT(movie_id) > 3
    ORDER BY total_movies DESC;
    """
    return run_query(cursor, query)


def get_movies_with_avg_rating_above_4(cursor):
    query = """
    SELECT
        movie_id,
        title,
        genre,
        avg_rating
    FROM movies
    GROUP BY movie_id, title, genre, avg_rating
    HAVING avg_rating > 4
    ORDER BY avg_rating DESC;
    """
    return run_query(cursor, query)


def get_customers_with_more_than_5_rentals(cursor):
    query = """
    SELECT
        c.customer_id,
        COUNT(r.renting_id) AS total_rentals
    FROM customers c
    JOIN rentings r
        ON r.customer_id = c.customer_id
    GROUP BY c.customer_id
    HAVING COUNT(r.renting_id) > 5
    ORDER BY total_rentals DESC;
    """
    return run_query(cursor, query)


# ---------------------------------------------------------
# MENU
# ---------------------------------------------------------
def show_menu():
    print("\n=== SELECT DATABASE / TASK ===")
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
    print("11. Task 5.1 - Number of movies per genre")
    print("12. Task 5.2 - Number of customers per country")
    print("13. Task 5.3 - Number of rentings per movie")
    print("14. Bonus - Save last result as JSON")
    print("15. Bonus - Save last result as CSV")
    print("16. Task 9 demo - Run an INVALID query (should not crash)")
    print("0. Exit")


def _task9_invalid_query_demo():
    print("\n=== Task 9 Demo: invalid SQL (should not crash) ===")
    conn = None
    try:
        conn = get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # intentionally wrong table name
            run_query(cur, "SELECT * FROM this_table_does_not_exist;")
    finally:
        if conn:
            conn.close()


def _handle_choice(choice: str) -> bool:
    """Returns True if program should continue, False to exit."""
    if choice == "1":
        fetch_actors()
    elif choice == "2":
        fetch_actsin()
    elif choice == "3":
        fetch_customers()
    elif choice == "4":
        fetch_log_activity()
    elif choice == "5":
        fetch_movies()
    elif choice == "6":
        fetch_rentings()
    elif choice == "7":
        fetch_view_actor_summary()
    elif choice == "8":
        fetch_task3_movies_after_2015()
    elif choice == "9":
        fetch_task3_customers_from_canada()
    elif choice == "10":
        fetch_task3_rentings_rating_ge_4()
    elif choice == "11":
        rows = _fetch_all("""SELECT genre, COUNT(movie_id) AS movie_count
                            FROM movies GROUP BY genre ORDER BY movie_count DESC;""")
        _print_rows("TASK5_MOVIES_PER_GENRE", rows)
    elif choice == "12":
        rows = _fetch_all("""SELECT country, COUNT(customer_id) AS customer_count
                            FROM customers GROUP BY country ORDER BY customer_count DESC;""")
        _print_rows("TASK5_CUSTOMERS_PER_COUNTRY", rows)
    elif choice == "13":
        rows = _fetch_all("""SELECT m.title, COUNT(r.renting_id) AS renting_count
                            FROM movies m JOIN rentings r ON r.movie_id = m.movie_id
                            GROUP BY m.title ORDER BY renting_count DESC;""")
        _print_rows("TASK5_RENTINGS_PER_MOVIE", rows)
    elif choice == "14":
        save_last_result_json()
    elif choice == "15":
        save_last_result_csv()
    elif choice == "16":
        _task9_invalid_query_demo()
    elif choice == "0":
        print("Exiting...")
        return False
    else:
        print("Invalid option, try again.")
    return True


if __name__ == "__main__":
    # Bonus: continuous menu loop (so you don't have to re-run each time)
    while True:
        try:
            show_menu()
            choice = input("\nEnter your choice: ").strip()
            if not _handle_choice(choice):
                break
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            # Final safety net: never crash the CLI
            print(f"\n[ERROR] {e}")
