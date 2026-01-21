from db.connection import close_connection, close_cursor, get_connection, get_cursor


class ResultsQueries:
    @staticmethod
    def execute_function(function_name, params=()):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            placeholders = ", ".join("%s" for _ in params)
            sql = f"SELECT * FROM {function_name}({placeholders});"
            cursor.execute(sql, params)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]  # type:ignore
            print(f" executed {function_name} , retrieved {len(results)} rows ")
            return results, columns
        except Exception as e:
            print(f"❌ Error executing {function_name}: {e}")
            return [], []
        finally:
            close_cursor(cursor)
            close_connection(connection)
# this helper function used in submenu for combo
    @staticmethod
    def get_semesters():

        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            sql = "SELECT Semester_ID, Name FROM Semester ORDER BY Start_Date DESC;"
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Error fetching semesters: {e}")
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
                SELECT Course_ID, Department_ID, name
                FROM Course
                ORDER BY name;
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
    def get_departments():

        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            sql = "SELECT Department_id, name FROM Department ORDER BY name;"
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Error fetching departments: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def update_enrollment_status(course_id, department_id, semester_id):

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = """
                WITH student_grades AS (
                    SELECT
                        g.student_id,
                        SUM(
                            CASE g.grade_type
                                WHEN 'Quiz' THEN (g.grade_value / g.max_points) * 20 * 0.10
                                WHEN 'Assignment' THEN (g.grade_value / g.max_points) * 20 * 0.10
                                WHEN 'Midterm' THEN (g.grade_value / g.max_points) * 20 * 0.30
                                WHEN 'Project' THEN (g.grade_value / g.max_points) * 20 * 0.10
                                WHEN 'Final' THEN (g.grade_value / g.max_points) * 20 * 0.40
                                WHEN 'Resit' THEN (g.grade_value / g.max_points) * 20 * 0.40
                                ELSE 0
                            END
                        ) as total_grade
                    FROM Grade g
                    WHERE g.course_id = %s
                        AND g.department_id = %s
                        AND g.semester_id = %s
                    GROUP BY g.student_id
                )
                UPDATE Enrollment e
                SET status = CASE
                    WHEN sg.total_grade >= 10 THEN 'Passed'
                    WHEN sg.total_grade >= 8 THEN 'Resit Eligible'
                    ELSE 'Failed'
                END
                FROM student_grades sg
                WHERE e.student_id = sg.student_id
                    AND e.course_id = %s
                    AND e.department_id = %s
                    AND e.semester_id = %s
                RETURNING e.student_id, e.status;
            """

            cursor.execute(
                sql,
                (
                    course_id,
                    department_id,
                    semester_id,
                    course_id,
                    department_id,
                    semester_id,
                ),
            )

            results = cursor.fetchall()
            connection.commit()

            print(f" Updated enrollment status for {len(results)} students")
            return results

        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error updating enrollment status: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)
