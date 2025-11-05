ALTER TABLE public.movies
ADD COLUMN avg_rating NUMERIC(3, 2) DEFAULT 0;

CREATE OR REPLACE FUNCTION update_movie_avg_rating()
RETURNS TRIGGER AS $$
DECLARE
    movie_to_update INTEGER;
BEGIN
    IF (TG_OP = 'DELETE') THEN
        movie_to_update := OLD.movie_id;
    ELSE
        movie_to_update := NEW.movie_id;
    END IF;

    IF movie_to_update IS NOT NULL THEN
        UPDATE public.movies
        SET avg_rating = (
            SELECT COALESCE(AVG(r.rating), 0)
            FROM public.rentings r
            WHERE r.movie_id = movie_to_update
        )
        WHERE movie_id = movie_to_update;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER recalculate_rating_after_renting
AFTER INSERT OR UPDATE OF rating OR DELETE
ON public.rentings
FOR EACH ROW
EXECUTE FUNCTION update_movie_avg_rating();

CREATE OR REPLACE FUNCTION check_movie_delete_protection()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM public.rentings WHERE movie_id = OLD.movie_id) THEN
        RAISE EXCEPTION 'Cannot delete movie (ID: %) - linked records exist in rentings table.', OLD.movie_id;
    END IF;

    IF EXISTS (SELECT 1 FROM public.actsin WHERE movie_id = OLD.movie_id) THEN
        RAISE EXCEPTION 'Cannot delete movie (ID: %) - linked records exist in actsin table.', OLD.movie_id;
    END IF;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER protect_movie_from_delete
BEFORE DELETE
ON public.movies
FOR EACH ROW
EXECUTE FUNCTION check_movie_delete_protection();

--- ТРИГЕР 3: ВАЛІДАЦІЯ ДІАПАЗОНУ РЕЙТИНГУ ---

CREATE OR REPLACE FUNCTION check_rating_range()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.rating IS NOT NULL AND (NEW.rating < 1 OR NEW.rating > 5) THEN
        RAISE EXCEPTION 'Validation error: Rating (%) must be between 1 and 5.', NEW.rating;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER enforce_rating_validation
BEFORE INSERT OR UPDATE OF rating
ON public.rentings
FOR EACH ROW
EXECUTE FUNCTION check_rating_range();
