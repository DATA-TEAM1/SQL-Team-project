CREATE OR REPLACE VIEW highly_rated_movies AS
SELECT
    m.title,
    m.year_of_release,
    m.runtime,
    m.avg_rating
FROM
    public.movies m
WHERE
    m.avg_rating >= 4.0
ORDER BY
    m.avg_rating DESC;

CREATE OR REPLACE VIEW customer_activity_summary AS
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(r.renting_id) AS total_rented_movies
FROM
    public.customers c
LEFT JOIN
    public.rentings r ON c.customer_id = r.customer_id
GROUP BY
    c.customer_id, c.first_name, c.last_name
ORDER BY
    total_rented_movies DESC;
