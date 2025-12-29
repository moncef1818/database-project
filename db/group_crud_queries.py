from db.connection import get_connection, get_cursor, close_connection, close_cursor


class GroupCRUD:
    @staticmethod
    def create_group(name, section_id):
        """Create a new group"""
        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            # Fixed: table name is "group" not group, column is group_name not name
            sql = 'INSERT INTO "Group" (group_name, section_id) VALUES (%s, %s) RETURNING group_id;'

            cursor.execute(sql, (name, section_id))
            new_id = cursor.fetchone()[0]

            connection.commit()
            print(f"✅ Group created with ID: {new_id}")
            return new_id
            
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error creating group: {e}")
            return None
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_all_sections(search_field=None, search_value=None, sort_by='section_id', sort_order='ASC'):
        """Get all sections for dropdown/combobox"""
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
    def get_all_groups(search_field=None, search_value=None, sort_by='group_id', sort_order='ASC'):
        """Get all groups with section info using JOIN"""
        connection = None
        cursor = None
        
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            # Base SQL with JOIN
            sql = """
                SELECT 
                    g.group_id,
                    g.group_name,
                    g.section_id,
                    s.name AS section_name
                FROM "Group" g
                INNER JOIN section s ON g.section_id = s.section_id
            """
            params = []

            # Add WHERE clause if searching
            if search_field and search_value:
                # Handle different field types
                if search_field in ['group_id', 'section_id']:
                    sql += f" WHERE g.{search_field} = %s"
                    params.append(search_value)
                elif search_field == 'group_name':
                    sql += " WHERE LOWER(g.group_name) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")

            # Validate and add ORDER BY
            if sort_by not in ['group_id', 'group_name', 'section_id']:
                sort_by = 'group_id'
            if sort_order not in ['ASC', 'DESC']:
                sort_order = 'ASC'
                
            sql += f" ORDER BY g.{sort_by} {sort_order};"

            cursor.execute(sql, params)
            groups = cursor.fetchall()

            print(f"✅ Retrieved {len(groups)} groups")
            return groups

        except Exception as e:
            print(f"❌ Error fetching groups: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_group_by_id(group_id):
        """Get a single group by ID with section info"""
        connection = None
        cursor = None
        
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = """
                SELECT 
                    g.group_id,
                    g.group_name,
                    g.section_id,
                    s.name AS section_name
                FROM "Group" g
                INNER JOIN section s ON g.section_id = s.section_id
                WHERE g.group_id = %s;
            """

            cursor.execute(sql, (group_id,))
            group = cursor.fetchone()

            return group

        except Exception as e:
            print(f"❌ Error fetching group: {e}")
            return None
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def update_group(group_id, name, section_id):
        """Update a group - can update name and/or section"""
        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            # Build dynamic update based on what's provided
            fields = []
            params = []

            if name is not None:
                fields.append("group_name = %s")
                params.append(name)
            
            if section_id is not None:
                fields.append("section_id = %s")
                params.append(section_id)

            if not fields:
                print("⚠️ No fields to update")
                return False

            # Add group_id to params
            params.append(group_id)

            sql = f'UPDATE "Group" SET {", ".join(fields)} WHERE group_id = %s;'
            cursor.execute(sql, params)
            rows_affected = cursor.rowcount

            connection.commit()

            if rows_affected > 0:
                print(f"✅ Group ID {group_id} updated successfully")
                return True
            else:
                print(f"⚠️ No group found with ID {group_id}")
                return False
                
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error updating group: {e}")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def delete_group(group_id):
        """Delete a group by ID"""
        connection = None
        cursor = None
        
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = 'DELETE FROM "Group" WHERE group_id = %s;'

            cursor.execute(sql, (group_id,))
            rows_affected = cursor.rowcount
            
            connection.commit()
            
            if rows_affected > 0:
                print(f"✅ Group {group_id} deleted successfully")
                return True
            else:
                print(f"⚠️ No group found with ID {group_id}")
                return False
                
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error deleting group: {e}")
            
            # Check if it's a foreign key constraint error
            if 'foreign key' in str(e).lower() or 'violates' in str(e).lower():
                print("⚠️ Cannot delete: Group is being used by students")
            
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)
