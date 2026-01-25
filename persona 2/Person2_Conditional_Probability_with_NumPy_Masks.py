# Person2_Conditional_Probability_with_NumPy_Masks.py

import numpy as np
import os

# --------------------------------------------------
# Load CSV (same directory as this script)
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(
    BASE_DIR, "Supabase Snippet Movie metadata extraction.csv")

raw_data = np.genfromtxt(
    CSV_PATH,
    delimiter=",",
    skip_header=1,
    dtype=str,
    encoding="utf-8"
)

# --------------------------------------------------
# Extract and clean columns
# --------------------------------------------------
genres = raw_data[:, 0]

runtimes = raw_data[:, 1].astype(int)

ratings = np.array(
    [
        float(x) if x.strip().lower() not in ("", "null", "nan")
        else np.nan
        for x in raw_data[:, 2]
    ],
    dtype=float
)

print("Array shapes and dtypes:")
print("genres:", genres.shape, genres.dtype)
print("runtimes:", runtimes.shape, runtimes.dtype)
print("ratings:", ratings.shape, ratings.dtype)

# --------------------------------------------------
# Define Events (EXPLICITLY)
# --------------------------------------------------
# A: Movie genre is Comedy
A = (genres == "Comedy")

# B: Movie has high rating (>= 7)
B = (ratings >= 7)

# C: Movie is long (> 120 minutes)
C = (runtimes > 120)

# D: Movie has missing rating
D = np.isnan(ratings)

# --------------------------------------------------
# Conditional Probability Function (SAFE)
# --------------------------------------------------


def conditional_probability(event_A, event_B):
    """
    Computes P(A | B) = P(A ∩ B) / P(B)

    If P(B) = 0, the conditional probability is undefined,
    so NaN is returned explicitly.
    """
    total_B = np.sum(event_B)
    if total_B == 0:
        return np.nan
    return np.sum(event_A & event_B) / total_B


# --------------------------------------------------
# Conditional Probabilities (5 required)
# --------------------------------------------------
p_comedy_given_high_rating = conditional_probability(A, B)
p_high_rating_given_comedy = conditional_probability(B, A)

p_long_given_high_rating = conditional_probability(C, B)
p_high_rating_given_long = conditional_probability(B, C)

p_missing_rating_given_comedy = conditional_probability(D, A)

# --------------------------------------------------
# INTENTIONALLY INCORRECT example
# --------------------------------------------------
# WRONG: Dividing by total number of movies
wrong_p_comedy_given_high_rating = np.sum(A & B) / len(genres)

# --------------------------------------------------
# Output results
# --------------------------------------------------
print("\nCorrect Conditional Probabilities:")
print("P(Comedy | High Rating):", p_comedy_given_high_rating)
print("P(High Rating | Comedy):", p_high_rating_given_comedy)
print("P(Long Movie | High Rating):", p_long_given_high_rating)
print("P(High Rating | Long Movie):", p_high_rating_given_long)
print("P(Missing Rating | Comedy):", p_missing_rating_given_comedy)

print("\nIncorrect Conditional Probability Example:")
print("WRONG P(Comedy | High Rating):", wrong_p_comedy_given_high_rating)

# --------------------------------------------------
# Explanation (for grading)
# --------------------------------------------------
# Ratings contained non-numeric values ('null', empty).
# These were converted to NaN using NumPy-safe logic.
#
# Conditional probability P(A | B) restricts the sample space
# to only cases where B occurs.
#
# When P(B) = 0, the conditional probability is undefined,
# so NaN is returned instead of dividing by zero.
#
# The incorrect example divides by total movies, which
# computes a joint probability, not a conditional one.
#
# P(A | B) ≠ P(B | A)
