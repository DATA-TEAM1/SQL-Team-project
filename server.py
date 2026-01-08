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

# -------------------------------------------------------
# GENERIC FETCH FUNCTION
# -------------------------------------------------------


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

# ============================
# Task 1 – Generic Function
# ============================


def run_query(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()

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

# ============================
# TASK 3 - WHERE CLAUSE
# ============================


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

# ============================
# Task 4 – Aggregation Functions
# ============================


def get_total_movies():
    query = """
    SELECT COUNT(movie_id) AS total_movies
    FROM movies;
    """
    return run_query(query)


def get_average_renting_price():
    query = """
    SELECT AVG(renting_price) AS average_renting_price
    FROM movies;
    """
    return run_query(query)


def get_average_rating():
    query = """
    SELECT AVG(rating) AS average_rating
    FROM rentings;
    """
    return run_query(query)

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
# Task 6 –  JOIN Queries
# ============================

# ============================
# Task 7 –  HAVING Clause
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


# ============================
# Task 8 –  Output Formatting
# ============================

# ============================
# Task 9 –  Error Handling
# ============================

# ============================
# Task Bonus –
# ============================

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


if __name__ == "__main__":
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    print("\n=== Task 5.1: Number of movies per genre ===")
for row in get_number_of_movies_per_genre(cursor):
    print(f"Genre: {row['genre']} | Movie Count: {row['movie_count']}")

print("\n=== Task 5.2: Number of customers per country ===")
for row in get_number_of_customers_per_country(cursor):
    print(
        f"Country: {row['country']} | Customer Count: {row['customer_count']}")

print("\n=== Task 5.3: Number of rentings per movie ===")
for row in get_number_of_rentings_per_movie(cursor):
    print(f"Movie: {row['title']} | Rentings: {row['renting_count']}")
