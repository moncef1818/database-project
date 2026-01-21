# New file: db/course_crud_queries.py
from db.connection import close_connection, close_cursor, get_connection, get_cursor


class CourseCRUD:
    @staticmethod
    def create_course(department_id, name, description):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = """
                INSERT INTO course (department_id, name, description)
                VALUES (%s, %s, %s) RETURNING course_id;
            """
            cursor.execute(sql, (department_id, name, description))
            new_id = cursor.fetchone()[0]
            connection.commit()
            print(f" Course created with ID: {new_id}")
            return True
        except Exception as e:
            if connection:
                connection.rollback()
            print(f" Error creating course: {e}")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_all_courses(
        search_field=None, search_value=None, sort_by="course_id", sort_order="ASC"
    ):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = """
                SELECT c.course_id, c.department_id, d.name as dept_name,
                       c.name, c.description
                FROM course c
                LEFT JOIN department d ON c.department_id = d.department_id
            """
            params = []

            if search_field and search_value:
                if search_field == "Course ID":
                    sql += " WHERE CAST(c.course_id AS TEXT) LIKE %s"
                    params.append(f"%{search_value}%")
                elif search_field == "Department ID":
                    sql += " WHERE CAST(c.department_id AS TEXT) LIKE %s"
                    params.append(f"%{search_value}%")
                elif search_field == "Course Name":
                    sql += " WHERE LOWER(c.name) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")
                elif search_field == "Department Name":
                    sql += " WHERE LOWER(d.name) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")

            if sort_by not in [
                "course_id",
                "department_id",
                "name",
                "dept_name",
            ]:
                sort_by = "course_id"
            if sort_order not in ["ASC", "DESC"]:
                sort_order = "ASC"

            sql += f" ORDER BY {sort_by} {sort_order}"

            cursor.execute(sql, params)
            results = cursor.fetchall()
            print(f" Retrieved {len(results)} courses")
            return results
        except Exception as e:
            print(f"Error fetching courses: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def update_course(course_id, department_id, name, description):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = """
                UPDATE course
                SET department_id = %s, name = %s, description = %s
                WHERE course_id = %s AND department_id = %s;
            """
            # Get old department_id first
            cursor.execute(
                "SELECT department_id FROM course WHERE course_id = %s", (course_id,)
            )
            result = cursor.fetchone()
            if not result:
                print(f" No course found with ID {course_id}")
                return False

            old_dept_id = result[0]

            cursor.execute(
                sql,
                (department_id, name, description, course_id, old_dept_id),
            )
            rows_affected = cursor.rowcount
            connection.commit()

            if rows_affected > 0:
                print(f"✅ Course {course_id} updated")
                return True
            else:
                print(f"⚠️ No course found with ID {course_id}")
                return False
        except Exception as e:
            if connection:
                connection.rollback()
            print(f" Error updating course: {e}")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def delete_course(course_id, department_id):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = "DELETE FROM course WHERE course_id = %s AND department_id = %s;"
            cursor.execute(sql, (course_id, department_id))
            rows_affected = cursor.rowcount
            connection.commit()

            if rows_affected > 0:
                print(f" Course {course_id} deleted")
                return True
            else:
                print(f"No course found with ID {course_id}")
                return False
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Error deleting course: {e}")
            if "foreign key" in str(e).lower() or "violates" in str(e).lower():
                print(" Cannot delete: Course is referenced in other records")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_all_departments():
        """Helper method to get departments for dropdown"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            cursor.execute("SELECT department_id, name FROM department ORDER BY name")
            return cursor.fetchall()
        except Exception as e:
            print(f" Error fetching departments: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)
