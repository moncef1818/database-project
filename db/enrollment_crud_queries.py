# New file: db/enrollment_crud_queries.py
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
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = """
                SELECT enrollment_id, student_id, course_id, department_id, semester_id, status
                FROM enrollment
            """
            params = []

            if search_field and search_value:
                if search_field == "ID":
                    sql += " WHERE CAST(enrollment_id AS TEXT) LIKE %s"
                    params.append(f"%{search_value}%")
                elif search_field == "Student ID":
                    sql += " WHERE CAST(student_id AS TEXT) LIKE %s"
                    params.append(f"%{search_value}%")
                elif search_field == "Course ID":
                    sql += " WHERE CAST(course_id AS TEXT) LIKE %s"
                    params.append(f"%{search_value}%")
                elif search_field == "Department ID":
                    sql += " WHERE CAST(department_id AS TEXT) LIKE %s"
                    params.append(f"%{search_value}%")
                elif search_field == "Semester ID":
                    sql += " WHERE CAST(semester_id AS TEXT) LIKE %s"
                    params.append(f"%{search_value}%")
                elif search_field == "Status":
                    sql += " WHERE LOWER(status) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")

            if sort_by not in [
                "enrollment_id",
                "student_id",
                "course_id",
                "department_id",
                "semester_id",
                "status",
            ]:
                sort_by = "enrollment_id"
            if sort_order not in ["ASC", "DESC"]:
                sort_order = "ASC"

            sql += f" ORDER BY {sort_by} {sort_order}"

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
