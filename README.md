# Students Database – PostgreSQL CRUD Application
# Oumar Hassen
# 101320909
# Assignment 3, question 1 demo video

A Python command-line application that connects to a PostgreSQL database and performs
CRUD operations on a `students` table.

**Demo video:** https://youtu.be/-t5Yv9dJ7Bw

## Project structure
```
db/schema.sql      # Creates the students table and inserts the initial data
app/main.py        # Application (getAllStudents, addStudent, updateStudentEmail, deleteStudent)
app/requirements.txt
```

## Prerequisites
- PostgreSQL 13+ and pgAdmin
- Python 3.9+

## Setup
1. **Create the database** in pgAdmin (right-click Databases > Create > Database, name it `student_db`)
   or from a terminal:
   ```bash
   createdb -U postgres student_db
   ```
2. **Create the table and load data.** In pgAdmin, open the Query Tool on `student_db`, paste in
   `db/schema.sql` and run it. Or from a terminal:
   ```bash
   psql -U postgres -d student_db -f db/schema.sql
   ```
3. **Install dependencies:**
   ```bash
   cd app
   pip install -r requirements.txt
   ```
4. **Configure the connection** (only if yours differs from the defaults: database `student_db`,
   user `postgres`, password `postgres`, host `localhost`, port `5432`). Either edit `DB_CONFIG`
   in `app/main.py` or set environment variables:
   ```bash
   export PGDATABASE=student_db PGUSER=postgres PGPASSWORD=yourpassword
   ```
   (On Windows PowerShell: `$env:PGPASSWORD="yourpassword"`.)

## Running
Python is interpreted, so there is nothing to compile.
```bash
python main.py        # interactive menu
python main.py demo   # runs all four operations in sequence
```

## Functions
| Function | Description |
|---|---|
| `getAllStudents()` | Selects and prints all rows in `students`. |
| `addStudent(first_name, last_name, email, enrollment_date)` | Inserts a new student; reports duplicate emails. |
| `updateStudentEmail(student_id, new_email)` | Updates one student's email; reports unknown IDs and duplicates. |
| `deleteStudent(student_id)` | Deletes the student with that ID; reports unknown IDs. |

All queries are parameterized and wrapped in try/except for error handling.