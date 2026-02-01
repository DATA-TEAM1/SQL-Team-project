# Person 6 – Bayes’ Theorem
# Reverse conditional probabilities using Bayes' Theorem

cursor = db.cursor()

# --------------------------------------------------
# 1. P(Drama | Rating >= 4) using Bayes' Theorem
# --------------------------------------------------

# Total number of rentings
cursor.execute("SELECT COUNT(*) FROM rentings")
total_rentings = cursor.fetchone()[0]

# P(A) = P(Drama)
cursor.execute("""
SELECT COUNT(*)
FROM movies
WHERE genre = 'Drama'
""")
total_drama_movies = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM movies")
total_movies = cursor.fetchone()[0]

P_drama = total_drama_movies / total_movies

# P(B) = P(Rating >= 4)
cursor.execute("""
SELECT COUNT(*)
FROM rentings
WHERE rating >= 4
""")
high_rating_count = cursor.fetchone()[0]
P_high_rating = high_rating_count / total_rentings

# P(B | A) = P(Rating >= 4 | Drama)
cursor.execute("""
SELECT COUNT(*)
FROM rentings r
JOIN movies m ON r.movie_id = m.movie_id
WHERE m.genre = 'Drama' AND r.rating >= 4
""")
drama_high_rating = cursor.fetchone()[0]

cursor.execute("""
SELECT COUNT(*)
FROM rentings r
JOIN movies m ON r.movie_id = m.movie_id
WHERE m.genre = 'Drama'
""")
total_drama_rentings = cursor.fetchone()[0]

P_high_rating_given_drama = drama_high_rating / total_drama_rentings

# Bayes' Theorem
P_drama_given_high_rating = (
    P_high_rating_given_drama * P_drama
) / P_high_rating

print("P(Drama | Rating >= 4):", round(P_drama_given_high_rating, 4))

# --------------------------------------------------
# 2. P(Action | Customer is Male)
# --------------------------------------------------

# P(A) = P(Action)
cursor.execute("""
SELECT COUNT(*)
FROM movies
WHERE genre = 'Action'
""")
total_action_movies = cursor.fetchone()[0]

P_action = total_action_movies / total_movies

# P(B) = P(Customer is Male)
cursor.execute("""
SELECT COUNT(*)
FROM customers
WHERE gender = 'Male'
""")
male_customers = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM customers")
total_customers = cursor.fetchone()[0]

P_male = male_customers / total_customers

# P(B | A) = P(Customer is Male | Action)
cursor.execute("""
SELECT COUNT(*)
FROM rentings r
JOIN customers c ON r.customer_id = c.customer_id
JOIN movies m ON r.movie_id = m.movie_id
WHERE m.genre = 'Action' AND c.gender = 'Male'
""")
male_action_rentings = cursor.fetchone()[0]

cursor.execute("""
SELECT COUNT(*)
FROM rentings r
JOIN movies m ON r.movie_id = m.movie_id
WHERE m.genre = 'Action'
""")
total_action_rentings = cursor.fetchone()[0]

P_male_given_action = male_action_rentings / total_action_rentings

# Bayes' Theorem
P_action_given_male = (P_male_given_action * P_action) / P_male

print("P(Action | Customer is Male):", round(P_action_given_male, 4))

# --------------------------------------------------
# 3. Verification using Direct Conditional Probability
# --------------------------------------------------

cursor.execute("""
SELECT COUNT(*)
FROM rentings r
JOIN movies m ON r.movie_id = m.movie_id
WHERE r.rating >= 4 AND m.genre = 'Drama'
""")
direct_drama_high = cursor.fetchone()[0]

P_direct_drama = direct_drama_high / high_rating_count

print("Direct P(Drama | Rating >= 4):", round(P_direct_drama, 4))

cursor.close()
