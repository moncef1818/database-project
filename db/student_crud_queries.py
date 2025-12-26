from db.connection import get_connection, get_cursor, close_connection, close_cursor


class StudentCRUD:
    
    @staticmethod
    def create_student(last_name, first_name, dob, address, city, zip_code, phone, fax, email):
        """INSERT a new student"""
        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = """
                INSERT INTO student (last_name, first_name, dob, address, city, zip_code, phone, fax, email)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING student_id;
            """

            cursor.execute(sql, (last_name, first_name, dob, address, city, zip_code, phone, fax, email))
            new_id = cursor.fetchone()[0]

            connection.commit()
            print(f"✅ Student created with ID: {new_id}")
            return new_id
            
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error creating student: {e}")
            return None
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_all_students(search_field=None, search_value=None, sort_by='student_id', sort_order='ASC'):
        """
        SELECT all students with optional search and sort
        Returns: List of tuples with all student fields
        """
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = """
                SELECT student_id, last_name, first_name, dob, address, 
                       city, zip_code, phone, fax, email 
                FROM student
            """
            params = []

            # Add search condition
            if search_field and search_value:
                if search_field == 'student_id':
                    sql += " WHERE CAST(student_id AS TEXT) LIKE %s"
                    params.append(f"%{search_value}%")
                elif search_field == 'last_name':
                    sql += " WHERE LOWER(last_name) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")
                elif search_field == 'first_name':
                    sql += " WHERE LOWER(first_name) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")
                elif search_field == 'email':
                    sql += " WHERE LOWER(email) LIKE LOWER(%s)"
                    params.append(f"%{search_value}%")

            # Validate and add sorting
            valid_sort_fields = ['student_id', 'last_name', 'first_name', 'dob', 'email']
            if sort_by not in valid_sort_fields:
                sort_by = 'student_id'
            if sort_order not in ['ASC', 'DESC']:
                sort_order = 'ASC'
        
            sql += f" ORDER BY {sort_by} {sort_order}"

            cursor.execute(sql, params)
            results = cursor.fetchall()

            print(f"✅ Retrieved {len(results)} students")
            return results
        
        except Exception as e:
            print(f"❌ Error fetching students: {e}")
            return []
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def get_student_by_id(student_id):
        """
        SELECT a single student by ID
        Returns: Tuple with all student fields or None
        """
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = """
                SELECT student_id, last_name, first_name, dob, address, 
                       city, zip_code, phone, fax, email
                FROM student
                WHERE student_id = %s
            """
            
            cursor.execute(sql, (student_id,))
            result = cursor.fetchone()

            if result:
                print(f"✅ Retrieved student ID {student_id}")
            else:
                print(f"⚠️ No student found with ID {student_id}")
            
            return result
        
        except Exception as e:
            print(f"❌ Error fetching student: {e}")
            return None
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def update_student(student_id, last_name, first_name, dob, address, city, zip_code, phone, fax, email):
        """UPDATE a student's information"""
        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            sql = """
                UPDATE student 
                SET last_name = %s, 
                    first_name = %s, 
                    dob = %s, 
                    address = %s, 
                    city = %s, 
                    zip_code = %s, 
                    phone = %s, 
                    fax = %s, 
                    email = %s
                WHERE student_id = %s
            """
            
            cursor.execute(sql, (last_name, first_name, dob, address, city, 
                                zip_code, phone, fax, email, student_id))
            rows_affected = cursor.rowcount

            connection.commit()

            if rows_affected > 0:
                print(f"✅ Student ID {student_id} updated successfully")
                return True
            else:
                print(f"⚠️ No student found with ID {student_id}")
                return False
                
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error updating student: {e}")
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)

    @staticmethod
    def delete_student(student_id):
        """DELETE a student"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = get_cursor(connection)
            
            sql = "DELETE FROM student WHERE student_id = %s"
            
            cursor.execute(sql, (student_id,))
            rows_affected = cursor.rowcount
            
            connection.commit()
            
            if rows_affected > 0:
                print(f"✅ Student {student_id} deleted successfully")
                return True
            else:
                print(f"⚠️ No student found with ID {student_id}")
                return False
                
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error deleting student: {e}")
            
            # Check if it's a foreign key constraint error
            if 'foreign key' in str(e).lower() or 'violates' in str(e).lower():
                print("⚠️ Cannot delete: Student is enrolled in courses or has other records")
            
            return False
        finally:
            close_cursor(cursor)
            close_connection(connection)
