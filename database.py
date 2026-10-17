import sqlite3
import os
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "students.db")

def get_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conn

def get_all_students():
    conn = get_connection()

    students = conn.execute("SELECT * FROM students").fetchall()

    conn.close()
    return students


# Read single student
def get_student_by_id(student_id):
    conn = get_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    conn.close()
    return student

# add student
def add_student(name, course, photo=""):
    conn = get_connection()

    cursor = conn.execute("""
        INSERT INTO students (name, course, photo)
        VALUES (?, ?, ?)
    """, (name, course, photo))

    conn.commit()

    student_id = cursor.lastrowid

    conn.close()

    return student_id

def update_student(student_id,name,course,photo=None):
    conn = get_connection()

    if photo is not None:
        conn.execute("""
        UPDATE students SET name = ?, course = ?, photo = ? where id = ? """,(name,course,photo,student_id))
    else:
        conn.execute("""
        UPDATE students SET name = ?, course = ? where id = ? """,(name,course,student_id))

    conn.commit()
    conn.close()


def delete_student(student_id):
    conn = get_connection()

    try:
        # Step 1: Delete only this student's course assignments
        conn.execute(
            "DELETE FROM student_courses WHERE student_id = ?",
            (student_id,)
        )

        # Step 2: Delete the student from the students table
        conn.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        # Step 3: Save both changes
        conn.commit()

    except Exception:
        # Undo database changes if an error occurs
        conn.rollback()
        raise

    finally:
        # Always close the database connection
        conn.close()


def create_user(username,email,password):
    conn = get_connection()
    hashed_password = generate_password_hash(password)
    conn.execute("""
    INSERT INTO users (username,email,password) VALUES (?,?,?)    
""",(username,email,hashed_password))

    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = get_connection()

    user = conn.execute("SELECT * FROM users WHERE username=?"
                        ,(username,)
                    ).fetchone()
    conn.close()
    return user

def get_user_by_email(email):
    conn = get_connection()

    user = conn.execute("SELECT * FROM users WHERE email=?"
                        ,(email,)
                    ).fetchone()
    conn.close()
    return user


def create_admin(username,email,password):
    conn = get_connection()

    hashed_password = generate_password_hash(password)
    conn.execute("""
    INSERT INTO users (username,email,password,role) VALUES (?,?,?,?)    
""",(username,email,hashed_password,"admin"))

    conn.commit()
    conn.close()

def get_student_count():
    conn = get_connection()

    count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]

    conn.close()
    return count

def get_user_count():
    conn = get_connection()

    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]

    conn.close()
    return count

def get_admin_count():
    conn = get_connection()

    count = conn.execute("SELECT COUNT(*) FROM users WHERE role = ?",("admin",)).fetchone()[0]

    conn.close()
    return count

def get_all_users():
    conn = get_connection()

    users = conn.execute("SELECT * FROM users").fetchall()

    conn.close()
    return users

def update_user_role(user_id,role):
    conn = get_connection()
    conn.execute("UPDATE users SET role=? WHERE id=?",(role,user_id))

    conn.commit()
    conn.close()

def search_students(search):
    conn = get_connection()

    students = conn.execute(
        """
        SELECT * FROM students WHERE name LIKE ?""",(f"{search}",)
    ).fetchall()

    conn.close()
    return students

def get_students_by_course(course):
    conn = get_connection()

    students = conn.execute(""" SELECT * FROM students WHERE course=? """,(course,)).fetchall()

    conn.close()
    return students

def filter_students(search="",course="",limit=10,offset=0):
    conn = get_connection()
    query = "SELECT * from students WHERE 1=1"
    parameters = []

    if search:
        query += " AND name LIKE ?" 
        parameters.append(f"%{search}%")

    if course:
        query += " AND course = ?" 
        parameters.append(course)

    query += " LIMIT ? OFFSET ?" 
    parameters.append(limit)
    parameters.append(offset)

    students = conn.execute(query,parameters).fetchall()
    conn.close()
    return students

def get_students_paginated(limit,offset):
    conn = get_connection()

    students = conn.execute("""
    SELECT * FROM students
    LIMIT ? OFFSET ?
    """,(limit,offset)).fetchall()
    conn.close()
    return students

def get_filtered_student_count(search="", course=""):

    conn = get_connection()

    query = """
        SELECT COUNT(*) FROM students
        WHERE 1=1
    """

    parameters = []

    if search:

        query += " AND name LIKE ?"

        parameters.append(
            f"%{search}%"
        )

    if course:

        query += " AND course = ?"

        parameters.append(course)

    count = conn.execute(
        query,
        parameters
    ).fetchone()[0]

    conn.close()

    return count

def create_courses_table():
    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS courses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE)
    """)
    conn.commit()
    conn.close()

# student courses table
def create_student_courses_table():
    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS student_courses (
    student_id INTEGER,
    course_id INTEGER,

    PRIMARY KEY(student_id,course_id),

    FOREIGN KEY (student_id)
    REFERENCES students(id),

    FOREIGN KEY (course_id)
    REFERENCES courses(id))
    """)
    conn.commit()
    conn.close()

def add_course(name):
    conn = get_connection()

    conn.execute(
        "INSERT INTO courses (name) VALUES (?)",
        (name,)
    )
    conn.commit()
    conn.close()

def get_all_courses():
    conn = get_connection()

    courses = conn.execute(
        "SELECT * FROM courses ORDER BY name"
    ).fetchall()

    conn.close()
    return courses

def assign_course(student_id,course_id):
    conn = get_connection()
    try:
        conn.execute("""
        INSERT INTO student_courses
        (student_id,course_id)
        VALUES (?,?)
        """,(student_id,course_id))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def get_student_courses(student_id):
    conn = get_connection()

    courses = conn.execute("""
    SELECT courses.id ,courses.name FROM student_courses
    JOIN courses
    ON student_courses.course_id = courses.id
    WHERE student_courses.student_id = ?
    ORDER BY courses.name
    """,(student_id,)).fetchall()
    conn.close()
    return courses

def remove_student_course(student_id,course_id):
    conn = get_connection()
    try:
        conn.execute("""
        DELETE FROM student_courses
        WHERE student_id = ?
        AND course_id = ?
        """,(student_id,course_id))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def create_default_courses():
    conn = get_connection()

    courses = [
        ("Python",),
        ("Django",),
        ("SQL",),
        ("Data Science",),
        ("Flask",)
    ]

    conn.executemany(
        "INSERT OR IGNORE INTO courses(name) VALUES(?)",courses
    )
    conn.commit()
    conn.close()

