-- features/triggers.sql
-- Part 2 – Triggers (Samuel)
-- TODO: Adapt syntax to your DB (PostgreSQL example below).

-- 1) Validate stars BEFORE INSERT on reviews
CREATE OR REPLACE FUNCTION fn_validate_stars() RETURNS trigger AS $$
BEGIN
  IF NEW.stars < 1 OR NEW.stars > 5 THEN
    RAISE EXCEPTION 'Stars must be between 1 and 5';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validate_stars
BEFORE INSERT ON reviews
FOR EACH ROW
EXECUTE FUNCTION fn_validate_stars();

-- 2) Recompute average rating AFTER INSERT/UPDATE/DELETE on reviews
CREATE OR REPLACE FUNCTION fn_recompute_movie_rating() RETURNS trigger AS $$
DECLARE
  v_avg NUMERIC(4,2);
  v_cnt INT;
  v_movie_id INT;
BEGIN
  v_movie_id := COALESCE(NEW.movie_id, OLD.movie_id);
  SELECT COALESCE(AVG(rating),0), COUNT(*) INTO v_avg, v_cnt
  FROM reviews WHERE movie_id = v_movie_id;

  UPDATE movies
  SET avg_rating = v_avg,
      review_count = v_cnt
  WHERE movie_id = v_movie_id;

  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_reviews_after_ins
AFTER INSERT ON reviews
FOR EACH ROW EXECUTE FUNCTION fn_recompute_movie_rating();

CREATE TRIGGER trg_reviews_after_upd
AFTER UPDATE ON reviews
FOR EACH ROW EXECUTE FUNCTION fn_recompute_movie_rating();

CREATE TRIGGER trg_reviews_after_del
AFTER DELETE ON reviews
FOR EACH ROW EXECUTE FUNCTION fn_recompute_movie_rating();

-- 3) Prevent deleting a movie with linked rows
CREATE OR REPLACE FUNCTION fn_block_delete_movie_when_linked() RETURNS trigger AS $$
DECLARE v_cnt INT;
BEGIN
  SELECT COUNT(*) INTO v_cnt FROM reviews WHERE movie_id = OLD.movie_id;
  IF v_cnt > 0 THEN
    RAISE EXCEPTION 'Cannot delete movie with existing reviews';
  END IF;

  SELECT COUNT(*) INTO v_cnt FROM actsin WHERE movie_id = OLD.movie_id;
  IF v_cnt > 0 THEN
    RAISE EXCEPTION 'Cannot delete movie with existing actsin records';
  END IF;

  RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_block_delete_movie
BEFORE DELETE ON movies
FOR EACH ROW EXECUTE FUNCTION fn_block_delete_movie_when_linked();

-- 4) Optional: logging table and trigger
CREATE TABLE IF NOT EXISTS log_activity (
  log_id SERIAL PRIMARY KEY,
  entity TEXT,
  action TEXT,
  entity_id INT,
  at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION fn_log_review_changes() RETURNS trigger AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    INSERT INTO log_activity(entity, action, entity_id) VALUES ('review','insert', NEW.review_id);
  ELSIF TG_OP = 'DELETE' THEN
    INSERT INTO log_activity(entity, action, entity_id) VALUES ('review','delete', OLD.review_id);
  END IF;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_log_review_ins
AFTER INSERT ON reviews
FOR EACH ROW EXECUTE FUNCTION fn_log_review_changes();

CREATE TRIGGER trg_log_review_del
AFTER DELETE ON reviews
FOR EACH ROW EXECUTE FUNCTION fn_log_review_changes();
