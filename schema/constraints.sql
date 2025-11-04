-- schema/constraints.sql
-- Part 1 – Relationships & Constraints (Andreii)
-- Add foreign keys, checks, unique constraints, and NOT NULL rules.

-- Foreign keys with delete behavior
ALTER TABLE movies
  ADD CONSTRAINT fk_movies_genre
  FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
  ON DELETE SET NULL;

ALTER TABLE movies
  ADD CONSTRAINT fk_movies_director
  FOREIGN KEY (director_id) REFERENCES directors(director_id)
  ON DELETE SET NULL;

ALTER TABLE reviews
  ADD CONSTRAINT fk_reviews_movie
  FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
  ON DELETE CASCADE;

ALTER TABLE actsin
  ADD CONSTRAINT fk_actsin_movie
  FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
  ON DELETE CASCADE;

ALTER TABLE actsin
  ADD CONSTRAINT fk_actsin_actor
  FOREIGN KEY (actor_id) REFERENCES actors(actor_id)
  ON DELETE CASCADE;

-- CHECK constraints
ALTER TABLE reviews
  ADD CONSTRAINT chk_reviews_stars CHECK (stars BETWEEN 1 AND 5);

ALTER TABLE reviews
  ADD CONSTRAINT chk_reviews_rating CHECK (rating BETWEEN 0 AND 10);

ALTER TABLE movies
  ADD CONSTRAINT chk_movies_release_year CHECK (release_year >= 1900);

-- Unique movie title per year
ALTER TABLE movies
  ADD CONSTRAINT uq_movies_title_year UNIQUE (title, release_year);

-- NOT NULL / non-empty names
ALTER TABLE actors
  ALTER COLUMN actor_name SET NOT NULL;
