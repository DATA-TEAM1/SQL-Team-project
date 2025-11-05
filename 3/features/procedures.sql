--- FUNCTIONS & PROCEDURES FOR PART 3 ---

-- 1. Function for searching movies by genre
CREATE OR REPLACE FUNCTION get_movies_by_genre(genre_name VARCHAR)
RETURNS TABLE(
    movie_id INT,
    title VARCHAR,
    year_of_release INT,
    avg_rating NUMERIC
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        m.movie_id,
        m.title,
        m.year_of_release,
        m.avg_rating
    FROM
        public.movies m
    WHERE
        m.genre = genre_name;
END;
$$ LANGUAGE plpgsql;

-- 2. Procedure for updating rental price
CREATE OR REPLACE PROCEDURE update_rental_price(
    movie_id_in INT,
    price_multiplier NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE public.movies
    SET renting_price = renting_price * price_multiplier
    WHERE movie_id = movie_id_in;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Movie with ID % not found.', movie_id_in;
    END IF;
END;
$$;
