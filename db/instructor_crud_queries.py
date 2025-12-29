# New file: db/instructor_crud_queries.py
from db.connection import close_connection, close_cursor, get_connection, get_cursor


class InstructorCRUD:
    @staticmethod
    def create_instructor(
        department_id, last_name, first_name, rank, phone, fax, email
    ):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = """
                INSERT INTO instructor (department_id, last_name, first_name, rank, phone, fax, email)
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING instructor_id;
            """
            cursor.execute(
                sql, (department_id, last_name, first_name, rank, phone, fax, email)
            )
            new_id = cursor.fetchone()[0]
            connection.commit()
            print(f"✅ Instructor created with ID: {new_id}")
            return True
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error creating instructor: {e}")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_all_instructors(
        search_field=None, search_value=None, sort_by="instructor_id", sort_order="ASC"
    ):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = """
                SELECT instructor_id, department_id, last_name, first_name, rank, phone, fax, email
                FROM instructor
            """
            params = []

            if search_field and search_value:
                if search_field == "ID":
                    sql += " WHERE CAST(instructor_id AS TEXT) LIKE %s"
                    params.append(f"%{search_value}%")
                elif search_field == "Last Name":
                    sql += " WHERE LOWER(last_name) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")
                elif search_field == "First Name":
                    sql += " WHERE LOWER(first_name) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")
                elif search_field == "Rank":
                    sql += " WHERE LOWER(rank) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")
                elif search_field == "Email":
                    sql += " WHERE LOWER(email) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")

            if sort_by not in [
                "instructor_id",
                "last_name",
                "first_name",
                "rank",
                "department_id",
            ]:
                sort_by = "instructor_id"
            if sort_order not in ["ASC", "DESC"]:
                sort_order = "ASC"

            sql += f" ORDER BY {sort_by} {sort_order}"

            cursor.execute(sql, params)
            results = cursor.fetchall()
            print(f"✅ Retrieved {len(results)} instructors")
            return results
        except Exception as e:
            print(f"❌ Error fetching instructors: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def update_instructor(
        instructor_id, department_id, last_name, first_name, rank, phone, fax, email
    ):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = """
                UPDATE instructor SET department_id = %s, last_name = %s, first_name = %s,
                rank = %s, phone = %s, fax = %s, email = %s WHERE instructor_id = %s;
            """
            cursor.execute(
                sql,
                (
                    department_id,
                    last_name,
                    first_name,
                    rank,
                    phone,
                    fax,
                    email,
                    instructor_id,
                ),
            )
            rows_affected = cursor.rowcount
            connection.commit()

            if rows_affected > 0:
                print(f"✅ Instructor {instructor_id} updated")
                return True
            else:
                print(f"⚠️ No instructor found with ID {instructor_id}")
                return False
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error updating instructor: {e}")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def delete_instructor(instructor_id):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = "DELETE FROM instructor WHERE instructor_id = %s;"
            cursor.execute(sql, (instructor_id,))
            rows_affected = cursor.rowcount
            connection.commit()

            if rows_affected > 0:
                print(f"✅ Instructor {instructor_id} deleted")
                return True
            else:
                print(f"⚠️ No instructor found with ID {instructor_id}")
                return False
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error deleting instructor: {e}")
            if "foreign key" in str(e).lower() or "violates" in str(e).lower():
                print("⚠️ Cannot delete: Instructor is referenced in other records")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)
