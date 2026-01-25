"""
Bayesian Analysis on Movie Rental Database

This module applies Bayes' Theorem using real data from the database.
It demonstrates:
- Prior, likelihood, evidence
- Bayesian arrays
- Normalization
- Posterior computation
- Verification via direct conditional probability
- Two real-world Bayesian scenarios
"""

from server import get_connection


# ==========================================================
# SAFE DATABASE HELPER
# ==========================================================

def fetch_scalar(query, params=None):
    """
    Executes a query that returns a single scalar value.
    Safely handles NULL and division-by-zero cases.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params or ())
    value = cur.fetchone()[0]
    conn.close()
    return value if value is not None else 0


# ==========================================================
# SCENARIO 1
# P(HighRating | Genre)
# ==========================================================

def bayes_high_rating_given_genre(genre):
    """
    Bayesian inference:
    Probability that a movie receives a high rating (>=4)
    given that it belongs to a specific genre.
    """

    # PRIOR: P(HighRating)
    prior = fetch_scalar("""
        SELECT COUNT(*) FILTER (WHERE rating >= 4)::float
               / NULLIF(COUNT(*), 0)
        FROM rentings;
    """)

    # LIKELIHOOD: P(Genre | HighRating)
    likelihood = fetch_scalar("""
        SELECT COUNT(*) FILTER (WHERE m.genre = %s)::float
               / NULLIF(COUNT(*), 0)
        FROM rentings r
        JOIN movies m ON r.movie_id = m.movie_id
        WHERE r.rating >= 4;
    """, (genre,))

    # EVIDENCE: P(Genre)
    evidence = fetch_scalar("""
        SELECT COUNT(*) FILTER (WHERE m.genre = %s)::float
               / NULLIF(COUNT(*), 0)
        FROM rentings r
        JOIN movies m ON r.movie_id = m.movie_id;
    """, (genre,))

    # BAYES ARRAY (UNNORMALIZED)
    bayes_array = [
        {"hypothesis": "HighRating", "joint": likelihood * prior},
        {"hypothesis": "NotHighRating", "joint": (1 - likelihood) * (1 - prior)}
    ]

    # NORMALIZATION
    normalization_constant = sum(x["joint"] for x in bayes_array)

    posterior = (
        bayes_array[0]["joint"] / normalization_constant
        if normalization_constant > 0 else 0
    )

    # DIRECT CONDITIONAL PROBABILITY (VERIFICATION)
    direct = fetch_scalar("""
        SELECT COUNT(*) FILTER (WHERE r.rating >= 4)::float
               / NULLIF(COUNT(*), 0)
        FROM rentings r
        JOIN movies m ON r.movie_id = m.movie_id
        WHERE m.genre = %s;
    """, (genre,))

    return {
        "scenario": "P(HighRating | Genre)",
        "genre": genre,
        "prior": prior,
        "likelihood": likelihood,
        "evidence": evidence,
        "bayes_array": bayes_array,
        "normalization_constant": normalization_constant,
        "posterior_bayes": posterior,
        "posterior_direct": direct
    }


# ==========================================================
# SCENARIO 2
# P(Female | HighRating)
# ==========================================================

def bayes_female_given_high_rating():
    """
    Bayesian inference:
    Probability that a customer is female,
    given that they give high ratings (>=4).
    """

    # PRIOR: P(Female)
    prior = fetch_scalar("""
        SELECT COUNT(*) FILTER (WHERE gender = 'F')::float
               / NULLIF(COUNT(*), 0)
        FROM customers;
    """)

    # LIKELIHOOD: P(HighRating | Female)
    likelihood = fetch_scalar("""
        SELECT COUNT(*) FILTER (WHERE r.rating >= 4)::float
               / NULLIF(COUNT(*), 0)
        FROM rentings r
        JOIN customers c ON r.customer_id = c.customer_id
        WHERE c.gender = 'F';
    """)

    # EVIDENCE: P(HighRating)
    evidence = fetch_scalar("""
        SELECT COUNT(*) FILTER (WHERE rating >= 4)::float
               / NULLIF(COUNT(*), 0)
        FROM rentings;
    """)

    # BAYES ARRAY (UNNORMALIZED)
    bayes_array = [
        {"hypothesis": "Female", "joint": likelihood * prior},
        {"hypothesis": "Male", "joint": (1 - likelihood) * (1 - prior)}
    ]

    # NORMALIZATION
    normalization_constant = sum(x["joint"] for x in bayes_array)

    posterior = (
        bayes_array[0]["joint"] / normalization_constant
        if normalization_constant > 0 else 0
    )

    # DIRECT CONDITIONAL VERIFICATION
    direct = fetch_scalar("""
        SELECT COUNT(*) FILTER (WHERE c.gender = 'F')::float
               / NULLIF(COUNT(*), 0)
        FROM rentings r
        JOIN customers c ON r.customer_id = c.customer_id
        WHERE r.rating >= 4;
    """)

    return {
        "scenario": "P(Female | HighRating)",
        "prior": prior,
        "likelihood": likelihood,
        "evidence": evidence,
        "bayes_array": bayes_array,
        "normalization_constant": normalization_constant,
        "posterior_bayes": posterior,
        "posterior_direct": direct
    }


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    print("\n========== BAYESIAN ANALYSIS ==========\n")

    # SCENARIO 1
    result1 = bayes_high_rating_given_genre("Action")
    print("SCENARIO 1 RESULT:\n", result1)

    print("\n--------------------------------------\n")

    # SCENARIO 2
    result2 = bayes_female_given_high_rating()
    print("SCENARIO 2 RESULT:\n", result2)
