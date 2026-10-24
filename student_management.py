import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create student table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    course TEXT NOT NULL,
    marks REAL NOT NULL
)
""")

conn.commit()


# 1. Add student
def add_student():
    try:
        name = input("Enter student name: ")
        age = int(input("Enter student age: "))
        course = input("Enter student course: ")
        marks = float(input("Enter student marks: "))

        if not name.strip() or not course.strip():
            print("Name and course cannot be empty.")
            return

        if age <= 0 or not 0 <= marks <= 100:
            print("Enter a valid age and marks between 0 and 100.")
            return

        cursor.execute("""
        INSERT INTO students (name, age, course, marks)
        VALUES (?, ?, ?, ?)
        """, (name.strip(), age, course.strip(), marks))

        conn.commit()
        print("Student added successfully!")

    except ValueError:
        print("Please enter valid numbers for age and marks.")


# 2. View all students
def view_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if not students:
        print("No students found.")
        return

    print("\n--- Student Details ---")

    for student in students:
        print(
            f"ID: {student[0]}, "
            f"Name: {student[1]}, "
            f"Age: {student[2]}, "
            f"Course: {student[3]}, "
            f"Marks: {student[4]}"
        )


# 3. Search student by ID
def search_student():
    try:
        student_id = int(input("Enter student ID to search: "))

        cursor.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,)
        )

        student = cursor.fetchone()

        if student:
            print("\nStudent found:")
            print("ID:", student[0])
            print("Name:", student[1])
            print("Age:", student[2])
            print("Course:", student[3])
            print("Marks:", student[4])
        else:
            print("Student not found.")

    except ValueError:
        print("Please enter a valid student ID.")


# 4. Update student details
def update_student():
    try:
        student_id = int(input("Enter student ID to update: "))

        cursor.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,)
        )

        student = cursor.fetchone()

        if not student:
            print("Student not found.")
            return

        print("Leave a field blank to keep its current value.")

        name = input(f"Enter new name [{student[1]}]: ").strip()
        age_input = input(f"Enter new age [{student[2]}]: ").strip()
        course = input(f"Enter new course [{student[3]}]: ").strip()
        marks_input = input(f"Enter new marks [{student[4]}]: ").strip()

        new_name = name if name else student[1]
        new_age = int(age_input) if age_input else student[2]
        new_course = course if course else student[3]
        new_marks = float(marks_input) if marks_input else student[4]

        if new_age <= 0 or not 0 <= new_marks <= 100:
            print("Enter a valid age and marks between 0 and 100.")
            return

        cursor.execute("""
        UPDATE students
        SET name = ?, age = ?, course = ?, marks = ?
        WHERE id = ?
        """, (new_name, new_age, new_course, new_marks, student_id))

        conn.commit()
        print("Student updated successfully!")

    except ValueError:
        print("Please enter valid numbers for age and marks.")


# 5. Delete student
def delete_student():
    try:
        student_id = int(input("Enter student ID to delete: "))

        cursor.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,)
        )

        student = cursor.fetchone()

        if not student:
            print("Student not found.")
            return

        confirm = input(
            f"Delete student {student[1]}? (yes/no): "
        ).strip().lower()

        if confirm == "yes":
            cursor.execute(
                "DELETE FROM students WHERE id = ?",
                (student_id,)
            )
            conn.commit()
            print("Student deleted successfully!")
        else:
            print("Deletion cancelled.")

    except ValueError:
        print("Please enter a valid student ID.")


# Main menu
try:
    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            search_student()

        elif choice == "4":
            update_student()

        elif choice == "5":
            delete_student()

        elif choice == "6":
            print("Thank you for using Student Management System!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 6.")

finally:
    conn.close()