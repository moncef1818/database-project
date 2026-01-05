# db/attendance_queries.py

from db.connection import close_connection, close_cursor, get_connection, get_cursor


class AttendanceQueries:
    @staticmethod
    def create_attendance(
        student_id,
        activity_id,
        attendance_date,
        attended,
        attendance_time,
        special_accommodations,
        activity_type,
    ):
        """
        Creates a new attendance record in the appropriate table based on activity type.

        Args:
            student_id: Student ID
            activity_id: Activity ID
            attendance_date: Date of attendance (YYYY-MM-DD)
            attended: Boolean indicating if student attended
            attendance_time: Time of attendance (HH:MM:SS) or None
            special_accommodations: Text describing any accommodations
            activity_type: Type of activity ("Lecture", "Tutorial", or "Practical")

        """
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            # Select appropriate table based on activity type
            if activity_type == "Lecture":
                table = "Student_Lecture_Attendance"
            elif activity_type == "Tutorial":
                table = "Student_Tutorial_Attendance"
            elif activity_type == "Practical":
                table = "Student_Practical_Attendance"
            else:
                raise ValueError(f"Invalid activity_type: {activity_type}")

            # SQL query with parameterized values (prevents SQL injection)
            sql = f"""
                INSERT INTO {table} (
                    student_id, activity_id, attendance_date, attended,
                    attendance_time, special_accommodations
                )
                VALUES (%s, %s, %s, %s, %s, %s);
            """

            cursor.execute(
                sql,
                (
                    student_id,
                    activity_id,
                    attendance_date,
                    attended,
                    attendance_time,
                    special_accommodations,
                ),
            )

            connection.commit()
            print(f"✅ Attendance created in {table}")
            return True

        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error creating attendance: {e}")
            return False

        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_all_attendance(activity_type=None, search_term=""):
        """
        Retrieves all attendance records with optional filtering.
        Uses UNION to combine results from all three attendance tables.

        Args:
            activity_type: Filter by activity type ("Lecture", "Tutorial", "Practical") or None for all
            search_term: Search by student name (partial match)

        Returns:
            list: List of tuples (student_name, activity_type, date, attended, time, accommodations, student_id, activity_id)
        """
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            # Base SQL query using UNION to combine all attendance types
            sql = """
                SELECT
                    S.first_name || ' ' || S.last_name AS student_name,
                    'Lecture' AS activity_type,
                    LA.attendance_date,
                    LA.attended,
                    LA.attendance_time,
                    LA.special_accommodations,
                    LA.student_id,
                    LA.activity_id
                FROM Student_Lecture_Attendance LA
                JOIN Student S ON LA.student_id = S.student_id
                WHERE 1=1
            """
            params = []

            # Add activity type filter for Lecture
            if activity_type and activity_type != "Lecture":
                sql += " AND 1=0"  # Exclude lectures if filtering for other types

            # Add search filter
            if search_term:
                sql += " AND (S.first_name ILIKE %s OR S.last_name ILIKE %s)"
                params.extend([f"%{search_term}%", f"%{search_term}%"])

            # UNION with Tutorial attendance
            sql += """
                UNION ALL
                SELECT
                    S.first_name || ' ' || S.last_name AS student_name,
                    'Tutorial' AS activity_type,
                    TA.attendance_date,
                    TA.attended,
                    TA.attendance_time,
                    TA.special_accommodations,
                    TA.student_id,
                    TA.activity_id
                FROM Student_Tutorial_Attendance TA
                JOIN Student S ON TA.student_id = S.student_id
                WHERE 1=1
            """

            # Add filters for Tutorial
            if activity_type and activity_type != "Tutorial":
                sql += " AND 1=0"

            if search_term:
                sql += " AND (S.first_name ILIKE %s OR S.last_name ILIKE %s)"
                params.extend([f"%{search_term}%", f"%{search_term}%"])

            # UNION with Practical attendance
            sql += """
                UNION ALL
                SELECT
                    S.first_name || ' ' || S.last_name AS student_name,
                    'Practical' AS activity_type,
                    PA.attendance_date,
                    PA.attended,
                    PA.attendance_time,
                    PA.special_accommodations,
                    PA.student_id,
                    PA.activity_id
                FROM Student_Practical_Attendance PA
                JOIN Student S ON PA.student_id = S.student_id
                WHERE 1=1
            """

            # Add filters for Practical
            if activity_type and activity_type != "Practical":
                sql += " AND 1=0"

            if search_term:
                sql += " AND (S.first_name ILIKE %s OR S.last_name ILIKE %s)"
                params.extend([f"%{search_term}%", f"%{search_term}%"])

            # Order results
            sql += " ORDER BY attendance_date DESC, student_name;"

            cursor.execute(sql, params)
            return cursor.fetchall()

        except Exception as e:
            print(f"❌ Error fetching attendance: {e}")
            return []

        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_attendance_by_key(student_id, activity_id, attendance_date, activity_type):
        """
        Retrieves a specific attendance record by its composite key.

        Args:
            student_id: Student ID
            activity_id: Activity ID
            attendance_date: Date of attendance
            activity_type: Type of activity ("Lecture", "Tutorial", or "Practical")

        Returns:
            tuple: (student_id, activity_id, date, attended, time, accommodations) or None
        """
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            # Select appropriate table
            if activity_type == "Lecture":
                table = "Student_Lecture_Attendance"
            elif activity_type == "Tutorial":
                table = "Student_Tutorial_Attendance"
            elif activity_type == "Practical":
                table = "Student_Practical_Attendance"
            else:
                raise ValueError(f"Invalid activity_type: {activity_type}")

            sql = f"""
                SELECT student_id, activity_id, attendance_date, attended,
                       attendance_time, special_accommodations
                FROM {table}
                WHERE student_id = %s
                  AND activity_id = %s
                  AND attendance_date = %s;
            """

            cursor.execute(sql, (student_id, activity_id, attendance_date))
            return cursor.fetchone()

        except Exception as e:
            print(f"❌ Error fetching attendance by key: {e}")
            return None

        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def update_attendance(
        student_id,
        activity_id,
        attendance_date,
        attended,
        attendance_time,
        special_accommodations,
        activity_type,
    ):
        """
        Updates an existing attendance record.
        Note: Primary key fields (student_id, activity_id, date) cannot be changed.

        Args:
            student_id: Student ID (part of PK)
            activity_id: Activity ID (part of PK)
            attendance_date: Date of attendance (part of PK)
            attended: New attended status
            attendance_time: New time or None
            special_accommodations: New accommodations text
            activity_type: Type of activity (determines table)

        Returns:
            bool: True if successful, False otherwise
        """
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            # Select appropriate table
            if activity_type == "Lecture":
                table = "Student_Lecture_Attendance"
            elif activity_type == "Tutorial":
                table = "Student_Tutorial_Attendance"
            elif activity_type == "Practical":
                table = "Student_Practical_Attendance"
            else:
                raise ValueError(f"Invalid activity_type: {activity_type}")

            sql = f"""
                UPDATE {table}
                SET attended = %s,
                    attendance_time = %s,
                    special_accommodations = %s
                WHERE student_id = %s
                  AND activity_id = %s
                  AND attendance_date = %s;
            """

            cursor.execute(
                sql,
                (
                    attended,
                    attendance_time,
                    special_accommodations,
                    student_id,
                    activity_id,
                    attendance_date,
                ),
            )

            connection.commit()

            if cursor.rowcount > 0:
                print(f"✅ Attendance updated in {table}")
                return True
            else:
                print(f"⚠️ No matching attendance found to update")
                return False

        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error updating attendance: {e}")
            return False

        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def delete_attendance(student_id, activity_id, attendance_date, activity_type):
        """
        Deletes an attendance record.

        Args:
            student_id: Student ID
            activity_id: Activity ID
            attendance_date: Date of attendance
            activity_type: Type of activity (determines table)

        Returns:
            bool: True if successful, False otherwise
        """
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            # Select appropriate table
            if activity_type == "Lecture":
                table = "Student_Lecture_Attendance"
            elif activity_type == "Tutorial":
                table = "Student_Tutorial_Attendance"
            elif activity_type == "Practical":
                table = "Student_Practical_Attendance"
            else:
                raise ValueError(f"Invalid activity_type: {activity_type}")

            sql = f"""
                DELETE FROM {table}
                WHERE student_id = %s
                  AND activity_id = %s
                  AND attendance_date = %s;
            """

            cursor.execute(sql, (student_id, activity_id, attendance_date))
            connection.commit()

            if cursor.rowcount > 0:
                print(f"✅ Attendance deleted from {table}")
                return True
            else:
                print(f"⚠️ No matching attendance found to delete")
                return False

        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error deleting attendance: {e}")
            return False

        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_activities():
        """
        Retrieves all activities from Activity table with course names.
        Used to populate activity dropdowns in UI.

        Returns:
            list: List of tuples (activity_id, activity_display_name)
        """
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = """
                SELECT
                    A.Activity_ID,
                    A.Activity_Type || ' - ' || C.name AS activity_name
                FROM Activity A
                JOIN Course C ON A.course_id = C.course_id
                             AND A.department_id = C.department_id
                ORDER BY C.name, A.Activity_Type;
            """

            cursor.execute(sql)
            return cursor.fetchall()

        except Exception as e:
            print(f"❌ Error fetching activities: {e}")
            return []

        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_attendance_for_percent(student_id, activity_id):
        """
        Calculates attendance statistics for percentage calculation.
        Counts total attendance records and number of times student attended.

        Args:
            student_id: Student ID
            activity_id: Activity ID

        Returns:
            tuple: (total_count, attended_count)
        """
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            # Query all three attendance tables and aggregate results
            sql = """
                SELECT
                    COUNT(*) AS total,
                    SUM(CASE WHEN attended THEN 1 ELSE 0 END) AS attended_count
                FROM (
                    -- Lecture attendance
                    SELECT attended
                    FROM Student_Lecture_Attendance
                    WHERE student_id = %s AND activity_id = %s

                    UNION ALL

                    -- Tutorial attendance
                    SELECT attended
                    FROM Student_Tutorial_Attendance
                    WHERE student_id = %s AND activity_id = %s

                    UNION ALL

                    -- Practical attendance
                    SELECT attended
                    FROM Student_Practical_Attendance
                    WHERE student_id = %s AND activity_id = %s
                ) AS all_attendance;
            """

            cursor.execute(
                sql,
                (
                    student_id,
                    activity_id,  # Lecture
                    student_id,
                    activity_id,  # Tutorial
                    student_id,
                    activity_id,  # Practical
                ),
            )

            result = cursor.fetchone()

            if result and result[0] is not None:
                total = result[0]
                attended_count = result[1] if result[1] is not None else 0
                return (total, attended_count)
            else:
                return (0, 0)

        except Exception as e:
            print(f"❌ Error fetching attendance for percent: {e}")
            return (0, 0)

        finally:
            close_cursor(cursor)
            close_connection(connection)
