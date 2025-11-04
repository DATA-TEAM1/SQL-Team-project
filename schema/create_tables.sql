-- schema/create_tables.sql
-- Create base tables for the movie database.
-- TODO: Adjust data types to match your chosen SQL dialect (recommended: PostgreSQL).

-- Example tables (adapt names/types as needed)
CREATE TABLE IF NOT EXISTS genres (
  genre_id SERIAL PRIMARY KEY,
  genre_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS directors (
  director_id SERIAL PRIMARY KEY,
  director_name VARCHAR(150) NOT NULL
);

CREATE TABLE IF NOT EXISTS actors (
  actor_id SERIAL PRIMARY KEY,
  actor_name VARCHAR(150) NOT NULL
);

CREATE TABLE IF NOT EXISTS movies (
  movie_id SERIAL PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  release_year INT,
  duration INT,
  genre_id INT,
  director_id INT,
  avg_rating NUMERIC(4,2) DEFAULT 0,
  review_count INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS reviews (
  review_id SERIAL PRIMARY KEY,
  movie_id INT NOT NULL,
  reviewer_id INT,
  stars INT NOT NULL,
  rating NUMERIC(4,2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS actsin (
  movie_id INT NOT NULL,
  actor_id INT NOT NULL,
  role_name VARCHAR(150),
  PRIMARY KEY (movie_id, actor_id)
);
