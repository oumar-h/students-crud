-- schema.sql
-- Creates the students table and loads the initial data.
-- Run this while connected to your target database (e.g. "student_db").

-- Drop the table if it exists so the script can be re-run cleanly.
DROP TABLE IF EXISTS students;

-- student_id is SERIAL (auto-incrementing integer) and the primary key.
-- first_name, last_name and email cannot be NULL; email must be unique.
-- enrollment_date is optional (no NOT NULL constraint), per the schema.
CREATE TABLE students (
    student_id      SERIAL PRIMARY KEY,
    first_name      TEXT   NOT NULL,
    last_name       TEXT   NOT NULL,
    email           TEXT   NOT NULL UNIQUE,
    enrollment_date DATE
);

-- Initial data provided in the assignment.
INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
('John', 'Doe',   'john.doe@example.com',   '2023-09-01'),
('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
('Jim',  'Beam',  'jim.beam@example.com',   '2023-09-02');