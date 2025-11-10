-- schema/constraints.sql
-- Part 1 – Relationships & Constraints 
-- Add foreign keys, checks, unique constraints, and NOT NULL rules.

-- Foreign keys with delete behavior
-- Connects actsin.movie_id -> movies.movie_id
ALTER TABLE public.actsin
ADD CONSTRAINT fk_actsin_movie
FOREIGN KEY (movie_id)
REFERENCES public.movies (movie_id)
ON DELETE CASCADE;

-- Connects actsin.actor_id -> actors.actor_id
ALTER TABLE public.actsin
ADD CONSTRAINT fk_actsin_actor
FOREIGN KEY (actor_id)
REFERENCES public.actors (actor_id)
ON DELETE CASCADE;

-- Connects rentings.customer_id -> customers.customer_id
ALTER TABLE public.rentings
ADD CONSTRAINT fk_rentings_customer
FOREIGN KEY (customer_id)
REFERENCES public.customers (customer_id)
ON DELETE CASCADE;

-- Connects rentings.movie_id -> movies.movie_id
ALTER TABLE public.rentings
ADD CONSTRAINT fk_rentings_movie
FOREIGN KEY (movie_id)
REFERENCES public.movies (movie_id)
ON DELETE CASCADE;

