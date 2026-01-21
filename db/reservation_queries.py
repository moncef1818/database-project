from db.connection import get_connection, get_cursor, close_connection, close_cursor


class ReservationQueries:
    
    @staticmethod
    def create_reservation(building, room_no, course_id, department_id, 
                          activity_type, instructor_id, reserv_date, 
                          start_time, end_time, hours_number):
        """Create a new reservation"""
        connection = None
        cursor = None
        
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            
            sql = """
                INSERT INTO reservation (building, roomno, course_id, department_id, 
                                        activity_type, instructor_id, reserv_date, 
                                        start_time, end_time, hours_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING reservation_id;
            """
            
            cursor.execute(sql, (building, room_no, course_id, department_id,
                                activity_type, instructor_id, reserv_date,
                                start_time, end_time, hours_number))
            
            new_id = cursor.fetchone()[0]
            connection.commit()
            print(f"✅ Reservation created with ID: {new_id}")
            return new_id
            
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error creating reservation: {e}")
            raise e
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_all_reservations(search_field=None, search_value=None, 
                            sort_by='reserv_date', sort_order='ASC'):
        """Get all reservations with course and instructor details"""
        connection = None
        cursor = None
        
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            
            sql = """
                SELECT 
                    r.reservation_id,
                    r.reserv_date,
                    r.start_time,
                    r.end_time,
                    r.hours_number,
                    c.name AS course_name,
                    d.name AS department_name,
                    r.activity_type,
                    i.last_name || ' ' || i.first_name AS instructor_name,
                    r.building,
                    r.roomno,
                    r.course_id,
                    r.department_id,
                    r.instructor_id
                FROM reservation r
                JOIN course c ON r.course_id = c.course_id
                JOIN department d ON r.department_id = d.department_id
                JOIN instructor i ON r.instructor_id = i.instructor_id
            """
            
            params = []
            
            if search_field and search_value:
                if search_field == 'course_name':
                    sql += " WHERE LOWER(c.name) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")
                elif search_field == 'instructor_name':
                    sql += " WHERE LOWER(i.last_name || ' ' || i.first_name) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")
                elif search_field == 'activity_type':
                    sql += " WHERE r.activity_type = %s"
                    params.append(search_value)
                elif search_field == 'building':
                    sql += " WHERE r.building = %s"
                    params.append(search_value)
                elif search_field == 'reserv_date':
                    sql += " WHERE r.reserv_date = %s"
                    params.append(search_value)
            
            valid_sort = ['reserv_date', 'start_time', 'course_name', 'instructor_name', 'building']
            if sort_by not in valid_sort:
                sort_by = 'reserv_date'
            if sort_order not in ['ASC', 'DESC']:
                sort_order = 'ASC'
            
            sql += f" ORDER BY {sort_by} {sort_order}, r.start_time ASC;"
            
            cursor.execute(sql, params)
            results = cursor.fetchall()
            
            print(f"✅ Retrieved {len(results)} reservations")
            return results
            
        except Exception as e:
            print(f"❌ Error fetching reservations: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_reservation_by_id(reservation_id):
        """Get a single reservation by ID"""
        connection = None
        cursor = None
        
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            
            sql = """
                SELECT 
                    r.reservation_id, r.building, r.roomno, r.course_id, 
                    r.department_id, r.activity_type, r.instructor_id,
                    r.reserv_date, r.start_time, r.end_time, r.hours_number,
                    c.name AS course_name,
                    i.last_name || ' ' || i.first_name AS instructor_name
                FROM reservation r
                JOIN course c ON r.course_id = c.course_id
                JOIN instructor i ON r.instructor_id = i.instructor_id
                WHERE r.reservation_id = %s;
            """
            
            cursor.execute(sql, (reservation_id,))
            return cursor.fetchone()
            
        except Exception as e:
            print(f"❌ Error fetching reservation: {e}")
            return None
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def update_reservation(reservation_id, building, room_no, course_id, 
                          department_id, activity_type, instructor_id, 
                          reserv_date, start_time, end_time, hours_number):
        """Update a reservation"""
        connection = None
        cursor = None
        
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            
            sql = """
                UPDATE reservation 
                SET building = %s, roomno = %s, course_id = %s, 
                    department_id = %s, activity_type = %s, instructor_id = %s,
                    reserv_date = %s, start_time = %s, end_time = %s, 
                    hours_number = %s
                WHERE reservation_id = %s;
            """
            
            cursor.execute(sql, (building, room_no, course_id, department_id,
                                activity_type, instructor_id, reserv_date,
                                start_time, end_time, hours_number, reservation_id))
            
            rows_affected = cursor.rowcount
            connection.commit()
            
            if rows_affected > 0:
                print(f"✅ Reservation {reservation_id} updated successfully")
                return True
            else:
                print(f"⚠️ No reservation found with ID {reservation_id}")
                return False
                
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error updating reservation: {e}")
            raise e
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def delete_reservation(reservation_id):
        """Delete a reservation by ID"""
        connection = None
        cursor = None
        
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            
            sql = "DELETE FROM reservation WHERE reservation_id = %s;"
            cursor.execute(sql, (reservation_id,))
            rows_affected = cursor.rowcount
            connection.commit()
            
            if rows_affected > 0:
                print(f"✅ Reservation {reservation_id} deleted successfully")
                return True
            else:
                print(f"⚠️ No reservation found with ID {reservation_id}")
                return False
                
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error deleting reservation: {e}")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def check_room_conflict(building, room_no, reserv_date, start_time, end_time, exclude_id=None):
        """Check if room is already booked at this time"""
        connection = None
        cursor = None
        
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            
            sql = """
                SELECT reservation_id, start_time, end_time,
                       c.name AS course_name
                FROM reservation r
                JOIN course c ON r.course_id = c.course_id
                WHERE r.building = %s 
                AND r.roomno = %s
                AND r.reserv_date = %s
                AND r.start_time < %s
                AND r.end_time > %s
            """
            
            params = [building, room_no, reserv_date, end_time, start_time]
            
            if exclude_id:
                sql += " AND r.reservation_id != %s"
                params.append(exclude_id)
            
            cursor.execute(sql, params)
            conflicts = cursor.fetchall()
            
            return conflicts
            
        except Exception as e:
            print(f"❌ Error checking room conflict: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def check_instructor_conflict(instructor_id, reserv_date, start_time, end_time, exclude_id=None):
        """Check if instructor is already assigned at this time"""
        connection = None
        cursor = None
        
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            
            sql = """
                SELECT reservation_id, start_time, end_time,
                       c.name AS course_name, r.building, r.roomno
                FROM reservation r
                JOIN course c ON r.course_id = c.course_id
                WHERE r.instructor_id = %s
                AND r.reserv_date = %s
                AND r.start_time < %s
                AND r.end_time > %s
            """
            
            params = [instructor_id, reserv_date, end_time, start_time]
            
            if exclude_id:
                sql += " AND r.reservation_id != %s"
                params.append(exclude_id)
            
            cursor.execute(sql, params)
            conflicts = cursor.fetchall()
            
            return conflicts
            
        except Exception as e:
            print(f"❌ Error checking instructor conflict: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_available_rooms(reserv_date, start_time, end_time, min_capacity=None):
        """Find available rooms at specified time"""
        connection = None
        cursor = None
        
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            
            sql = """
                SELECT r.building, r.roomno, r.capacity
                FROM room r
                WHERE NOT EXISTS (
                    SELECT 1 FROM reservation res
                    WHERE res.building = r.building
                    AND res.roomno = r.roomno
                    AND res.reserv_date = %s
                    AND res.start_time < %s
                    AND res.end_time > %s
                )
            """
            
            params = [reserv_date, end_time, start_time]
            
            if min_capacity:
                sql += " AND r.capacity >= %s"
                params.append(min_capacity)
            
            sql += " ORDER BY r.building, r.roomno;"
            
            cursor.execute(sql, params)
            results = cursor.fetchall()
            
            print(f"✅ Found {len(results)} available rooms")
            return results
            
        except Exception as e:
            print(f"❌ Error finding available rooms: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_instructor_schedule(instructor_id, start_date, end_date):
        """Get instructor schedule for a date range"""
        connection = None
        cursor = None
        
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            
            sql = """
                SELECT r.reserv_date, r.start_time, r.end_time,
                       c.name AS course_name, r.activity_type,
                       r.building, r.roomno, r.hours_number
                FROM reservation r
                JOIN course c ON r.course_id = c.course_id
                WHERE r.instructor_id = %s
                AND r.reserv_date >= %s
                AND r.reserv_date <= %s
                ORDER BY r.reserv_date, r.start_time;
            """
            
            cursor.execute(sql, (instructor_id, start_date, end_date))
            return cursor.fetchall()
            
        except Exception as e:
            print(f"❌ Error fetching instructor schedule: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_room_schedule(building, room_no, start_date, end_date):
        """Get room schedule for a date range"""
        connection = None
        cursor = None
        
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            
            sql = """
                SELECT r.reserv_date, r.start_time, r.end_time,
                       c.name AS course_name, r.activity_type,
                       i.last_name || ' ' || i.first_name AS instructor_name,
                       r.hours_number
                FROM reservation r
                JOIN course c ON r.course_id = c.course_id
                JOIN instructor i ON r.instructor_id = i.instructor_id
                WHERE r.building = %s
                AND r.roomno = %s
                AND r.reserv_date >= %s
                AND r.reserv_date <= %s
                ORDER BY r.reserv_date, r.start_time;
            """
            
            cursor.execute(sql, (building, room_no, start_date, end_date))
            return cursor.fetchall()
            
        except Exception as e:
            print(f"❌ Error fetching room schedule: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_instructor_workload(instructor_id):
        """Calculate total hours for an instructor"""
        connection = None
        cursor = None
        
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            
            sql = """
                SELECT 
                    COUNT(*) AS total_reservations,
                    SUM(hours_number) AS total_hours,
                    COUNT(DISTINCT course_id) AS courses_count
                FROM reservation
                WHERE instructor_id = %s;
            """
            
            cursor.execute(sql, (instructor_id,))
            return cursor.fetchone()
            
        except Exception as e:
            print(f"❌ Error calculating workload: {e}")
            return None
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_all_courses():
        """Get all courses for dropdown"""
        connection = None
        cursor = None
        
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            
            sql = "SELECT course_id, name, department_id FROM course ORDER BY name;"
            cursor.execute(sql)
            return cursor.fetchall()
            
        except Exception as e:
            print(f"❌ Error fetching courses: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_all_instructors():
        """Get all instructors for dropdown"""
        connection = None
        cursor = None
        
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            
            sql = """
                SELECT instructor_id, last_name || ' ' || first_name AS name
                FROM instructor
                ORDER BY last_name, first_name;
            """
            cursor.execute(sql)
            return cursor.fetchall()
            
        except Exception as e:
            print(f"❌ Error fetching instructors: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_all_rooms():
        """Get all rooms for dropdown"""
        connection = None
        cursor = None
        
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            
            sql = """
                SELECT building, roomno, capacity
                FROM room
                ORDER BY building, roomno;
            """
            cursor.execute(sql)
            return cursor.fetchall()
            
        except Exception as e:
            print(f"❌ Error fetching rooms: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_activities_for_course(course_id, department_id):
        """Get available activity types for a course"""
        connection = None
        cursor = None
        
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            
            sql = """
                SELECT activity_type
                FROM activity
                WHERE course_id = %s AND department_id = %s
                ORDER BY activity_type;
            """
            cursor.execute(sql, (course_id, department_id))
            return cursor.fetchall()
            
        except Exception as e:
            print(f"❌ Error fetching activities: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)
