# Movie-Database
This repository contains our **Team Group 1 Project**, focused on building and managing a **Movie Database** 

Each team member is responsible for one key section of the project.  
The goal is to demonstrate solid database design, automation with triggers, reusable SQL logic with functions, and insightful data analytics through queries and reports.

---

## Team Members & Roles

| Member | Git Branch | Part | Role Description |
|:--------|:-------------|:------|:----------------|
|  **Mohammad** | `feature/constraints` | **Part 1 – Relationships & Constraints** | 
|  **Samuel** | `feature/triggers` | **Part 2 – Triggers** | 
|  **Sayed** | `feature/views` | **Part 3 – Views** | 
|  **Nadya** | `feature/functions` | **Part 4 – Stored Functions** | 
|  **Nelson (Project Manager)** | `feature/analytical` | **Part 5 – Analytical Queries** | 
|  **Abanoub** | `feature/reports` | **Part 6 – Reports (Summary Queries)** | 

## Team Members & Roles (Main Project)

| Member                 | Git Branch          | Part                             | Role Description                    |
|:-----------------------|:--------------------|:---------------------------------|:------------------------------------|
| **Mohammad**           | `feature/constraints` | **Part 1 – Relationships & Constraints** |
| **Samuel**             | `feature/triggers`    | **Part 2 – Triggers**           |
| **Sayed**              | `feature/views`       | **Part 3 – Views**              |
| **Nadya**              | `feature/functions`   | **Part 4 – Stored Functions**   |
| **Nelson (Project Manager)** | `feature/analytical` | **Part 5 – Analytical Queries** |
| **Abanoub**            | `feature/reports`     | **Part 6 – Reports (Summary Queries)** |

---

### 24 November to 1 December Task

Create `server.py` and inside this file create 6 functions to display all the table data.

Tables: `actors`, `actsin`, `customers`, `log_activity`, `movies`, `rentings`  
Views: `view_actor_summary`, `view_genre_stats`, `view_movie_summary`

---

## Team Members & Roles (Python Server Tasks)

| Member                 | Git Branch                  | Task Description                                                             |
|:-----------------------|:----------------------------|:-----------------------------------------------------------------------------|
| **Mohammad**           | `feature/actors`            | Create a function that fetches the `actors` table and displays the results. |
| **Samuel**             | `feature/actsin`            | Create a function that fetches the `actsin` table and displays the results. |
| **Sayed**              | `feature/customers`         | Create a function that fetches the `customers` table and displays the results. |
| **Nadya**              | `feature/log_activity`      | Create a function that fetches the `log_activity` table and displays the results. |
| **Nelson (Project Manager)** | `feature/movies`      | Create a function that fetches the `movies` table and displays the results. |
| **Abanoub**            | `feature/rentings`          | Create a function that fetches the `rentings` table and displays the results. |
| **Krishma**            | `feature/view-actor-summary` | Create a function that fetches the `view_actor_summary` view and displays the results. |


## Python Scripts for Movies and Rentings

This project includes two simple Python scripts that connect to a Supabase
PostgreSQL database using the psycopg2 library. Each script belongs to a
different feature branch and retrieves data from a specific table.

---

### Feature: Movies (feature/movies)

Location: feature_movies/server.py
Purpose:

- Connects to the database  
- Fetches all rows from the movies table  
- Prints the results in the terminal  

Main function: get_all_movies()

---

### Feature: Rentings (feature/rentings)

Location: feature_rentings/server.py
Purpose:

- Connects to the database  
- Fetches all rows from the rentings table  
- Displays all rows in the terminal  

Main function: get_all_rentings()

---

## Environment Variables

Both scripts require a local `.env` file with the database credentials.
Important:  
The real `.env` file is **not uploaded** to GitHub for security reasons.

Example structure:

user=YOUR_USER
password=YOUR_PASSWORD
host=YOUR_HOST
port=5432
dbname=postgres
sslmode=require

This file shows the required variables without exposing real credentials.

## How to Run the Scripts

Run from the root directory:

Movies:python feature_movies/server.py
Rentings:python feature_rentings/server.py

Each script loads the environment variables, connects to Supabase, and prints
the table data in the console.

