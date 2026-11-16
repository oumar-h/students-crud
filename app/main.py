import os
import sys

import psycopg2
from psycopg2 import errors


DB_CONFIG = {
    "dbname":   os.getenv("PGDATABASE", "student_db"),
    "user":     os.getenv("PGUSER", "postgres"),
    "password": os.getenv("PGPASSWORD", "postgres"),
    "host":     os.getenv("PGHOST", "localhost"),
    "port":     os.getenv("PGPORT", "5432"),
}


def get_connection():
    """Open and return a new connection to the PostgreSQL database."""
    return psycopg2.connect(**DB_CONFIG)


def getAllStudents():
    """Retrieve every row from the students table and print it."""
    try:
        # 'with conn' commits/rolls back the transction; 'with cur' closes the cursor.
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT student_id, first_name, last_name, email, enrollment_date "
                "FROM studets ORDER BY student_id;"
            )
            rows = cur.fetchall()

        # Print a simple formatted table.
        print(f"\n{'ID':<5}{'First':<12}{'Last':<12}{'Email':<28}{'Enrolled'}")
        print("-" * 70)
        for sid, first, last, email, enrolled in rows:
            print(f"{sid:<5}{first:<12}{last:<12}{email:<28}{enrolled}")
        print(f"\n{len(rows)} student(s) found.\n")
        return rows
    except psycopg2.Error as e:
        print(f"Database eror while retrieving students: {e}")


def addStudent(first_name, last_name, email, enrollment_date):
    """Insert a new student. enrollment_date is a 'YYYY-MM-DD' string (or None)."""
    try:
        with get_connection() as conn, conn.cursor() as cur:
            # Parameterized query (%s) protects against SQL injection.
            cur.execute(
                "INSERT INTO students (first_name, last_name, email, enrollment_date) "
                "VALUES (%s, %s, %s, %s) RETURNING student_id;",
                (first_name, last_name, email, enrollment_date),
            )
            new_id = cur.fetchone()[0]
        print(f"Added student '{first_name} {last_name}' with student_id {new_id}.")
        return new_id
    except errors.UniqueViolation:
        print(f"Error: a student with email '{email}' already exists.")
    except psycopg2.Error as e:
        print(f"Database error while adding student: {e}")


def updateStudentEmail(student_id, new_email):
    """Change the email of the student with the given student_id."""
    try:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                "UPDATE students SET email = %s WHERE student_id = %s;",
                (new_email, student_id),
            )
            updated = cur.rowcount  # number of rows affected
        if updated:
            print(f"Updated email for student_id {student_id} to '{new_email}'.")
        else:
            print(f"No atudent found with student_id {student_id}.")
        return updated
    except errors.UniqueViolation:
        print(f"Error: email '{new_email}' is already used by another student.")
    except psycopg2.Error as e:
        print(f"Database error while updating email: {e}")


def deleteStudent(student_id):
    """Delete the student with the given student_id."""
    try:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("DELETE FROM students WHERE student_id = %s;", (student_id,))
            deleted = cur.rowcount
        if deleted:
            print(f"Deleted student with student_id {student_id}.")
        else:
            print(f"No student found with student_id {student_id}.")
        return deleted
    except psycopg2.Error as e:
        print(f"Database error while deleting student: {e}")


def read_int(prompt):
    """Prompt until the user enters a valid integer."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Please enter a whole number.")


def menu():
    """Interactive command-line menu that calls the four CRUD functions."""
    options = (
        "\n=== Student Database ===\n"
        "1. View all students\n"
        "2. Add a student\n"
        "3. Update a student's email\n"
        "4. Delete a student\n"
        "5. Quit\n"
    )
    while True:
        print(options)
        choice = input("Choose an option: ").strip()
        if choice == "1":
            getAllStudents()
        elif choice == "2":
            first = input("First name: ").strip()
            last = input("Last name: ").strip()
            email = input("Email: ").strip()
            date = input("Enrollment date (YYYY-MM-DD, blank for none): ").strip() or None
            addStudent(first, last, email, date)
        elif choice == "3":
            updateStudentEmail(read_int("student_id: "), input("New email: ").strip())
        elif choice == "4":
            deleteStudent(read_int("student_id: "))
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")


def demo():
    """Run each operation once, in order, for the demonstration video."""
    print(">>> getAllStudents()")
    getAllStudents()
    print(">>> addStudent('Alice', 'Johnson', 'alice.johnson@example.com', '2023-09-03')")
    new_id = addStudent("Alice", "Johnson", "alice.johnson@example.com", "2023-09-03")
    getAllStudents()
    print(f">>> updateStudentEmail({new_id}, 'alice.j@example.com')")
    updateStudentEmail(new_id, "alice.j@example.com")
    getAllStudents()
    print(f">>> deleteStudent({new_id})")
    deleteStudent(new_id)
    getAllStudents()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    else:
        menu()