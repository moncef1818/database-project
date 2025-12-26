from db.connection import get_connection , get_cursor , close_connection , close_cursor

class DepartmentCRUD:
    @staticmethod
    def create_department(name):
        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = "insert into department (name) values (%s) returning department_id;"

            cursor.execute(sql , (name,))
            new_id = cursor.fetchone()[0]

            connection.commit()
            print(f"✅ Department created with ID: {new_id}")
            return new_id
        except Exception as e :
            if connection:
                connection.rollback()
                print(f"❌ Error creating department: {e}")
            return None
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_all_departments(search_field=None, search_value=None, sort_by='department_id', sort_order='ASC'):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = "SELECT department_id, name FROM department"
            params = []

            if search_field and search_value:
                if search_field == 'ID':
                    sql += " WHERE CAST(department_id AS TEXT) LIKE %s"
                    params.append(f"%{search_value}%")
                elif search_field == 'Name':
                    sql += " WHERE LOWER(name) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")

            if sort_by not in ['department_id', 'name']:
                sort_by = 'department_id'
            if sort_order not in ['ASC', 'DESC']:
                sort_order = 'ASC'
        
            sql += f" ORDER BY {sort_by} {sort_order}"

            cursor.execute(sql, params)
            results = cursor.fetchall()

            print(f"✅ Retrieved {len(results)} departments")
            return results
        
        except Exception as e:
            print(f"❌ Error fetching departments: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)