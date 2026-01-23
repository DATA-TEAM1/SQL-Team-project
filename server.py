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
            return run_query(cur, query)   
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
    """
    Task 4.1
    Return total number of movies.
    """
    query = """
    SELECT COUNT(movie_id) AS total_movies
    FROM movies;
    """
    return run_query(cursor, query)


def get_total_customers(cursor):
    """
    Task 4.2
    Return total number of customers.
    """
    query = """
    SELECT COUNT(customer_id) AS total_customers
    FROM customers;
    """
    return run_query(cursor, query)


def get_average_movie_rating(cursor):
    """
    Task 4.3
    Return average rating (NULL ratings ignored).
    """
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
# Task 6 –  JOIN Queries
# ============================
    
def get_movies_with_avg_rating(cursor):
    """
    Task 6.1: Movie titles with their average rating.
    """
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
    """
    Task 6.2: Number of movies each actor acted in.
    """
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
    """
    Task 6.3: Number of movies rented by each customer.
    """
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

def task8_output_formatting():
    """
    Task 8: formatted output (safe to import).
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT genre, COUNT(movie_id) AS movie_count
        FROM movies
        GROUP BY genre
        """

        cursor.execute(query)
        results = cursor.fetchall()

        for row in results:
            genre = row[0]
            movie_count = row[1]
            print(f"Genre: {genre} | Movie Count: {movie_count}")

    except Exception as e:
        print(f"Task 8 error: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ============================
# Task 9 –  Error Handling
# ============================

# ============================
# Task Bonus –
# ============================
import time

def bonus_top_5_genres_to_file(output_file: str = "bonus_task_output.txt"):
    """
    Bonus: top 5 genres + execution time written to a file (safe to import).
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        start_time = time.time()

        query = """
        SELECT genre, COUNT(movie_id) AS movie_count
        FROM movies
        GROUP BY genre
        ORDER BY movie_count DESC
        LIMIT 5
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        end_time = time.time()
        execution_time = end_time - start_time

        # Convert results into dictionaries (manual, no pandas)
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in rows]

        with open(output_file, "w") as file:
            for row in results:
                file.write(f"Genre: {row['genre']} | Movie Count: {row['movie_count']}\n")
            file.write(f"\nQuery Execution Time: {execution_time:.6f} seconds\n")

        print(f"Saved bonus output to: {output_file}")

    except Exception as e:
        print(f"Bonus task error: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

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

    print("11. Task 5.1 - Number of movies per genre")
    print("12. Task 5.2 - Number of customers per country")
    print("13. Task 5.3 - Number of rentings per movie")

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


def print_task5_movies_per_genre():
    print("\n=== Task 5.1: Number of movies per genre ===")
    conn = None
    try:
        conn = get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            for row in get_number_of_movies_per_genre(cur):
                print(f"Genre: {row['genre']} | Movie Count: {row['movie_count']}")
    except Exception as e:
        print(f"Error while fetching Task 5.1: {e}")
    finally:
        if conn:
            conn.close()


def print_task5_customers_per_country():
    print("\n=== Task 5.2: Number of customers per country ===")
    conn = None
    try:
        conn = get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            for row in get_number_of_customers_per_country(cur):
                print(f"Country: {row['country']} | Customer Count: {row['customer_count']}")
    except Exception as e:
        print(f"Error while fetching Task 5.2: {e}")
    finally:
        if conn:
            conn.close()


def print_task5_rentings_per_movie():
    print("\n=== Task 5.3: Number of rentings per movie ===")
    conn = None
    try:
        conn = get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            for row in get_number_of_rentings_per_movie(cur):
                print(f"Movie: {row['title']} | Rentings: {row['renting_count']}")
    except Exception as e:
        print(f"Error while fetching Task 5.3: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    query = "SELECT * FROM movies;"
    result = run_query(cursor, query)

    print("=== MOVIES ===")
    for movie in get_all_movies(cursor):
        print(movie)

    print("\n=== CUSTOMERS ===")
    for customer in get_all_customers(cursor):
        print(customer)

    print("\n=== ACTORS ===")
    for actor in get_all_actors(cursor):
        print(actor)

    print("\n=== Task 7.1: Genres with more than 3 movies ===")
    for row in get_genres_with_more_than_3_movies(cursor):
        print(row)

    print("\n=== Task 7.2: Movies with avg rating above 4 ===")
    for row in get_movies_with_avg_rating_above_4(cursor):
        print(row)

    print("\n=== Task 7.3: Customers with more than 5 rentals ===")
    for row in get_customers_with_more_than_5_rentals(cursor):
        print(row)

    for row in result:
        print(row)

    cursor.close()
    conn.close()

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

    elif choice == "11":
        print_task5_movies_per_genre()
    elif choice == "12":
        print_task5_customers_per_country()
    elif choice == "13":
        print_task5_rentings_per_movie()

    elif choice == "0":
        print("Exiting...")
    else:
        print("Invalid option, try again.")