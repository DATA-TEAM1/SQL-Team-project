Overview

This repository includes a Python script called server.py that connects to a Supabase PostgreSQL database and allows the user to interactively display data from several tables and a view via a simple command-line menu.

The script:
Loads database credentials from a local .env file
Opens a connection to the Supabase Postgres database
Fetches rows from specific tables and a view
Prints the results in a readable, numbered format in the terminal
Provides a text menu so the user can choose what to display

Technologies Used

Python 3
psycopg2 — PostgreSQL database adapter for Python
psycopg2.extras.RealDictCursor — returns query results as dictionaries
python-dotenv — loads environment variables from a .env file
Supabase PostgreSQL as the database backend

Environment Configuration (.env)
The script reads database connection values from a .env file using python-dotenv.
These variables must be defined in your .env file:

user=your_db_user
password=your_db_password
host=your_db_host
port=5432
dbname=your_db_name
sslmode=require


user – database user (defined but not directly passed in the current connection call)
password – database password
host – database host (Supabase host URL)
port – database port (default 5432)
dbname – database name
sslmode – SSL mode, typically require for Supabase
The .env file should be in the same directory as server.py and must not be committed to GitHub.

Database Connection

The function get_connection() is responsible for opening a connection to the Supabase PostgreSQL database using the values from the .env file:

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
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME,
        sslmode=SSLMODE
    )
    return conn


If the connection fails, the exception is handled in the fetch helper and an error message is printed to the console.

Data Fetching Logic
All SELECT operations go through a generic helper function:

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


Opens a connection using get_connection()
Executes the provided SELECT query
Returns all rows as a list of dictionaries thanks to RealDictCursor
Closes the connection in the finally block, even if an error occurs
There is also a small printer helper:

def _print_rows(title: str, rows: List[Dict[str, Any]]):
    """ print results."""
    print(f"\n===== {title} =====")
    if not rows:
        print("No data found.")
        return
    for i, row in enumerate(rows, start=1):
        print(f"{i}. {row}")


This prints a section header and then each row with a numbered index.
Table & View Fetch Functions
The script defines specific functions to fetch from each table or view:

fetch_actors() → SELECT * FROM public.actors;

fetch_actsin() → SELECT * FROM public.actsin;

fetch_customers() → SELECT * FROM public.customers;

fetch_log_activity() → SELECT * FROM public.log_activity;

fetch_movies() → SELECT * FROM public.movies;

fetch_rentings() → SELECT * FROM public.rentings;

fetch_view_actor_summary() → SELECT * FROM public.view_actor_summary;

Each of these:

Calls _fetch_all(<table_or_view_query>)
Prints the results with _print_rows(...)
Returns the list of rows for further use if needed

Example:

def fetch_movies():
    rows = _fetch_all("SELECT * FROM public.movies;")
    _print_rows("MOVIES", rows)
    return rows

Printer Wrapper Functions
For each table/view there is a corresponding printer function that simply calls the fetcher:

print_database_actors() → fetch_actors()
print_database_actsin() → fetch_actsin()
print_database_customers() → fetch_customers()
print_database_log_activity() → fetch_log_activity()
print_database_movies() → fetch_movies()
print_database_rentings() → fetch_rentings()
print_database_view_actor_summary() → fetch_view_actor_summary()

These are used by the menu in the main block.

Interactive Menu (CLI)
When server.py is executed directly, it shows a text-based menu:

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

The user is then prompted for a choice:

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


So, running the script lets the user:

Choose which table or view to display
Automatically fetch and print all rows from that source

Exit by choosing 0

How to Run the Script
1. Install Dependencies
pip install psycopg2 python-dotenv

If you are using Windows and psycopg2 gives build issues, you may need psycopg2-binary instead:
pip install psycopg2-binary python-dotenv

2. Set Up .env
Create a .env file in the same directory as server.py and add your Supabase database credentials:

user=your_db_user
password=your_db_password
host=your_db_host
port=5432
dbname=your_db_name
sslmode=require

3. Run the Script
From the project folder:

python server.py

You will see the menu:

=== SELECT DATABASE TO DISPLAY ===
1. Actors
2. Actsin
3. Customers
4. Log Activity
5. Movies
6. Rentings
7. View Actor Summary
0. Exit

Enter a number (e.g. 5) to display that table’s content in the console.

Role in the SQL Team Project

This script is part of the SQL Team Project and serves as a Python command-line viewer for the Supabase database.
It allows team members to quickly inspect data from the main tables and the view_actor_summary view without writing SQL manually each time
