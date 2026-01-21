from db.connection import close_connection, close_cursor, get_connection, get_cursor


class ActivityCRUD:
    @staticmethod
    def create_activity(course_id, department_id, activity_type):
        """
        Create an activity and its corresponding subtype (Lecture/Tutorial/Practical)
        Note: Lecture is created automatically via trigger, so this is mainly for Tutorial/Practical
        """
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            # Check if this activity type already exists for this course
            cursor.execute(
                """
                SELECT activity_id FROM activity
                WHERE course_id = %s AND department_id = %s AND activity_type = %s
            """,
                (course_id, department_id, activity_type),
            )

            if cursor.fetchone():
                print(
                    f"Activity type '{activity_type}' already exists for this course"
                )
                return False

            sql_activity = """
                INSERT INTO activity (course_id, department_id, activity_type)
                VALUES (%s, %s, %s) RETURNING activity_id;
            """
            cursor.execute(sql_activity, (course_id, department_id, activity_type))
            new_activity_id = cursor.fetchone()[0]

            # Insert into corresponding subtype table
            if activity_type == "Lecture":
                cursor.execute(
                    "INSERT INTO lecture (activity_id) VALUES (%s)", (new_activity_id,)
                )
            elif activity_type == "Tutorial":
                cursor.execute(
                    "INSERT INTO tutorial (activity_id) VALUES (%s)", (new_activity_id,)
                )
            elif activity_type == "Practical":
                cursor.execute(
                    "INSERT INTO practical (activity_id) VALUES (%s)",
                    (new_activity_id,),
                )

            connection.commit()
            print(f" {activity_type} activity created with ID: {new_activity_id}")
            return True
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Error creating activity: {e}")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_all_activities(
        search_field=None, search_value=None, sort_by="activity_id", sort_order="ASC"
    ):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = """
                SELECT a.activity_id, a.course_id, a.department_id,
                       c.name as course_name, d.name as dept_name, a.activity_type
                FROM activity a
                LEFT JOIN course c ON a.course_id = c.course_id AND a.department_id = c.department_id
                LEFT JOIN department d ON a.department_id = d.department_id
            """
            params = []

            if search_field and search_value:
                if search_field == "Activity ID":
                    sql += " WHERE CAST(a.activity_id AS TEXT) LIKE %s"
                    params.append(f"%{search_value}%")
                elif search_field == "Course ID":
                    sql += " WHERE CAST(a.course_id AS TEXT) LIKE %s"
                    params.append(f"%{search_value}%")
                elif search_field == "Course Name":
                    sql += " WHERE LOWER(c.name) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")
                elif search_field == "Activity Type":
                    sql += " WHERE LOWER(a.activity_type) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")

            if sort_by not in [
                "activity_id",
                "course_id",
                "department_id",
                "activity_type",
                "course_name",
            ]:
                sort_by = "activity_id"
            if sort_order not in ["ASC", "DESC"]:
                sort_order = "ASC"

            sql += f" ORDER BY {sort_by} {sort_order}"

            cursor.execute(sql, params)
            results = cursor.fetchall()
            print(f" Retrieved {len(results)} activities")
            return results
        except Exception as e:
            print(f"Error fetching activities: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def update_activity(activity_id, course_id, department_id, activity_type):
        """
        Update activity - NOTE: Changing activity_type will require special handling
        This updates the activity type and moves it to the correct subtype table
        """
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            # Get current activity info
            cursor.execute(
                """
                SELECT course_id, department_id, activity_type
                FROM activity WHERE activity_id = %s
            """,
                (activity_id,),
            )

            result = cursor.fetchone()
            if not result:
                print(f" No activity found with ID {activity_id}")
                return False

            old_course_id, old_dept_id, old_type = result

            # Check if new activity type already exists for the new course
            if (
                course_id != old_course_id
                or department_id != old_dept_id
                or activity_type != old_type
            ):
                cursor.execute(
                    """
                    SELECT activity_id FROM activity
                    WHERE course_id = %s AND department_id = %s
                    AND activity_type = %s AND activity_id != %s
                """,
                    (course_id, department_id, activity_type, activity_id),
                )

                if cursor.fetchone():
                    print(
                        f" Activity type '{activity_type}' already exists for this course"
                    )
                    return False

            # If activity type changed, handle subtype table changes
            if activity_type != old_type:
                # Delete from old subtype table
                if old_type == "Lecture":
                    cursor.execute(
                        "DELETE FROM lecture WHERE activity_id = %s", (activity_id,)
                    )
                elif old_type == "Tutorial":
                    cursor.execute(
                        "DELETE FROM tutorial WHERE activity_id = %s", (activity_id,)
                    )
                elif old_type == "Practical":
                    cursor.execute(
                        "DELETE FROM practical WHERE activity_id = %s", (activity_id,)
                    )

                # Insert into new subtype table
                if activity_type == "Lecture":
                    cursor.execute(
                        "INSERT INTO lecture (activity_id) VALUES (%s)", (activity_id,)
                    )
                elif activity_type == "Tutorial":
                    cursor.execute(
                        "INSERT INTO tutorial (activity_id) VALUES (%s)", (activity_id,)
                    )
                elif activity_type == "Practical":
                    cursor.execute(
                        "INSERT INTO practical (activity_id) VALUES (%s)",
                        (activity_id,),
                    )

            # Update main activity table
            sql = """
                UPDATE activity
                SET course_id = %s, department_id = %s, activity_type = %s
                WHERE activity_id = %s;
            """
            cursor.execute(sql, (course_id, department_id, activity_type, activity_id))

            connection.commit()
            print(f"Activity {activity_id} updated")
            return True
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Error updating activity: {e}")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def delete_activity(activity_id):
        """
        Delete activity - CASCADE will handle subtype table deletion
        """
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            # Check if it's a mandatory lecture
            cursor.execute(
                """
                SELECT activity_type FROM activity WHERE activity_id = %s
            """,
                (activity_id,),
            )

            result = cursor.fetchone()
            if result and result[0] == "Lecture":
                print(
                    "⚠️ Cannot delete Lecture activity - it's mandatory for the course"
                )
                return False

            sql = "DELETE FROM activity WHERE activity_id = %s;"
            cursor.execute(sql, (activity_id,))
            rows_affected = cursor.rowcount
            connection.commit()

            if rows_affected > 0:
                print(f"Activity {activity_id} deleted")
                return True
            else:
                print(f" No activity found with ID {activity_id}")
                return False
        except Exception as e:
            if connection:
                connection.rollback()
            print(f" Error deleting activity: {e}")
            if "foreign key" in str(e).lower() or "violates" in str(e).lower():
                print(" Cannot delete: Activity is referenced in other records")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_all_courses():
        """Helper method to get courses for dropdown"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            cursor.execute(
                """
                SELECT c.course_id, c.department_id, c.name, d.name as dept_name
                FROM course c
                LEFT JOIN department d ON c.department_id = d.department_id
                ORDER BY c.name
            """
            )
            return cursor.fetchall()
        except Exception as e:
            print(f" Error fetching courses: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_activity_counts_for_course(course_id, department_id):
        """Check which activity types exist for a course"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            cursor.execute(
                """
                SELECT activity_type, COUNT(*)
                FROM activity
                WHERE course_id = %s AND department_id = %s
                GROUP BY activity_type
            """,
                (course_id, department_id),
            )
            return dict(cursor.fetchall())
        except Exception as e:
            print(f" Error checking activity counts: {e}")
            return {}
        finally:
            close_cursor(cursor)
            close_connection(connection)
