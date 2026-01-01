from db.connection import close_connection, close_cursor, get_connection, get_cursor


class ResultsQueries:
    @staticmethod
    def execute_function(function_name, params=()):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            placeholders = ", ".join("%s" for _ in params)
            sql = f"SELECT * FROM {function_name}({placeholders});"
            cursor.execute(sql, params)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]  # type:ignore
            print(f" executed {function_name} , retrieved {len(results)} rows ")
            return results, columns
        except Exception as e:
            print(f"❌ Error executing {function_name}: {e}")
            return [], []
        finally:
            close_cursor(cursor)
            close_connection(connection)
