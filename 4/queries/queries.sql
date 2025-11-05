-- 1. Movie Rating Comparison by Year of Release
SELECT
    title,
    year_of_release,
    avg_rating,
    AVG(avg_rating) OVER (PARTITION BY year_of_release) AS avg_rating_for_year
FROM
    public.movies
ORDER BY
    year_of_release DESC, avg_rating DESC;

-- 2. Actors with the highest number of movies compared to the average
WITH ActorMovieCount AS (
    SELECT
        a.actor_id,
        a.name,
        COUNT(ai.movie_id) AS total_movies
    FROM
        public.actors a
    JOIN
        public.actsin ai ON a.actor_id = ai.actor_id
    GROUP BY
        a.actor_id, a.name
)
SELECT
    amc.name,
    amc.total_movies,
    (SELECT AVG(total_movies) FROM ActorMovieCount) AS average_movies_per_actor
FROM
    ActorMovieCount amc
ORDER BY
    amc.total_movies DESC;
