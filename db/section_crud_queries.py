from db.connection import get_connection , get_cursor , close_connection , close_cursor

class SectionCRUD:
    @staticmethod
    def create_section(name):
        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = "insert into section (name) values (%s) returning section_id;"

            cursor.execute(sql , (name,))
            new_id = cursor.fetchone()[0]

            connection.commit()
            print(f"✅ Section created with ID: {new_id}")
            return new_id
        except Exception as e :
            if connection:
                connection.rollback()
                print(f"❌ Error creating section: {e}")
            return None
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_all_sections(search_field=None, search_value=None, sort_by='section_id', sort_order='ASC'):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = "SELECT section_id, name FROM section"
            params = []

            if search_field and search_value:
                if search_field == 'ID':
                    sql += " WHERE CAST(section_id AS TEXT) LIKE %s"
                    params.append(f"%{search_value}%")
                elif search_field == 'Name':
                    sql += " WHERE LOWER(name) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")

            if sort_by not in ['section_id', 'name']:
                sort_by = 'section_id'
            if sort_order not in ['ASC', 'DESC']:
                sort_order = 'ASC'
        
            sql += f" ORDER BY {sort_by} {sort_order}"

            cursor.execute(sql, params)
            results = cursor.fetchall()

            print(f"✅ Retrieved {len(results)} sections")
            return results
        
        except Exception as e:
            print(f"❌ Error fetching sections: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def update_section(section_id, name):
        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = "UPDATE section SET name = %s WHERE section_id = %s;"
            cursor.execute(sql , (name, section_id))
            rows_affected = cursor.rowcount

            connection.commit()

            if rows_affected > 0:
                print(f"✅ Section ID {section_id} updated successfully")
                return True
            else:
                print(f"⚠️ No section found with ID {section_id}")
                return False
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error updating section: {e}")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)



    @staticmethod
    def delete_section(section_id):
        """DELETE a section"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = "DELETE FROM section WHERE section_id = %s"

            cursor.execute(sql, (section_id,))
            rows_affected = cursor.rowcount
            
            connection.commit()
            
            if rows_affected > 0:
                print(f"✅ Section {section_id} deleted successfully")
                return True
            else:
                print(f"⚠️ No section found with ID {section_id}")
                return False
                
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error deleting section: {e}")
            
            # Check if it's a foreign key constraint error
            if 'foreign key' in str(e).lower() or 'violates' in str(e).lower():
                print("⚠️ Cannot delete: Section is being used by other records")
            
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)