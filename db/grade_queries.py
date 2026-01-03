# db/grade_queries.py
# Purpose: CRUD operations for Grade table,
# Helpers: get_students, get_courses, get_exams, get_semesters for UI combos.


from db.connection import get_connection, get_cursor, close_connection, close_cursor

class GradeQueries:
    @staticmethod
    def create_grade(
        student_id,
        course_id,
        department_id,
        exam_id,
        semester_id,
        grade_type,
        grade_date,
        grade_source,
        grade_value,
        max_points,
        comments,
    ):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            sql = """
                INSERT INTO Grade (student_id, course_id, department_id, exam_id, semester_id, grade_type, grade_date, grade_source, grade_value, max_points, comments)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING grade_id;
            """
            cursor.execute(
                sql,
                (
                    student_id,
                    course_id,
                    department_id,
                    exam_id,
                    semester_id,
                    grade_type,
                    grade_date,
                    grade_source,
                    grade_value,
                    max_points,
                    comments,
                ),
            )
            new_id = cursor.fetchone()[0]
            connection.commit()
            print(f"✅ Grade created with ID: {new_id}")
            return new_id
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error creating grade: {e}")
            return None
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_all_grades(search_term="", semester_id=None, grade_type=None):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            sql = """
                SELECT G.grade_id, S.first_name || ' ' || S.last_name AS student_name, C.name AS course_name, G.grade_type, G.grade_value, G.max_points
                FROM Grade G
                JOIN Student S ON G.student_id = S.student_id
                JOIN Course C ON G.course_id = C.course_id AND G.department_id = C.department_id
                WHERE (S.first_name ILIKE %s OR S.last_name ILIKE %s OR C.name ILIKE %s)
            """
            params = [f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"]
            if semester_id:
                sql += " AND G.semester_id = %s"
                params.append(semester_id)
            if grade_type and grade_type != 'All':
                sql += " AND G.grade_type = %s"
                params.append(grade_type)
            sql += " ORDER BY G.grade_date DESC;"
            cursor.execute(sql, params)
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Error reading grades: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def update_grade(grade_id, student_id, course_id, department_id, exam_id, semester_id, grade_type, grade_date, grade_source, grade_value, max_points, comments):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            sql = """
                UPDATE Grade SET student_id = %s, course_id = %s, department_id = %s, exam_id = %s, semester_id = %s, grade_type = %s, grade_date = %s, grade_source = %s, grade_value = %s, max_points = %s, comments = %s
                WHERE grade_id = %s;
            """
            cursor.execute(sql, (student_id, course_id, department_id, exam_id, semester_id, grade_type, grade_date, grade_source, grade_value, max_points, comments, grade_id))
            connection.commit()
            print(f"✅ Grade ID {grade_id} updated")
            return True
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error updating grade: {e}")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def delete_grade(grade_id):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            sql = "DELETE FROM Grade WHERE grade_id = %s;"
            cursor.execute(sql, (grade_id,))
            connection.commit()
            print(f"✅ Grade ID {grade_id} deleted")
            return True
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error deleting grade: {e}")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_students():
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            sql = """
                SELECT Student_ID, First_Name || ' ' || Last_Name AS full_name
                FROM Student
                ORDER BY Last_Name, First_Name;
            """
            cursor.execute(sql)
            return cursor.fetchall()  # List of (id, name) tuples
        except Exception as e:
            print(f"❌ Error fetching students: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_courses():
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            sql = """
                SELECT Course_ID, name AS course_name
                FROM Course
                ORDER BY name;
            """
            cursor.execute(sql)
            return cursor.fetchall()  # List of (id, name) tuples
        except Exception as e:
            print(f"❌ Error fetching courses: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_exams():
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            sql = """
                SELECT Exam_ID, Exam_Name AS exam_name
                FROM Exam
                ORDER BY Exam_Name;
            """
            cursor.execute(sql)
            return cursor.fetchall()  # List of (id, name) tuples
        except Exception as e:
            print(f"❌ Error fetching exams: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_semesters():
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            sql = """
                SELECT Semester_ID, Name AS semester_name
                FROM Semester
                ORDER BY Name;
            """
            cursor.execute(sql)
            return cursor.fetchall()  # List of (id, name) tuples
        except Exception as e:
            print(f"❌ Error fetching semesters: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_grade_by_id(grade_id):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            sql = """
                SELECT student_id, course_id, department_id, exam_id, semester_id, grade_type, grade_date, grade_source, grade_value, max_points, comments
                FROM Grade WHERE grade_id = %s;
            """
            cursor.execute(sql, (grade_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"❌ Error fetching grade by ID: {e}")
            return None
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_grades_for_avg(student_id, course_id, department_id):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            sql = """
                SELECT grade_type, grade_value, max_points
                FROM Grade
                WHERE student_id = %s AND course_id = %s AND department_id = %s;
            """
            cursor.execute(sql, (student_id, course_id, department_id))
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Error fetching grades for avg: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)
