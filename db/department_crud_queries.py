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

    @staticmethod
    def update_department(department_id, name ):
        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = "UPDATE department SET name = %s WHERE department_id = %s;"
            cursor.execute(sql , (name, department_id))
            rows_affected = cursor.rowcount

            connection.commit()

            if rows_affected > 0:
                print(f"✅ Department ID {department_id} updated successfully")
                return True
            else:
                print(f"⚠️ No department found with ID {department_id}")
                return False
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error updating department: {e}")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)



    @staticmethod
    def delete_department(dept_id):
        """DELETE a department"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            
            sql = "DELETE FROM department WHERE department_id = %s"
            
            cursor.execute(sql, (dept_id,))
            rows_affected = cursor.rowcount
            
            connection.commit()
            
            if rows_affected > 0:
                print(f"✅ Department {dept_id} deleted successfully")
                return True
            else:
                print(f"⚠️ No department found with ID {dept_id}")
                return False
                
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error deleting department: {e}")
            
            # Check if it's a foreign key constraint error
            if 'foreign key' in str(e).lower() or 'violates' in str(e).lower():
                print("⚠️ Cannot delete: Department is being used by other records")
            
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)