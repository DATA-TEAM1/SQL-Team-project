-- features/functions.sql
-- Part 4 – Stored Functions (Nadya)
-- PostgreSQL syntax example. Adjust for your dialect if needed.

-- 1) get_actor_avg_rating(actor_id) → numeric
CREATE OR REPLACE FUNCTION get_actor_avg_rating(p_actor_id INT)
RETURNS NUMERIC(4,2) AS $$
DECLARE v_avg NUMERIC(4,2);
BEGIN
  SELECT COALESCE(AVG(m.avg_rating),0)
    INTO v_avg
  FROM actsin ai
  JOIN movies m ON m.movie_id = ai.movie_id
  WHERE ai.actor_id = p_actor_id;

  RETURN v_avg;
END;
$$ LANGUAGE plpgsql;

-- 2) get_genre_top_movie(genre_name) → return TABLE (title, avg_rating)
CREATE OR REPLACE FUNCTION get_genre_top_movie(p_genre_name TEXT)
RETURNS TABLE(title TEXT, avg_rating NUMERIC(4,2)) AS $$
BEGIN
  RETURN QUERY
  SELECT m.title, m.avg_rating
  FROM movies m
  JOIN genres g ON g.genre_id = m.genre_id
  WHERE g.genre_name = p_genre_name
  ORDER BY m.avg_rating DESC NULLS LAST, m.review_count DESC
  LIMIT 1;
END;
$$ LANGUAGE plpgsql;

-- USAGE EXAMPLES:
-- SELECT get_actor_avg_rating(1);
-- SELECT * FROM get_genre_top_movie('Action');
