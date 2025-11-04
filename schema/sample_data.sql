-- schema/sample_data.sql
-- Minimal sample data for testing.

INSERT INTO genres (genre_name) VALUES
  ('Action'), ('Comedy'), ('Drama'), ('Sci-Fi')
ON CONFLICT DO NOTHING;

INSERT INTO directors (director_name) VALUES
  ('Jane Doe'), ('John Smith'), ('Ava Lee')
ON CONFLICT DO NOTHING;

INSERT INTO actors (actor_name) VALUES
  ('Actor One'), ('Actor Two'), ('Actor Three'), ('Actor Four')
ON CONFLICT DO NOTHING;

INSERT INTO movies (title, release_year, duration, genre_id, director_id) VALUES
  ('Alpha', 2010, 110, 1, 1),
  ('Beta', 2015, 100, 2, 2),
  ('Gamma', 2018, 95, 3, 2),
  ('Delta', 2020, 125, 4, 3);

INSERT INTO actsin (movie_id, actor_id, role_name) VALUES
  (1, 1, 'Lead'),
  (1, 2, 'Support'),
  (2, 2, 'Lead'),
  (3, 3, 'Lead'),
  (4, 4, 'Lead');

INSERT INTO reviews (movie_id, reviewer_id, stars, rating) VALUES
  (1, 101, 5, 9.2),
  (1, 102, 4, 8.0),
  (2, 103, 3, 6.5);
