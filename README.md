# SQL Week 2 Project – Movie Database

## Overview
This repository contains our **SQL Week 2 Group Project**.

Each team member is responsible for one key section of the project.  

---

## Team Members & Roles

| Member | Git Branch | Part | Role Description |
|:--------|:-------------|:------|:----------------|
|  **Andreii** | `feature/constraints` | **Part 1 – Relationships & Constraints** | Create and enforce all database relationships, foreign keys, and validation rules. |
|  **Samuel** | `feature/triggers` | **Part 2 – Triggers** | Automate database actions and enforce logic integrity (rating updates, deletions, etc.). |
|  **Krishma** | `feature/views` | **Part 3 – Views** | Create summarized and analytical database views for easy data access. |
|  **Nadya** | `feature/functions` | **Part 4 – Stored Functions** | Develop reusable SQL functions for retrieving calculated or specific information. |
|  **Nelson (Project Manager)** | `feature/analytical` | **Part 5 – Analytical Queries** | Build advanced analytical queries to explore and analyze data trends. |
|  **Abanoub** | `feature/reports` | **Part 6 – Reports (Summary Queries)** | Create final summary reports combining data across multiple tables. |

---

##  Repository Structure

```
sql-week2-project/
│
├── README.md
│
├── schema/
│   ├── create_tables.sql
│   ├── constraints.sql
│   └── sample_data.sql
│
├── features/
│   ├── functions.sql
│   ├── triggers.sql
│   ├── views.sql
│
├── queries/
│   ├── analytical_queries.sql
│   ├── reports.sql
│
├── tests/
│   ├── test_data.sql
│   ├── validation_queries.sql
│   ├── test_runner.sql
│
└── docs/
    ├── team_roles.md
    ├── project_summary.md
    ├── ER_diagram.png
```

---

##  Run Order (Execution Sequence for Supabase / PostgreSQL)

Run the SQL files in this exact order for best compatibility:

1. `schema/create_tables.sql`  
2. `schema/constraints.sql`  
3. `schema/sample_data.sql`  
4. `features/functions.sql`  
5. `features/triggers.sql`  
6. `features/views.sql`  
7. `queries/analytical_queries.sql`  
8. `queries/reports.sql`  
9. `tests/test_data.sql`  
10. `tests/validation_queries.sql`  
11. `tests/test_runner.sql`

You can execute them sequentially in Supabase’s SQL Editor, or via CLI:

```bash
psql -f schema/create_tables.sql
psql -f schema/constraints.sql
psql -f schema/sample_data.sql
psql -f features/functions.sql
psql -f features/triggers.sql
psql -f features/views.sql
psql -f queries/analytical_queries.sql
psql -f queries/reports.sql
psql -f tests/test_runner.sql
```

Or directly inside Supabase’s SQL Editor by copying each block in sequence.

---

##  Task Breakdown and Expectations

###  Part 1 – Relationships & Constraints (Andreii)
- Add all **foreign keys** (`ON DELETE CASCADE` / `SET NULL`)
- Add **CHECK** constraints:  
  - `rating BETWEEN 0 AND 10`  
  - `stars BETWEEN 1 AND 5`  
  - `release_year >= 1900`
- `UNIQUE (title, release_year)`
- Enforce **NOT NULL** and valid foreign keys
- Validate constraints using `tests/validation_queries.sql`
-  *PostgreSQL Tip:* Wrap constraint creation in a `DO $$` block if you need an `IF NOT EXISTS` guard (Postgres doesn’t support it directly).

---

###  Part 2 – Triggers (Samuel)
- `AFTER INSERT/UPDATE/DELETE` on reviews → recompute movie’s average rating + review count  
- `BEFORE INSERT` on reviews → validate stars between 1–5  
- `BEFORE DELETE` on movies → prevent deleting movies with linked reviews or acts_in  
- Optional: logging trigger to track activity  
- Include commented examples for testing
-  *PostgreSQL Syntax:*  
  - Use `LANGUAGE plpgsql`  
  - Use `EXECUTE FUNCTION` (not `EXECUTE PROCEDURE`)  

---

###  Part 3 – Views (Krishma)
- Create:
  - `view_movie_summary`
  - `view_actor_summary`
  - `view_genre_stats`
  - (Optional) `view_director_performance`
- Use joins and aggregations
- Add `DROP VIEW IF EXISTS` before each create statement

---

###  Part 4 – Stored Functions (Nadya)
- `get_actor_avg_rating(actor_id)` → return `NUMERIC` (or `FLOAT`)  
- `get_genre_top_movie(genre_name)` → return `TABLE(movie_id, title, rating)`  
- Add **LANGUAGE plpgsql** and mark as `STABLE`  
- Include test SELECTs for each function  

---

###  Part 5 – Analytical Queries (Nelson)
- 10–12 analytical queries covering:
  - Top-rated movies  
  - Actors per genre  
  - Directors with high averages  
  - Genres above global average  
  - Actors never in movies below rating 5  
  - Most active reviewers, etc.  
- Add a `-- goal:` comment above each query explaining its purpose  
- Ensure every query runs independently after schema + features are executed  

---

###  Part 6 – Reports (Abanoub)
- Write 3–5 report-style queries:
  - “Top 3 genres by total reviews”
  - “Top 5 actors by appearances”
  - “Director performance by average rating”
  - “Movies with reviews after 2020”
  - “Genres by average duration”
- Keep all results cleanly formatted with clear column names  

---

## Branching Strategy

| Branch | Purpose |
|:--------|:----------|
| `main` | Stable release (final tested version). |
| `dev` | Integration branch (merge all reviewed features). |
| `feature/<part>` | Individual feature branches per team member. |

Example:
```bash
git checkout -b feature/views
git add .
git commit -m "Add view_movie_summary and view_actor_summary"
git push origin feature/views
```

---

## 🧾 Pull Request Workflow

Each team member:
1. Works in their feature branch  
2. Commits changes with a clear message referencing the issue (e.g., `#3 add views`)  
3. Opens a **Pull Request** to the `dev` branch  
4. The PM reviews and merges once it passes testing

**PR Template:**
```markdown
### What changed?
- Describe updates or new SQL components added.

### How to test:
- Run [specific file] after running schema.

### Screenshot / Output (if applicable):
```

---

##  Testing

Use `tests/test_data.sql` and `tests/validation_queries.sql` to verify:
- Constraints reject invalid data  
- Triggers update correctly  
- Views/functions return valid results  
- Queries produce expected outputs  

Each SQL file should include at least **one commented test snippet**  
(e.g., an example `INSERT` and `SELECT` to demonstrate results).

You can run all tests together using:
```sql
\i tests/test_runner.sql
```

---

## Database Schema Overview
The database models a **movie ecosystem** with:
- **Movies**
- **Directors**
- **Actors**
- **Genres**
- **Reviews**
- **ActsIn** (relationship between actors and movies)

---

##  Tools & Dialect

Primary dialect: **PostgreSQL (Supabase)**  

### Supabase/PostgreSQL Guidelines
- Use `LANGUAGE plpgsql` for all trigger and function bodies  
- Use `EXECUTE FUNCTION` (Postgres ≥ 14 syntax)  
- For idempotent scripts, add `DROP IF EXISTS` before `CREATE`  
- Run inside **Supabase SQL Editor** or using `psql` CLI  

*(SQLite/MySQL can be adapted, but this project is tested and graded on PostgreSQL via Supabase.)*

---

##  Credits
Created collaboratively by the **SQL Week 2 Team**  Andrii, Nadya, Krishma, Samuel, Abanoub
**Project Manager:** Nelson  
Powered by **Supabase** + **PostgreSQL**
