-- 1. Top 3 genres by total reviews
SELECT
    m.genre,
    COUNT(r.renting_id) AS total_reviews
FROM
    public.movies m
JOIN
    public.rentings r ON m.movie_id = r.movie_id
GROUP BY
    m.genre
ORDER BY
    total_reviews DESC
LIMIT 3;

-- 2. Top 5 actors by total appearances
SELECT
    a.name,
    COUNT(ai.movie_id) AS total_appearances
FROM
    public.actors a
JOIN
    public.actsin ai ON a.actor_id = ai.actor_id
GROUP BY
    a.name
ORDER BY
    total_appearances DESC
LIMIT 5;

-- 3. Director performance by average movie rating
SELECT
    d.name,
    AVG(m.avg_rating) AS average_rating
FROM
    public.directors d
JOIN
    public.movies m ON d.director_id = m.director_id
GROUP BY
    d.name
HAVING
    COUNT(m.movie_id) >= 2
ORDER BY
    average_rating DESC;

/*
--------------------------------------------------------------------------------
7. PROJECT DOCUMENTATION SUMMARY
--------------------------------------------------------------------------------

PROJECT TEAM:
    - Andrii Platonov01 (Developer/Database Engineer)

A. TABLES AND RELATIONSHIPS:
    The schema defines tables for:
    1. public.movies: Stores movie details (title, year, director_id).
    2. public.directors: Stores director names.
    3. public.actors: Stores actor names.
    4. public.actsin: Junction table for M:N relationship between movies and actors.
    5. public.rentings: Stores customer rentals and movie reviews (rating, review_date).
    6. public.customers: Stores customer details.

    Key relationships (via FOREIGN KEY constraints):
    - movies to directors (1:N)
    - rentings to movies (N:1)
    - rentings to customers (N:1)
    - actsin to movies (N:1)
    - actsin to actors (N:1)

B. FEATURES SUMMARY:

    1. TRIGGERS (Part 2):
        - update_movie_avg_rating: An AFTER INSERT, UPDATE, or DELETE trigger on the public.rentings table.
        - Purpose: Automatically recalculates the 'avg_rating' column in the public.movies table whenever a new rating is added, modified, or removed, ensuring rating data integrity.

    2. VIEWS (Part 3):
        - highly_rated_movies: Shows movies with an average rating >= 4.0.
        - customer_activity_summary: Provides a summary of total rented movies per customer.

    3. FUNCTIONS/PROCEDURES (Part 3):
        - get_movies_by_genre(VARCHAR): Function to easily retrieve a list of movies belonging to a specified genre.
        - update_rental_price(INT, NUMERIC): Procedure to update the renting price of a specific movie using a price multiplier.

C. ANALYTICAL QUERIES (Part 4 & 6):

    Part 4 (Analytical Queries):
    - Query 1 (Window Function): Demonstrates how a movie's individual rating compares to the average rating of all movies released in the same year, using the AVG() OVER (PARTITION BY) window function.
    - Query 2 (CTE/Subquery): Identifies actors based on their total number of movie appearances and compares this count against the overall average number of appearances per actor.

    Part 6 (Summary Reports):
    - Report 1: Lists the top 3 genres based on the total number of reviews received.
    - Report 2: Lists the top 5 actors based on the total number of film appearances.
    - Report 3: Measures and ranks director performance based on the average rating of the movies they have directed (minimum 2 movies required).

--------------------------------------------------------------------------------
*/
