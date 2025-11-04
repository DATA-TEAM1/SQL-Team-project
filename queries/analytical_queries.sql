-- queries/analytical_queries.sql
-- Part 5 – Analytical Queries (Nelson)
-- Add a purpose comment above each query.

-- 1) Top 5 movies by rating (title, genre, director)
-- Purpose: Rank best movies by computed avg_rating.
SELECT m.title, g.genre_name, d.director_name, m.avg_rating
FROM movies m
JOIN genres g ON g.genre_id = m.genre_id
JOIN directors d ON d.director_id = m.director_id
ORDER BY m.avg_rating DESC NULLS LAST, m.review_count DESC
LIMIT 5;

-- 2) Count how many movies each actor has acted in.
SELECT a.actor_name, COUNT(DISTINCT ai.movie_id) AS movie_count
FROM actors a
LEFT JOIN actsin ai ON ai.actor_id = a.actor_id
GROUP BY a.actor_name
ORDER BY movie_count DESC, a.actor_name;

-- Add remaining queries following the examples in the assignment...
