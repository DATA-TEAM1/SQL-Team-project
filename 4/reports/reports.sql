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
