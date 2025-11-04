# Team Roles
- Andrii — Part 1 (Constraints)
- Samuel — Part 2 (Triggers)
- Krishma — Part 3 (Views)
- Nadya — Part 4 (Functions)
- Nelson (PM) — Part 5 (Analytical)
- Abanoub — Part 6 (Reports)
# Team Quick Start Guide – SQL Team Project

Welcome to the **SQL-Team-Project**!  
Follow these simple steps so our workflow stays clean, organized, and stress-free 👇
---

## Before You Start
- Go to our repo → **Branches** → select **your branch**:
  - Andreii → `feature/constraints`
  - Samuel → `feature/triggers`
  - Krishma → `feature/views`
  - Nadya → `feature/functions`
  - Nelson (PM) → `feature/analytical`
  - Abanoub → `feature/reports`
- Never edit directly on **main**.  
- Use the web editor or GitHub Desktop (whichever you prefer).

---

## What to Edit
| Your Part | File Location |
|------------|----------------|
| Part 1 | `schema/constraints.sql` |
| Part 2 | `features/triggers.sql` |
| Part 3 | `features/views.sql` |
| Part 4 | `features/functions.sql` |
| Part 5 | `queries/analytical_queries.sql` |
| Part 6 | `queries/reports.sql` |

Each file already has comments and **TODOs** guiding what to build.

---

## Commit & Push
1. After editing, click **Commit changes**.  
2. Write a short message (example:  
   `#3 Added view_actor_summary`)  
3. Make sure the commit goes to **your branch** (`feature/...`) not `main`.

---

##  Create a Pull Request (PR)
When your part works:
1. Go to **Pull Requests → New Pull Request**  
2. Base branch → `dev`  
   Compare branch → your `feature/...` branch  
3. Fill out the short PR template  
4. Click **Create Pull Request**

Nelson (PM) reviews and merges into `dev`.

---

##  Testing
Before submitting:
- Run or preview your SQL using an online PostgreSQL/SQLite tool.  
- Test your constraints, views, or functions with the examples in `tests/validation_queries.sql`.  
- Ensure your SQL runs without errors and uses proper `DROP IF EXISTS` where needed.

---

##  Final Merge
After all parts are approved and merged into `dev`,  
the PM tests everything together using `tests/test_runner.sql`,  
then merges `dev → main` for the final version.

---

##  Quick Reminders
✅ Comment your SQL sections  
✅ Keep file names and structure unchanged  
✅ Don’t upload `.db` or `.sqlite` files  
✅ Always pull (sync) before starting new edits  
✅ Be kind and review a teammate’s PR if asked 😄

---

**Team Motto:**  
> “Clean code, clear structure, one commit at a time!”  
