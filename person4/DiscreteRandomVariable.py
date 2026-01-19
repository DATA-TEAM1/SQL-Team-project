# -------------------------------------------------
# 1. MOVIE RATING AS DISCRETE RANDOM VARIABLE X
# -------------------------------------------------

# This dictionary comes from SQL:
# SELECT rating, COUNT(*) FROM movies WHERE rating IS NOT NULL GROUP BY rating;

rating_counts = {
    1.59: 8,
    1.69: 6,
    1.79: 8,
    2.09: 6,
    2.59: 5,
    2.69: 7,
    2.89: 6,
    3.09: 4,
    3.39: 4,
    3.69: 4,
    3.89: 3,
    4.09: 4,
    4.39: 3,
    4.69: 2,
    4.89: 1
}

# Total number of rated movies
total_movies = sum(rating_counts.values())

# -------------------------------------------------
# 2. PMF OF X
# -------------------------------------------------

pmf_X = {}

for rating, count in rating_counts.items():
    pmf_X[rating] = count / total_movies

# -------------------------------------------------
# 3. EXPECTED VALUE E(X)
# Formula: E(X) = Σ x · P(X = x)
# -------------------------------------------------

expected_X = 0

for x, p in pmf_X.items():
    expected_X += x * p

# -------------------------------------------------
# 4. VARIANCE Var(X)
# Formula: Var(X) = Σ (x − μ)^2 · P(X = x)
# -------------------------------------------------

variance_X = 0

for x, p in pmf_X.items():
    variance_X += (x - expected_X) ** 2 * p

# -------------------------------------------------
# 5. STANDARD DEVIATION
# Formula: σ = √Var(X)
# -------------------------------------------------

std_dev_X = variance_X ** 0.5

# -------------------------------------------------
# 6. MOVIES RENTED PER CUSTOMER AS RANDOM VARIABLE Y
# -------------------------------------------------

# This dictionary comes from SQL:
# SELECT customer_id, COUNT(*) FROM rentings GROUP BY customer_id;

rentals_per_customer_counts = {
    1: 7,
    2: 5,
    3: 9,
    4: 8,
    5: 7,
    6: 6,
    7: 5,
    8: 4,
    9: 4,
    10: 3
}

# Total number of customers
total_customers = sum(rentals_per_customer_counts.values())

# -------------------------------------------------
# 7. PMF OF Y
# -------------------------------------------------

pmf_Y = {}

for rentals, count in rentals_per_customer_counts.items():
    pmf_Y[rentals] = count / total_customers

# -------------------------------------------------
# 8. EXPECTED VALUE E(Y)
# Formula: E(Y) = Σ y · P(Y = y)
# -------------------------------------------------

expected_Y = 0

for y, p in pmf_Y.items():
    expected_Y += y * p

# -------------------------------------------------
# 9. VARIANCE Var(Y)
# -------------------------------------------------

variance_Y = 0

for y, p in pmf_Y.items():
    variance_Y += (y - expected_Y) ** 2 * p

# -------------------------------------------------
# 10. PRINT RESULTS
# -------------------------------------------------

print("----- RANDOM VARIABLE X: MOVIE RATING -----")
print("Expected Value E(X):", round(expected_X, 3))
print("Variance Var(X):", round(variance_X, 3))
print("Standard Deviation:", round(std_dev_X, 3))

print("\n----- RANDOM VARIABLE Y: MOVIES RENTED -----")
print("Expected Value E(Y):", round(expected_Y, 3))
print("Variance Var(Y):", round(variance_Y, 3))
