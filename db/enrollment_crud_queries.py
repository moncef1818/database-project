# Fixed file: db/enrollment_crud_queries.py
from db.connection import close_connection, close_cursor, get_connection, get_cursor


class EnrollmentCRUD:
    @staticmethod
    def create_enrollment(
        student_id, course_id, department_id, semester_id, status="Enrolled"
    ):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = """
                INSERT INTO enrollment (student_id, course_id, department_id, semester_id, status)
                VALUES (%s, %s, %s, %s, %s) RETURNING enrollment_id;
            """
            cursor.execute(
                sql, (student_id, course_id, department_id, semester_id, status)
            )
            new_id = cursor.fetchone()[0]
            connection.commit()
            print(f"✅ Enrollment created with ID: {new_id}")
            return True
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error creating enrollment: {e}")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_all_enrollments(
        search_field=None, search_value=None, sort_by="enrollment_id", sort_order="ASC"
    ):
        """
        Retrieves enrollments with JOINs to show names instead of just IDs
        """
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = """
                SELECT
                    e.enrollment_id,
                    e.student_id,
                    s.first_name || ' ' || s.last_name AS student_name,
                    e.course_id,
                    c.name AS course_name,
                    e.department_id,
                    d.name AS department_name,
                    e.semester_id,
                    sem.name AS semester_name,
                    e.status
                FROM enrollment e
                INNER JOIN student s ON e.student_id = s.student_id
                INNER JOIN course c ON e.course_id = c.course_id AND e.department_id = c.department_id
                INNER JOIN department d ON e.department_id = d.department_id
                INNER JOIN semester sem ON e.semester_id = sem.semester_id
            """
            params = []

            # Search filtering
            if search_field and search_value:
                if search_field == "ID":
                    sql += " WHERE CAST(e.enrollment_id AS TEXT) LIKE %s"
                    params.append(f"%{search_value}%")
                elif search_field == "Student ID":
                    sql += " WHERE CAST(e.student_id AS TEXT) LIKE %s"
                    params.append(f"%{search_value}%")
                elif search_field == "Student Name":
                    sql += " WHERE LOWER(s.first_name || ' ' || s.last_name) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")
                elif search_field == "Course Name":
                    sql += " WHERE LOWER(c.name) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")
                elif search_field == "Department Name":
                    sql += " WHERE LOWER(d.name) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")
                elif search_field == "Status":
                    sql += " WHERE LOWER(e.status) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")

            # Sorting
            valid_sorts = {
                "enrollment_id": "e.enrollment_id",
                "student_name": "student_name",
                "course_name": "course_name",
                "status": "e.status",
            }

            sort_col = valid_sorts.get(sort_by, "e.enrollment_id")
            if sort_order not in ["ASC", "DESC"]:
                sort_order = "ASC"

            sql += f" ORDER BY {sort_col} {sort_order}"

            cursor.execute(sql, params)
            results = cursor.fetchall()
            print(f"✅ Retrieved {len(results)} enrollments")
            return results
        except Exception as e:
            print(f"❌ Error fetching enrollments: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_students_for_dropdown():
        """Get all students for dropdown"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            sql = """
                SELECT student_id, first_name || ' ' || last_name AS full_name
                FROM student
                ORDER BY last_name, first_name
            """
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Error fetching students: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_courses_for_dropdown(department_id=None):
        """Get courses, optionally filtered by department"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            if department_id:
                sql = """
                    SELECT c.course_id, c.name, c.department_id
                    FROM course c
                    WHERE c.department_id = %s
                    ORDER BY c.name
                """
                cursor.execute(sql, (department_id,))
            else:
                sql = """
                    SELECT c.course_id, c.name, c.department_id
                    FROM course c
                    ORDER BY c.name
                """
                cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Error fetching courses: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_departments_for_dropdown():
        """Get all departments"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            sql = "SELECT department_id, name FROM department ORDER BY name"
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Error fetching departments: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_semesters_for_dropdown():
        """Get all semesters"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            sql = "SELECT semester_id, name FROM semester ORDER BY start_date DESC"
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Error fetching semesters: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def update_enrollment(
        enrollment_id, student_id, course_id, department_id, semester_id, status
    ):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = """
                UPDATE enrollment SET student_id = %s, course_id = %s, department_id = %s,
                semester_id = %s, status = %s WHERE enrollment_id = %s;
            """
            cursor.execute(
                sql,
                (
                    student_id,
                    course_id,
                    department_id,
                    semester_id,
                    status,
                    enrollment_id,
                ),
            )
            rows_affected = cursor.rowcount
            connection.commit()

            if rows_affected > 0:
                print(f"✅ Enrollment {enrollment_id} updated")
                return True
            else:
                print(f"⚠️ No enrollment found with ID {enrollment_id}")
                return False
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error updating enrollment: {e}")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def delete_enrollment(enrollment_id):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = "DELETE FROM enrollment WHERE enrollment_id = %s;"
            cursor.execute(sql, (enrollment_id,))
            rows_affected = cursor.rowcount
            connection.commit()

            if rows_affected > 0:
                print(f"✅ Enrollment {enrollment_id} deleted")
                return True
            else:
                print(f"⚠️ No enrollment found with ID {enrollment_id}")
                return False
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error deleting enrollment: {e}")
            if "foreign key" in str(e).lower() or "violates" in str(e).lower():
                print("⚠️ Cannot delete: Enrollment is referenced in other records")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)
