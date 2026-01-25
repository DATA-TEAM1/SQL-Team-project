import numpy as np

"""
Random Variables & Linear Algebra
Discrete Random Variables

All numerical work uses NumPy.
No hardcoded probabilities.
No loops unless unavoidable.
No np.mean, np.var, scipy, sklearn, pandas stats.
"""

# =====================================================
# PART 1: RANDOM VARIABLE X — MOVIE RATINGS
# =====================================================

# X = rating of a randomly selected movie
# Load raw data (example: from CSV or database extraction)

ratings = np.loadtxt("movie_ratings.csv")  
# ratings is a 1D NumPy array of raw rating values

print("Raw ratings sample:", ratings[:10])

# -----------------------------------------------------
# Step 1: Identify support of X (unique values)
# -----------------------------------------------------

x_values, counts = np.unique(ratings, return_counts=True)

print("\nPossible values of X (ratings):")
print(x_values)

print("\nCounts for each rating:")
print(counts)

# -----------------------------------------------------
# Step 2: Compute PMF using normalization
# PMF = counts / total observations
# -----------------------------------------------------

total_movies = ratings.size
pmf_X = counts / total_movies

print("\nProbability Mass Function P(X = x):")
print(pmf_X)

# -----------------------------------------------------
# Step 3: Expected Value using dot product
# E(X) = Σ x · P(X=x)
# -----------------------------------------------------

expected_X = np.dot(x_values, pmf_X)

print("\nExpected Value E(X):", expected_X)

print(
    "\nInterpretation:\n"
    "If we repeatedly select a movie at random from the database,\n"
    "the long-run average rating we expect to observe is {:.2f}.\n"
    "This does NOT mean most movies have this rating — it is a weighted average."
    .format(expected_X)
)

# -----------------------------------------------------
# Step 4: Variance (manual formula)
# Var(X) = Σ (x − μ)^2 · P(X=x)
# -----------------------------------------------------

deviations = x_values - expected_X
squared_deviations = deviations ** 2

print("\nDeviations from mean:")
print(deviations)

print("\nSquared deviations:")
print(squared_deviations)

variance_X = np.dot(squared_deviations, pmf_X)
std_dev_X = np.sqrt(variance_X)

print("\nVariance Var(X):", variance_X)
print("Standard Deviation:", std_dev_X)

print(
    "\nInterpretation:\n"
    "Variance measures how spread out the ratings are around the mean.\n"
    "The standard deviation tells us that ratings typically differ from\n"
    "the average by about {:.2f} rating points."
    .format(std_dev_X)
)

# -----------------------------------------------------
# Step 5: Manual sanity check on small subset
# -----------------------------------------------------

subset = x_values[:3]
subset_pmf = pmf_X[:3]

manual_check = subset[0]*subset_pmf[0] + subset[1]*subset_pmf[1] + subset[2]*subset_pmf[2]

print(
    "\nManual verification (partial sum of E(X) using first 3 values):",
    manual_check
)
