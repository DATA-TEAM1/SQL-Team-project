# 🎬 SQL Week 2 Project – Movie Database

## 📖 Overview
This repository contains our **SQL Week 2 Group Project**, focused on building and managing a **Movie Database** system using advanced SQL concepts such as **relationships**, **constraints**, **triggers**, **views**, **functions**, **analytical queries**, and **reports**.

Each team member is responsible for one key section of the project.  
The goal is to demonstrate solid database design, automation with triggers, reusable SQL logic with functions, and insightful data analytics through queries and reports.

---

## 👥 Team Members & Roles

| Member | Git Branch | Part | Role Description |
|:--------|:-------------|:------|:----------------|
| 🎓 **Andreii** | `feature/constraints` | **Part 1 – Relationships & Constraints** | Create and enforce all database relationships, foreign keys, and validation rules. |
| ⚙️ **Samuel** | `feature/triggers` | **Part 2 – Triggers** | Automate database actions and enforce logic integrity (rating updates, deletions, etc.). |
| 🧩 **Krishma** | `feature/views` | **Part 3 – Views** | Create summarized and analytical database views for easy data access. |
| 🧠 **Nadya** | `feature/functions` | **Part 4 – Stored Functions** | Develop reusable SQL functions for retrieving calculated or specific information. |
| 🧮 **Nelson (Project Manager)** | `feature/analytical` | **Part 5 – Analytical Queries** | Build advanced analytical queries to explore and analyze data trends. |
| 📈 **Abanoub** | `feature/reports` | **Part 6 – Reports (Summary Queries)** | Create final summary reports combining data across multiple tables. |

---

## 🧭 Repository Structure

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
│   ├── triggers.sql
│   ├── views.sql
│   ├── functions.sql
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

## ⚙️ Run Order (Execution Sequence)

Run the SQL files in this exact order:

1. `schema/create_tables.sql`  
2. `schema/constraints.sql`  
3. `features/triggers.sql`  
4. `features/views.sql`  
5. `features/functions.sql`  
6. `queries/analytical_queries.sql`  
7. `queries/reports.sql`

You can automate the process with (example for SQLite CLI):

```sql
.read schema/create_tables.sql
.read schema/constraints.sql
.read features/triggers.sql
.read features/views.sql
.read features/functions.sql
.read queries/analytical_queries.sql
.read queries/reports.sql
```

Or use `tests/test_runner.sql` in this repo.

---

## 🧩 Task Breakdown and Expectations

### 🟢 Part 1 – Relationships & Constraints (Andreii)
- Add all **foreign keys** (`ON DELETE CASCADE` / `SET NULL`)
- Add **CHECK** constraints:  
  - `rating BETWEEN 0 AND 10`  
  - `stars BETWEEN 1 AND 5`  
  - `release_year >= 1900`
- `UNIQUE (title, release_year)`
- Enforce **NOT NULL** and valid foreign keys
- Validate constraints with `tests/validation_queries.sql`

### 🟠 Part 2 – Triggers (Samuel)
- `AFTER INSERT/UPDATE/DELETE` on reviews → recompute movie’s average rating + review_count  
- `BEFORE INSERT` on reviews → validate stars between 1–5  
- `BEFORE DELETE` on movies → prevent deleting movies with linked reviews/actsin  
- Optional: logging trigger to track activity  
- Include commented examples for testing

### 🟡 Part 3 – Views (Krishma)
- Create:
  - `view_movie_summary`
  - `view_actor_summary`
  - `view_genre_stats`
  - (Optional) `view_director_performance`
- Use joins and aggregations
- Add `DROP VIEW IF EXISTS` before each create statement

### 🧠 Part 4 – Stored Functions (Nadya)
- `get_actor_avg_rating(actor_id)` → return FLOAT  
- `get_genre_top_movie(genre_name)` → return TABLE or TEXT (depending on dialect)  
- Include **test SELECTs** for each function  

### 🔴 Part 5 – Analytical Queries (Nelson)
- 10–12 queries covering:
  - Top-rated movies  
  - Actors per genre  
  - Directors with high averages  
  - Genres above global average  
  - Actors never in movies below rating 5  
  - Most active reviewers, etc.  
- Add `-- comment` above each query explaining its goal

### 🟣 Part 6 – Reports (Abanoub)
- Write 3–5 report-style queries:
  - “Top 3 genres by total reviews”
  - “Top 5 actors by appearances”
  - “Director performance by average rating”
  - “Movies with reviews after 2020”
  - “Genres by average duration”

---

## 🔀 Branching Strategy

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

**PR Template (auto-applies in this repo):**
```markdown
### What changed?
- Describe updates or new SQL components added.

### How to test:
- Run [specific file] after running schema.

### Screenshot / Output (if applicable):
```

---

## 🧪 Testing
Use `tests/test_data.sql` and `tests/validation_queries.sql` to verify:
- Constraints reject invalid data  
- Triggers update correctly  
- Views/functions return valid results  
- Queries produce expected outputs  

---

## 🧱 Database Schema Overview
The database models a **movie ecosystem** with:
- **Movies**
- **Directors**
- **Actors**
- **Genres**
- **Reviews**
- **ActsIn** (relationship between actors and movies)

---

## 🧩 Tools & Dialect
Recommended SQL Dialect: **PostgreSQL** (also compatible with MySQL with syntax changes).  
SQLite has limitations for stored functions; triggers are supported with some differences.

---

## 💬 Credits
Created collaboratively by the **SQL Week 2 Team**  
Project Manager: Nelson
``