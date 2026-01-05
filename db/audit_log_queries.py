from db.connection import get_connection, get_cursor, close_connection, close_cursor

class AuditLogQueries:
    @staticmethod
    def get_audit_logs(search_field=None, search_value=None, sort_by='log_id', sort_order='ASC'):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = get_cursor(conn)
            sql = "select * from audit_log"
            params = []

            if search_field and search_value:
                if search_field == 'ID':
                    sql += " where cast(audit_id as text) like %s"
                    params.append(f"%{search_value}%")
                elif search_field == 'Table Name':
                    sql += " where lower(table_name) like lower(%s)"
                    params.append(f"%{search_value}%")
                elif search_field == 'Operation':
                    sql += " where lower(operation) like lower(%s)"
                    params.append(f"%{search_value}%")
                elif search_field == 'Timestamp':
                    sql += " where cast(timestamp as text) like %s"
                    params.append(f"%{search_value}%")
                elif search_field == 'User':
                    sql += " where lower(user_name) like lower(%s)"
                    params.append(f"%{search_value}%")

            if sort_by not in ['audit_id', 'table_name', 'operation', 'timestamp']:
                sort_by = 'audit_id'
            if sort_order not in ['ASC', 'DESC']:
                sort_order = 'ASC'
            sql += f" order by {sort_by} {sort_order}"

            cursor.execute(sql, params)
            results = cursor.fetchall()
            print(f"✅ Retrieved {len(results)} audit logs")

            return results
        except Exception as e:
            print(f"❌ Error fetching audit logs: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(conn)