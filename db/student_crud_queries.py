from db.connection import close_connection, close_cursor, get_connection, get_cursor


class StudentCRUD:
    @staticmethod
    def get_all_groups():
        """Helper to fetch groups for the dropdown (including Section name)"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            # Joins with Section to make the group name more descriptive
            sql = """
                SELECT g.Group_ID, g.Group_Name, s.Name as Section_Name
                FROM "Group" g
                LEFT JOIN Section s ON g.Section_ID = s.Section_ID
                ORDER BY s.Name, g.Group_Name
            """
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching groups: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def create_student(
        first_name, last_name, dob, group_id, email, phone, address, city, zip_code
    ):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = """
                INSERT INTO Student (
                    First_Name, Last_Name, DOB, Group_ID,
                    Email, Phone, Address, City, Zip_Code
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            # If group_id is 0 or None, we insert NULL
            g_id = group_id if group_id and group_id > 0 else None

            cursor.execute(
                sql,
                (
                    first_name,
                    last_name,
                    dob,
                    g_id,
                    email,
                    phone,
                    address,
                    city,
                    zip_code,
                ),
            )
            connection.commit()
            return True
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Error creating student: {e}")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_all_students(search_field=None, search_value=None):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            # Join with Group and Section to show readable names in the table
            sql = """
                SELECT s.Student_ID, s.First_Name, s.Last_Name, s.DOB,
                       g.Group_Name, sec.Name as Section_Name,
                       s.Email, s.Phone, s.Group_ID
                FROM Student s
                LEFT JOIN "Group" g ON s.Group_ID = g.Group_ID
                LEFT JOIN Section sec ON g.Section_ID = sec.Section_ID
            """
            params = []

            if search_field and search_value:
                if search_field == "Student ID":
                    sql += " WHERE CAST(s.Student_ID AS TEXT) LIKE %s"
                    params.append(f"%{search_value}%")
                elif search_field == "Last Name":
                    sql += " WHERE LOWER(s.Last_Name) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")
                elif search_field == "Group":
                    sql += " WHERE LOWER(g.Group_Name) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")

            sql += " ORDER BY s.Student_ID ASC"
            cursor.execute(sql, params)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching students: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_student_details(student_id):
        """Fetches full details for a single student to populate update forms"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            sql = """
                SELECT First_Name, Last_Name, DOB, Group_ID, Email, Phone, Address, City, Zip_Code
                FROM Student WHERE Student_ID = %s
            """
            cursor.execute(sql, (student_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error fetching student details: {e}")
            return None
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def update_student(
        student_id,
        first_name,
        last_name,
        dob,
        group_id,
        email,
        phone,
        address,
        city,
        zip_code,
    ):
        """Updates an existing student record"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            sql = """
                UPDATE Student
                SET First_Name = %s, Last_Name = %s, DOB = %s, Group_ID = %s,
                    Email = %s, Phone = %s, Address = %s, City = %s, Zip_Code = %s
                WHERE Student_ID = %s
            """
            g_id = group_id if group_id and group_id > 0 else None
            cursor.execute(
                sql,
                (
                    first_name,
                    last_name,
                    dob,
                    g_id,
                    email,
                    phone,
                    address,
                    city,
                    zip_code,
                    student_id,
                ),
            )
            connection.commit()
            return True
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Error updating student: {e}")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def delete_student(student_id):
        """Deletes a student record by ID"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            cursor.execute("DELETE FROM Student WHERE Student_ID = %s", (student_id,))
            connection.commit()
            return True
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Error deleting student: {e}")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)
