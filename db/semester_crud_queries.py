# New file: db/semester_crud_queries.py
from db.connection import close_connection, close_cursor, get_connection, get_cursor


class SemesterCRUD:
    @staticmethod
    def create_semester(name, start_date, end_date):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = """
                INSERT INTO semester (name, start_date, end_date)
                VALUES (%s, %s, %s) RETURNING semester_id;
            """
            cursor.execute(sql, (name, start_date, end_date))
            new_id = cursor.fetchone()[0]
            connection.commit()
            print(f" Semester created with ID: {new_id}")
            return True
        except Exception as e:
            if connection:
                connection.rollback()
            print(f" Error creating semester: {e}")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_all_semesters(
        search_field=None, search_value=None, sort_by="semester_id", sort_order="ASC"
    ):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = """
                SELECT semester_id, name, start_date, end_date
                FROM semester
            """
            params = []

            if search_field and search_value:
                if search_field == "ID":
                    sql += " WHERE CAST(semester_id AS TEXT) LIKE %s"
                    params.append(f"%{search_value}%")
                elif search_field == "Name":
                    sql += " WHERE LOWER(name) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")
                elif search_field == "Year":
                    sql += " WHERE CAST(EXTRACT(YEAR FROM start_date) AS TEXT) LIKE %s"
                    params.append(f"%{search_value}%")

            if sort_by not in [
                "semester_id",
                "name",
                "start_date",
                "end_date",
            ]:
                sort_by = "semester_id"
            if sort_order not in ["ASC", "DESC"]:
                sort_order = "ASC"

            sql += f" ORDER BY {sort_by} {sort_order}"

            cursor.execute(sql, params)
            results = cursor.fetchall()
            print(f" Retrieved {len(results)} semesters")
            return results
        except Exception as e:
            print(f" Error fetching semesters: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def update_semester(semester_id, name, start_date, end_date):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = """
                UPDATE semester
                SET name = %s, start_date = %s, end_date = %s
                WHERE semester_id = %s;
            """
            cursor.execute(sql, (name, start_date, end_date, semester_id))
            rows_affected = cursor.rowcount
            connection.commit()

            if rows_affected > 0:
                print(f" Semester {semester_id} updated")
                return True
            else:
                print(f" No semester found with ID {semester_id}")
                return False
        except Exception as e:
            if connection:
                connection.rollback()
            print(f" Error updating semester: {e}")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def delete_semester(semester_id):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = "DELETE FROM semester WHERE semester_id = %s;"
            cursor.execute(sql, (semester_id,))
            rows_affected = cursor.rowcount
            connection.commit()

            if rows_affected > 0:
                print(f" Semester {semester_id} deleted")
                return True
            else:
                print(f"No semester found with ID {semester_id}")
                return False
        except Exception as e:
            if connection:
                connection.rollback()
            print(f" Error deleting semester: {e}")
            if "foreign key" in str(e).lower() or "violates" in str(e).lower():
                print(" Cannot delete: Semester is referenced in other records")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)
