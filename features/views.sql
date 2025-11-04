-- features/views.sql
-- Part 3 – Views (Krishma)
-- Include DROP VIEW IF EXISTS before creation.

DROP VIEW IF EXISTS view_movie_summary;
CREATE VIEW view_movie_summary AS
SELECT
  m.movie_id,
  m.title,
  g.genre_name AS genre,
  d.director_name AS director,
  m.avg_rating,
  m.review_count
FROM movies m
LEFT JOIN genres g ON g.genre_id = m.genre_id
LEFT JOIN directors d ON d.director_id = m.director_id;

DROP VIEW IF EXISTS view_actor_summary;
CREATE VIEW view_actor_summary AS
SELECT
  a.actor_id,
  a.actor_name,
  COUNT(DISTINCT ai.movie_id) AS movie_count,
  COALESCE(AVG(m.avg_rating),0) AS avg_movie_rating
FROM actors a
LEFT JOIN actsin ai ON ai.actor_id = a.actor_id
LEFT JOIN movies m ON m.movie_id = ai.movie_id
GROUP BY a.actor_id, a.actor_name;

DROP VIEW IF EXISTS view_genre_stats;
CREATE VIEW view_genre_stats AS
SELECT
  g.genre_id,
  g.genre_name,
  COUNT(DISTINCT m.movie_id) AS total_movies,
  COALESCE(AVG(m.avg_rating),0) AS avg_genre_rating
FROM genres g
LEFT JOIN movies m ON m.genre_id = g.genre_id
GROUP BY g.genre_id, g.genre_name;
