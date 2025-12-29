from db.connection import close_connection, close_cursor, get_connection, get_cursor


class RoomCRUD:
    @staticmethod
    def create_room(building, roomno, capacity):
        """INSERT a new room into the database"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = "INSERT INTO room (building, roomno, capacity) VALUES (%s, %s, %s);"
            cursor.execute(sql, (building, roomno, capacity))
            connection.commit()

            print(f"✅ Room created successfully")
            return True
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error creating room: {e}")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_all_rooms(
        search_field=None, search_value=None, sort_by="building", sort_order="ASC"
    ):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = "SELECT building, roomno, capacity FROM room"
            params = []

            if search_field and search_value:
                if search_field == "Building":
                    sql += " WHERE LOWER(building) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")
                elif search_field == "RoomNo":
                    sql += " WHERE LOWER(roomno) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")
                elif search_field == "Capacity":
                    sql += " WHERE CAST(capacity AS TEXT) LIKE %s"
                    params.append(f"%{search_value}%")

            if sort_by not in ["building", "roomno", "capacity"]:
                sort_by = "building"
            if sort_order not in ["ASC", "DESC"]:
                sort_order = "ASC"

            sql += f" ORDER BY {sort_by} {sort_order}"

            cursor.execute(sql, params)
            results = cursor.fetchall()

            print(f"✅ Retrieved {len(results)} rooms")
            return results
        except Exception as e:
            print(f"❌ Error fetching rooms: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def update_room(building, roomno, capacity):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = "UPDATE room SET capacity = %s WHERE building = %s AND roomno = %s"
            cursor.execute(sql, (capacity, building, roomno))
            rows_affected = cursor.rowcount
            connection.commit()

            if rows_affected > 0:
                print(f"✅ Room updated successfully")
                return True
            else:
                print(f"⚠️ No room found with Building: {building}, Room No: {roomno}")
                return False
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error updating room: {e}")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def delete_room(building, roomno):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = "DELETE FROM room WHERE building = %s AND roomno = %s"
            cursor.execute(sql, (building, roomno))
            rows_affected = cursor.rowcount
            connection.commit()

            if rows_affected > 0:
                print(f"✅ Room deleted successfully")
                return True
            else:
                print(f"⚠️ No room found with Building: {building}, Room No: {roomno}")
                return False
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error deleting room: {e}")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)
