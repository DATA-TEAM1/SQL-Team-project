1/schema/constraints.sql

ALTER TABLE public.movies
ADD CONSTRAINT fk_director
FOREIGN KEY (director_id)
REFERENCES public.directors (director_id)
ON DELETE SET NULL;

ALTER TABLE public.movies
ADD CONSTRAINT fk_genre
FOREIGN KEY (genre_id)
REFERENCES public.genres (genre_id)
ON DELETE CASCADE;

ALTER TABLE public.actsin
ADD CONSTRAINT fk_movie
FOREIGN KEY (movie_id)
REFERENCES public.movies (movie_id)
ON DELETE CASCADE;

ALTER TABLE public.actsin
ADD CONSTRAINT fk_actor
FOREIGN KEY (actor_id)
REFERENCES public.actors (actor_id)
ON DELETE CASCADE;

ALTER TABLE public.rentings
ADD CONSTRAINT fk_renting_movie
FOREIGN KEY (movie_id)
REFERENCES public.movies (movie_id)
ON DELETE CASCADE;

ALTER TABLE public.rentings
ADD CONSTRAINT fk_renting_customer
FOREIGN KEY (customer_id)
REFERENCES public.customers (customer_id)
ON DELETE CASCADE;

ALTER TABLE public.rentings
ADD CONSTRAINT check_rating
CHECK (rating BETWEEN 0 AND 10);

ALTER TABLE public.movies
ADD CONSTRAINT check_release_year
CHECK (year_of_release >= 1900);

ALTER TABLE public.movies
ADD CONSTRAINT unique_movie_title_year
UNIQUE (title, year_of_release);

