# ============================
# Person 6 – Bayes’ Theorem
# ============================

def bayes_analysis():
    print("\n==============================")
    print("Bayesian Analysis Using Database Data")
    print("==============================")

    conn = None
    try:
        conn = get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            # ---------- Scenario 1 ----------
            total_rentings = run_query(
                cur, "SELECT COUNT(*) AS count FROM rentings;"
            )[0]["count"]

            total_movies = run_query(
                cur, "SELECT COUNT(*) AS count FROM movies;"
            )[0]["count"]

            drama_movies = run_query(
                cur,
                "SELECT COUNT(*) AS count FROM movies WHERE genre = 'Drama';"
            )[0]["count"]

            high_rating = run_query(
                cur,
                "SELECT COUNT(*) AS count FROM rentings WHERE rating >= 4;"
            )[0]["count"]

            drama_high = run_query(
                cur,
                """
                SELECT COUNT(*) AS count
                FROM rentings r
                JOIN movies m ON r.movie_id = m.movie_id
                WHERE m.genre = 'Drama' AND r.rating >= 4;
                """
            )[0]["count"]

            drama_rentings = run_query(
                cur,
                """
                SELECT COUNT(*) AS count
                FROM rentings r
                JOIN movies m ON r.movie_id = m.movie_id
                WHERE m.genre = 'Drama';
                """
            )[0]["count"]

            P_drama = drama_movies / total_movies
            P_high = high_rating / total_rentings
            P_high_given_drama = drama_high / drama_rentings

            P_drama_given_high = (
                P_high_given_drama * P_drama
            ) / P_high

            print("\n--- Scenario 1 ---")
            print("P(Drama | Rating >= 4):", round(P_drama_given_high, 4))

            # ---------- Scenario 2 ----------
            action_movies = run_query(
                cur,
                "SELECT COUNT(*) AS count FROM movies WHERE genre = 'Action';"
            )[0]["count"]

            male_customers = run_query(
                cur,
                "SELECT COUNT(*) AS count FROM customers WHERE gender = 'Male';"
            )[0]["count"]

            total_customers = run_query(
                cur,
                "SELECT COUNT(*) AS count FROM customers;"
            )[0]["count"]

            male_action = run_query(
                cur,
                """
                SELECT COUNT(*) AS count
                FROM rentings r
                JOIN customers c ON r.customer_id = c.customer_id
                JOIN movies m ON r.movie_id = m.movie_id
                WHERE m.genre = 'Action' AND c.gender = 'Male';
                """
            )[0]["count"]

            action_rentings = run_query(
                cur,
                """
                SELECT COUNT(*) AS count
                FROM rentings r
                JOIN movies m ON r.movie_id = m.movie_id
                WHERE m.genre = 'Action';
                """
            )[0]["count"]

            P_action = action_movies / total_movies
            P_male = male_customers / total_customers
            P_male_given_action = male_action / action_rentings

            P_action_given_male = (
                P_male_given_action * P_action
            ) / P_male

            print("\n--- Scenario 2 ---")
            print("P(Action | Customer is Male):", round(P_action_given_male, 4))

            # ---------- Verification ----------
            P_direct = drama_high / high_rating
            print("\n--- Verification ---")
            print("Direct P(Drama | Rating >= 4):", round(P_direct, 4))

            # ---------- Explanation ----------
            print("\n--- Why Normalization Is Required ---")
            print(
                "Bayes' theorem divides by P(B) to normalize probabilities.\n"
                "Without normalization, probabilities would be invalid."
            )

    except Exception as e:
        print("Bayesian analysis error:", e)

    finally:
        if conn:
            conn.close()


# ------------------------------------------------
# Run inside server.py
# ------------------------------------------------
if __name__ == "__main__":
    bayes_analysis()
