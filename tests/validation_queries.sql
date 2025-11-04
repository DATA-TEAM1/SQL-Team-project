-- tests/validation_queries.sql
-- Quick checks to validate constraints and views.

-- Should fail: stars out of range
-- INSERT INTO reviews (movie_id, reviewer_id, stars, rating) VALUES (1, 999, 6, 9.0);

-- Should fail: release year < 1900
-- INSERT INTO movies (title, release_year) VALUES ('Ancient', 1800);

-- View samples
SELECT * FROM view_movie_summary LIMIT 10;
SELECT * FROM view_actor_summary LIMIT 10;
SELECT * FROM view_genre_stats LIMIT 10;

-- Function samples (PostgreSQL)
-- SELECT get_actor_avg_rating(1);
-- SELECT * FROM get_genre_top_movie('Action');
