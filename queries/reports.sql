-- queries/reports.sql
-- Part 6 – Reports (Abanoub)

-- Top 3 genres by total reviews
SELECT g.genre_name, SUM(m.review_count) AS total_reviews
FROM genres g
JOIN movies m ON m.genre_id = g.genre_id
GROUP BY g.genre_name
ORDER BY total_reviews DESC NULLS LAST
LIMIT 3;

-- Top 5 actors by total appearances
SELECT a.actor_name, COUNT(*) AS appearances
FROM actsin ai
JOIN actors a ON a.actor_id = ai.actor_id
GROUP BY a.actor_name
ORDER BY appearances DESC, a.actor_name
LIMIT 5;

-- Director performance by average movie rating
SELECT d.director_name, COALESCE(AVG(m.avg_rating),0) AS avg_rating, COUNT(*) AS movies_count
FROM directors d
JOIN movies m ON m.director_id = d.director_id
GROUP BY d.director_name
ORDER BY avg_rating DESC NULLS LAST, movies_count DESC;
