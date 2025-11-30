import psycopg2

def fetch_actsin():
    try:
        # Connect to your PostgreSQL database
        connection = psycopg2.connect(
            dbname="database_name",
            user="username",
            password="password",
            host="host",
            port="port"
        )
        
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

# Call the function
fetch_actsin()
