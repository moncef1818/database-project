-- ============================================================================
-- PostgreSQL Complete Labs Script (Labs 1-4)
-- ============================================================================
-- Institution: National School of Cybersecurity, Algiers, Algeria
-- Department: Foundation Training - Second Year
-- Module: Introduction to Databases
-- Instructor: Dr. NAIT-HAMOUD
-- Academic Year: 2025/2026
--
-- Description: This file contains all SQL code for Labs 1 through 4,
--              including DDL, DML, Views, Functions, Transactions, and Triggers.
-- ============================================================================

-- ============================================================================
-- LAB 1: DATA DEFINITION LANGUAGE (DDL)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- SECTION 1.1: Database Creation
-- ----------------------------------------------------------------------------

-- Create the University database
-- Note: This command must be run outside a transaction block
-- You may need to run this separately in psql
-- CREATE DATABASE University;

-- Connect to the database (psql command)
-- \c University

-- ----------------------------------------------------------------------------
-- SECTION 1.2: Table Creation
-- ----------------------------------------------------------------------------

-- Table 1: Department
-- Purpose: Stores information about academic departments
CREATE TABLE Department (
    Department_id integer,
    name varchar(25) NOT NULL,

    -- Constraints
    CONSTRAINT UN_Department_Name UNIQUE (name),
    CONSTRAINT PK_Department PRIMARY KEY (Department_id)
);

-- Table 2: Student
-- Purpose: Stores student information including contact details
CREATE TABLE Student (
    Student_ID integer,
    Last_Name varchar(25) NOT NULL,
    First_Name varchar(25) NOT NULL,
    DOB date NOT NULL,
    Address varchar(50) DEFAULT NULL,
    City varchar(25) DEFAULT NULL,
    Zip_Code varchar(9) DEFAULT NULL,
    Phone varchar(10) DEFAULT NULL,
    Fax varchar(10) DEFAULT NULL,
    Email varchar(100) DEFAULT NULL,

    -- Constraints
    CONSTRAINT PK_Student PRIMARY KEY (Student_ID)
);

-- Table 3: Course
-- Purpose: Stores course information linked to departments
CREATE TABLE Course (
    Course_ID int4 NOT NULL,
    Department_ID int4 NOT NULL,
    name varchar(60) NOT NULL,
    Description varchar(1000),

    -- Constraints
    CONSTRAINT PK_Course PRIMARY KEY (Course_ID, Department_ID),
    CONSTRAINT FK_Course_Department FOREIGN KEY (Department_ID)
        REFERENCES Department (Department_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT
);

-- Table 4: Instructor
-- Purpose: Stores faculty member information
CREATE TABLE Instructor (
    Instructor_ID integer,
    Department_ID integer NOT NULL,
    Last_Name varchar(25) NOT NULL,
    First_Name varchar(25) NOT NULL,
    Rank varchar(25),
    Phone varchar(10) DEFAULT NULL,
    Fax varchar(10) DEFAULT NULL,
    Email varchar(100) DEFAULT NULL,

    -- Constraints
    CONSTRAINT CK_Instructor_Rank CHECK (Rank IN ('Substitute','MCB', 'MCA', 'PROF')),
    CONSTRAINT PK_Instructor PRIMARY KEY (Instructor_ID),
    CONSTRAINT FK_Instructor_Department_ID FOREIGN KEY (Department_ID)
        REFERENCES Department (Department_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT
);

-- Table 5: Room
-- Purpose: Stores classroom and facility information
CREATE TABLE Room (
    Building varchar(1),
    RoomNo varchar(20),
    Capacity integer CHECK (Capacity >= 1),

    -- Constraints
    CONSTRAINT PK_Room PRIMARY KEY (Building, RoomNo)
);

-- Table 6: Reservation
-- Purpose: Stores room booking information for courses
CREATE TABLE Reservation (
    Reservation_ID integer,
    Building varchar(1) NOT NULL,
    RoomNo varchar(10) NOT NULL,
    Course_ID integer NOT NULL,
    Department_ID integer NOT NULL,
    Instructor_ID integer NOT NULL,
    Reserv_Date date NOT NULL DEFAULT CURRENT_DATE,
    Start_Time time NOT NULL DEFAULT CURRENT_TIME,
    End_Time time NOT NULL DEFAULT '23:00:00',
    Hours_Number integer NOT NULL,

    -- Constraints
    CONSTRAINT PK_Reservation PRIMARY KEY (Reservation_ID),
    CONSTRAINT FK_Reservation_Room FOREIGN KEY (Building, RoomNo)
        REFERENCES Room (Building, RoomNo)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    CONSTRAINT FK_Reservation_Course FOREIGN KEY (Course_ID, Department_ID)
        REFERENCES Course (Course_ID, Department_ID)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    CONSTRAINT FK_Reservation_Instructor FOREIGN KEY (Instructor_ID)
        REFERENCES Instructor (Instructor_ID)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    CONSTRAINT CK_Reservation_Hours_Number CHECK (Hours_Number >= 1),
    CONSTRAINT CK_Reservation_StartEndTime CHECK (Start_Time < End_Time)
);

-- ----------------------------------------------------------------------------
-- SECTION 1.3: Schema Extension - Required Work
-- ----------------------------------------------------------------------------

-- Table 7: Enrollment
-- Purpose: Manages student enrollments in courses with dates
CREATE TABLE Enrollment (
    Enrollment_ID SERIAL PRIMARY KEY,
    Student_ID integer NOT NULL,
    Course_ID integer NOT NULL,
    Department_ID integer NOT NULL,
    Enrollment_Date date NOT NULL DEFAULT CURRENT_DATE,
    Status varchar(20) DEFAULT 'Active',

    -- Constraints
    CONSTRAINT FK_Enrollment_Student FOREIGN KEY (Student_ID)
        REFERENCES Student (Student_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT FK_Enrollment_Course FOREIGN KEY (Course_ID, Department_ID)
        REFERENCES Course (Course_ID, Department_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT UN_Enrollment UNIQUE (Student_ID, Course_ID, Department_ID),
    CONSTRAINT CK_Enrollment_Status CHECK (Status IN ('Active', 'Completed', 'Dropped'))
);

-- Table 8: Grade
-- Purpose: Manages student grades (multiple grades per course allowed)
CREATE TABLE Grade (
    Grade_ID SERIAL PRIMARY KEY,
    Student_ID integer NOT NULL,
    Course_ID integer NOT NULL,
    Department_ID integer NOT NULL,
    Grade_Type varchar(30) NOT NULL,
    Grade_Value numeric(5,2) NOT NULL,
    Max_Points numeric(5,2) NOT NULL,
    Grade_Date date NOT NULL DEFAULT CURRENT_DATE,
    Comments varchar(500),

    -- Constraints
    CONSTRAINT FK_Grade_Student FOREIGN KEY (Student_ID)
        REFERENCES Student (Student_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT FK_Grade_Course FOREIGN KEY (Course_ID, Department_ID)
        REFERENCES Course (Course_ID, Department_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT CK_Grade_Value CHECK (Grade_Value >= 0 AND Grade_Value <= Max_Points),
    CONSTRAINT CK_Max_Points CHECK (Max_Points > 0),
    CONSTRAINT CK_Grade_Type CHECK (Grade_Type IN ('Quiz', 'Midterm', 'Final', 'Assignment', 'Project', 'Practical'))
);

-- ----------------------------------------------------------------------------
-- SECTION 1.4: Data Insertion
-- ----------------------------------------------------------------------------

-- Insert Departments
INSERT INTO Department VALUES ('1','SADS');
INSERT INTO Department VALUES ('2','CCS');
INSERT INTO Department VALUES ('3','GRC');
INSERT INTO Department VALUES ('4','INS');

-- Insert Students
INSERT INTO Student VALUES
('1','Ali', 'Ben Ali','1979/02/18','50, 1st street','Algiers','16000','0143567890',NULL,'A1@yahoo.fr');
INSERT INTO Student VALUES
('2','Amar', 'Ben Ammar','1980/08/23','10, Avenue b','BATNA','05000','0678567801',NULL,'pt@yahoo.fr');
INSERT INTO Student VALUES
('3','Ameur', 'Ben Ameur','1978/05/12','25, 2nd street','Oran','31000','0145678956','0145678956','o@yahoo.fr');
INSERT INTO Student VALUES
('4','Aissa', 'Ben Aissa','1979/07/15','56, Road','Annaba','23000','0678905645',NULL,'d@hotmail.com');
INSERT INTO Student VALUES
('5','Fatima', 'Ben Abdedallah','1979/08/15','45, Faubourg','Constantine','25000',NULL,NULL,NULL);

-- Insert Instructors
-- Note: Fixed typo in last instructor - 'Substitute' not 'Substitue'
INSERT INTO Instructor VALUES('1','1','Abbas','BenAbbes','MCA','4185','4091','Ab@yahoo.fr');
INSERT INTO Instructor VALUES('2','1','Mokhtar','BenMokhtar','Substitute', NULL, NULL, NULL);
INSERT INTO Instructor VALUES('3','1','Djemaa','Ben Mohamed','MCB', NULL, NULL, NULL);
INSERT INTO Instructor VALUES('4','1','Lahlou','Mohamed','PROF', NULL, NULL, NULL);
INSERT INTO Instructor VALUES('5','1','Abla','Chad','MCA',NULL,NULL,'ab@lgmail.com');
INSERT INTO Instructor VALUES('6','4','Mariam','BALI','Substitute',NULL,NULL,NULL);

-- Insert Rooms
INSERT INTO Room VALUES('B','020','15');
INSERT INTO Room VALUES('B','022','15');
INSERT INTO Room VALUES('A','301','45');
INSERT INTO Room VALUES('C','Lecture Hall 1','500');
INSERT INTO Room VALUES('C','Lecture Hall 2','200');

-- Insert Courses
INSERT INTO Course VALUES
('1','1','Databases','Licence(L3) : Modeling E/A and UML, Relational Model, Relational Algebra, Relational calculs,SQL, NFs and FDs');
INSERT INTO Course VALUES ('2','1','C++ progr.','Level Master 1');
INSERT INTO Course VALUES
('3','1','Advanced DBs','Level Master 2 -Program Licence and Master 1');
INSERT INTO Course VALUES ('4','4','English','');

-- Insert Reservations
INSERT INTO Reservation VALUES ('1','B','022','1','1','1','2006/10/15','08:30:00','11:45:00','3');
INSERT INTO Reservation VALUES ('2','B','022','1','1','4','2006/11/04','08:30:00','11:45:00','3');
INSERT INTO Reservation VALUES ('3','B','022','1','1','4','2006/11/07','08:30:00','11:45:00','3');
INSERT INTO Reservation VALUES ('4','B','020','1','1','5','2006/10/20','13:45:00','17:00:00','3');
INSERT INTO Reservation VALUES ('5','B','020','1','1','4','2006/12/09','13:45:00','17:00:00','3');
INSERT INTO Reservation VALUES ('6','A','301','2','1','1','2006/09/02','08:30:00','11:45:00','3');
INSERT INTO Reservation VALUES ('7','A','301','2','1','1','2006/09/03','08:30:00','11:45:00','3');
INSERT INTO Reservation VALUES ('8','A','301','2','1','1','2006/09/10','08:30:00','11:45:00','3');
INSERT INTO Reservation VALUES ('9','A','301','3','1','1','2006/09/24','13:45:00','17:00:00','3');
INSERT INTO Reservation VALUES ('10','B','022','3','1','1','2006/10/15','13:45:00','17:00:00','3');
INSERT INTO Reservation VALUES ('11','A','301','3','1','1','2006/10/01','13:45:00','17:00:00','3');
INSERT INTO Reservation VALUES ('12','A','301','3','1','1','2006/10/08','13:45:00','17:00:00','3');
INSERT INTO Reservation VALUES ('13','B','022','1','1','4','2006/11/03','13:45:00','17:00:00','3');
INSERT INTO Reservation VALUES ('14','B','022','1','1','5','2006/10/20','13:45:00','17:00:00','3');
INSERT INTO Reservation VALUES ('15','B','022','1','1','4','2006/12/09','13:45:00','17:00:00','3');
INSERT INTO Reservation VALUES ('16','B','022','1','1','4','2006/09/03','08:30:00','11:45:00','3');
INSERT INTO Reservation VALUES ('17','B','022','1','1','5','2006/09/10','08:30:00','11:45:00','3');
INSERT INTO Reservation VALUES ('18','B','022','1','1','4','2006/09/24','13:45:00','17:00:00','3');
INSERT INTO Reservation VALUES ('19','B','022','1','1','5','2006/10/01','13:45:00','17:00:00','3');
INSERT INTO Reservation VALUES ('20','B','022','1','1','1','2006/10/08','13:45:00','17:00:00','3');
INSERT INTO Reservation VALUES ('21','B','022','1','1','4','2003/09/02','08:30:00','11:45:00','3');

-- Insert Sample Enrollments
INSERT INTO Enrollment (Student_ID, Course_ID, Department_ID, Enrollment_Date, Status)
VALUES
(1, 1, 1, '2006-09-01', 'Active'),
(2, 1, 1, '2006-09-01', 'Active'),
(3, 2, 1, '2006-09-01', 'Active'),
(4, 1, 1, '2006-09-01', 'Active'),
(5, 3, 1, '2006-09-01', 'Active');

-- Insert Sample Grades
INSERT INTO Grade (Student_ID, Course_ID, Department_ID, Grade_Type, Grade_Value, Max_Points, Grade_Date, Comments)
VALUES
(1, 1, 1, 'Quiz', 18, 20, '2006-10-20', 'Excellent understanding'),
(1, 1, 1, 'Midterm', 45, 50, '2006-11-15', 'Very good performance'),
(2, 1, 1, 'Quiz', 15, 20, '2006-10-20', 'Good effort'),
(3, 2, 1, 'Assignment', 28, 30, '2006-10-10', 'Well done');

-- ----------------------------------------------------------------------------
-- SECTION 1.5: Views - Required Work
-- ----------------------------------------------------------------------------

-- Regular View: Instructor Reservations
-- Purpose: Real-time view of instructor workload statistics
CREATE VIEW instructor_reservations AS
SELECT
    i.Instructor_ID,
    i.First_Name || ' ' || i.Last_Name AS Instructor_Name,
    i.Rank,
    d.name AS Department_Name,
    COUNT(r.Reservation_ID) AS Total_Reservations,
    SUM(r.Hours_Number) AS Total_Hours_Taught,
    MIN(r.Reserv_Date) AS First_Reservation,
    MAX(r.Reserv_Date) AS Last_Reservation
FROM Instructor i
JOIN Department d ON i.Department_ID = d.Department_id
LEFT JOIN Reservation r ON i.Instructor_ID = r.Instructor_ID
GROUP BY i.Instructor_ID, i.First_Name, i.Last_Name, i.Rank, d.name
ORDER BY Total_Reservations DESC;

-- Materialized View: Instructor Reservations Summary
-- Purpose: Pre-computed statistics for faster access (requires periodic refresh)
CREATE MATERIALIZED VIEW instructor_reservations_summary AS
SELECT
    i.Instructor_ID,
    i.First_Name || ' ' || i.Last_Name AS Instructor_Name,
    i.Rank,
    d.name AS Department_Name,
    COUNT(r.Reservation_ID) AS Total_Reservations,
    SUM(r.Hours_Number) AS Total_Hours_Taught,
    ROUND(AVG(r.Hours_Number), 2) AS Avg_Hours_Per_Session,
    COUNT(DISTINCT r.Course_ID) AS Courses_Taught
FROM Instructor i
JOIN Department d ON i.Department_ID = d.Department_id
LEFT JOIN Reservation r ON i.Instructor_ID = r.Instructor_ID
GROUP BY i.Instructor_ID, i.First_Name, i.Last_Name, i.Rank, d.name
ORDER BY Total_Reservations DESC;


-- To refresh the materialized view (run periodically):
-- REFRESH MATERIALIZED VIEW instructor_reservations_summary;;


-- ============================================================================
-- LAB 2: DATA MANIPULATION LANGUAGE (DML) - Sample Queries
-- ============================================================================

-- ----------------------------------------------------------------------------
-- SECTION 2.1: Basic SELECT Queries
-- ----------------------------------------------------------------------------

-- Query 1: List all student names
SELECT Last_Name, First_Name
FROM Student;

-- Query 2: Students from a specific city
SELECT Last_Name, First_Name, City
FROM Student
WHERE City = 'Algiers';

-- Query 3: Students whose last name starts with 'A'
SELECT Last_Name, First_Name
FROM Student
WHERE Last_Name LIKE 'A%';

-- Query 4: Instructors with 'E' as second-to-last letter
SELECT Last_Name, First_Name
FROM Instructor
WHERE Last_Name LIKE '%E_';

-- Query 5: Instructors sorted by department, last name, first name
SELECT
    d.name AS Department_Name,
    i.Last_Name,
    i.First_Name,
    i.Rank
FROM Instructor i
JOIN Department d ON i.Department_ID = d.Department_id
ORDER BY d.name, i.Last_Name, i.First_Name;

-- Query 6: Count instructors with 'Substitute' rank
SELECT COUNT(*) AS Substitute_Count
FROM Instructor
WHERE Rank = 'Substitute';

-- Query 7: Students without fax numbers
SELECT Last_Name, First_Name, Phone, Fax
FROM Student
WHERE Fax IS NULL;

-- Query 8: Courses with 'Licence' in description
SELECT Course_ID, name AS Course_Title, Description
FROM Course
WHERE Description LIKE '%Licence%';

-- ----------------------------------------------------------------------------
-- SECTION 2.2: Aggregation and Calculations
-- ----------------------------------------------------------------------------

-- Query 9: Course costs (1 hour = 3000 DA)
SELECT
    c.Course_ID,
    c.name AS Course_Name,
    SUM(r.Hours_Number) AS Total_Hours,
    SUM(r.Hours_Number) * 3000 AS Total_Cost_DA
FROM Course c
LEFT JOIN Reservation r ON c.Course_ID = r.Course_ID
GROUP BY c.Course_ID, c.name
ORDER BY Total_Cost_DA DESC;

-- Query 10: Courses costing between 25000 and 40000 DA
SELECT
    Course_Name,
    Total_Cost_DA
FROM (
    SELECT
        c.name AS Course_Name,
        SUM(r.Hours_Number) * 3000 AS Total_Cost_DA
    FROM Course c
    LEFT JOIN Reservation r ON c.Course_ID = r.Course_ID
    GROUP BY c.name
) AS course_costs
WHERE Total_Cost_DA BETWEEN 25000 AND 40000;

-- Query 11: Average and maximum room capacity
SELECT
    AVG(Capacity) AS Average_Capacity,
    MAX(Capacity) AS Maximum_Capacity,
    MIN(Capacity) AS Minimum_Capacity,
    COUNT(*) AS Total_Rooms
FROM Room;

-- Query 12: Rooms with below-average capacity
SELECT
    Building,
    RoomNo,
    Capacity
FROM Room
WHERE Capacity < (SELECT AVG(Capacity) FROM Room)
ORDER BY Capacity;

-- ----------------------------------------------------------------------------
-- SECTION 2.3: Advanced Filtering
-- ----------------------------------------------------------------------------

-- Query 13: Instructors from SADS or CCS (using IN)
SELECT
    i.Last_Name,
    i.First_Name,
    d.name AS Department
FROM Instructor i
JOIN Department d ON i.Department_ID = d.Department_id
WHERE d.name IN ('SADS', 'CCS')
ORDER BY d.name, i.Last_Name;


-- Query 14: Instructors NOT in SADS or CCS
SELECT
    i.Last_Name,
    i.First_Name,
    d.name AS Department
FROM Instructor i
JOIN Department d ON i.Department_ID = d.Department_id
WHERE d.name NOT IN ('SADS', 'CCS')
ORDER BY d.name;

-- Query 15: Students sorted by city
SELECT
    Last_Name,
    First_Name,
    City,
    Zip_Code
FROM Student
ORDER BY City;

-- ----------------------------------------------------------------------------
-- SECTION 2.4: Grouping and Subqueries
-- ----------------------------------------------------------------------------

-- Query 16: Number of courses per department
SELECT
    d.name AS Department_Name,
    COUNT(c.Course_ID) AS Number_Of_Courses
FROM Department d
LEFT JOIN Course c ON d.Department_id = c.Department_ID
GROUP BY d.name
ORDER BY Number_Of_Courses DESC;

-- Query 17: Departments with 3+ courses
SELECT
    d.name AS Department_Name,
    COUNT(c.Course_ID) AS Number_Of_Courses
FROM Department d
LEFT JOIN Course c ON d.Department_id = c.Department_ID
GROUP BY d.name
HAVING COUNT(c.Course_ID) >= 3
ORDER BY Number_Of_Courses DESC;

-- Query 18: Instructors with at least 2 reservations (using view)
SELECT
    Instructor_Name,
    Total_Reservations
FROM instructor_reservations
WHERE Total_Reservations >= 2
ORDER BY Total_Reservations DESC;

-- Query 19: Instructors with most reservations (using ALL)
SELECT
    Instructor_Name,
    Total_Reservations
FROM instructor_reservations
WHERE Total_Reservations >= ALL (
    SELECT Total_Reservations
    FROM instructor_reservations
)
ORDER BY Total_Reservations DESC;

-- Query 20: Instructors without reservations
SELECT
    i.Last_Name,
    i.First_Name,
    d.name AS Department
FROM Instructor i
JOIN Department d ON i.Department_ID = d.Department_id
LEFT JOIN Reservation r ON i.Instructor_ID = r.Instructor_ID
WHERE r.Reservation_ID IS NULL;

-- ----------------------------------------------------------------------------
-- SECTION 2.5: UPDATE Examples
-- ----------------------------------------------------------------------------

-- Update Example 1: Single student's phone
UPDATE Student
SET Phone = '0551234567'
WHERE Student_ID = 1;

-- Update Example 2: Instructor rank promotion
UPDATE Instructor
SET Rank = 'MCA'
WHERE Rank = 'MCB' AND Last_Name = 'Ben Mohamed';

-- Update Example 3: Multiple columns
UPDATE Instructor
SET Phone = '0661122334',
    Email = 'mariam.bali@ens.dz'
WHERE Instructor_ID = 6;

-- Update Example 4: Conditional update with subquery
UPDATE Room
SET Capacity = Capacity + 5
WHERE Capacity < (SELECT AVG(Capacity) FROM Room);

-- Update Example 5: Update with JOIN
UPDATE Course c
SET Description = 'Updated: ' || c.Description
FROM Department d
WHERE c.Department_ID = d.Department_id
AND d.name = 'SADS'
AND c.Description IS NOT NULL
AND c.Description != '';

-- ----------------------------------------------------------------------------
-- SECTION 2.6: Set Operations
-- ----------------------------------------------------------------------------

-- Set Operation Example 1: UNION - All contacts
SELECT
    'Instructor' AS Type,
    First_Name || ' ' || Last_Name AS Full_Name,
    Email
FROM Instructor
WHERE Email IS NOT NULL

UNION

SELECT
    'Student' AS Type,
    First_Name || ' ' || Last_Name AS Full_Name,
    Email
FROM Student
WHERE Email IS NOT NULL

ORDER BY Type, Full_Name;

-- Set Operation Example 2: INTERSECT - Students with both enrollment and grades
SELECT Student_ID, Course_ID
FROM Enrollment

INTERSECT

SELECT Student_ID, Course_ID
FROM Grade

ORDER BY Student_ID, Course_ID;

-- Set Operation Example 3: EXCEPT - Enrolled students without grades
SELECT
    e.Student_ID,
    s.First_Name || ' ' || s.Last_Name AS Student_Name,
    c.name AS Course_Name
FROM Enrollment e
JOIN Student s ON e.Student_ID = s.Student_ID
JOIN Course c ON e.Course_ID = c.Course_ID

EXCEPT

SELECT
    g.Student_ID,
    s.First_Name || ' ' || s.Last_Name AS Student_Name,
    c.name AS Course_Name
FROM Grade g
JOIN Student s ON g.Student_ID = s.Student_ID
JOIN Course c ON g.Course_ID = c.Course_ID

ORDER BY Student_Name;


-- ============================================================================
-- LAB 3: USER-DEFINED FUNCTIONS AND TRANSACTIONS
-- ============================================================================

-- ----------------------------------------------------------------------------
-- SECTION 3.1: SQL User-Defined Functions
-- ----------------------------------------------------------------------------

-- Function 1: Get rooms with capacity greater than given value
-- Purpose: Returns all rooms exceeding a minimum capacity threshold
-- Returns: TABLE with building, room number, and capacity
CREATE OR REPLACE FUNCTION get_rooms_by_capacity(min_capacity integer)
RETURNS TABLE(
    building_name varchar(1),
    room_number varchar(10),
    room_capacity integer
) AS $$
    SELECT
        Building,
        RoomNo,
        Capacity
    FROM Room
    WHERE Capacity > $1  -- $1 refers to min_capacity parameter
    ORDER BY Capacity DESC;
$$ LANGUAGE SQL;

-- Usage Example:
-- SELECT * FROM get_rooms_by_capacity(100);


-- Function 2: Get department ID by name
-- Purpose: Lookup function to retrieve department ID given its name
-- Returns: Integer (department ID) or NULL if not found
CREATE OR REPLACE FUNCTION get_department_id(dept_name varchar(25))
RETURNS integer AS $$
    SELECT Department_id
    FROM Department
    WHERE name = $1;  -- $1 refers to dept_name parameter
$$ LANGUAGE SQL;

-- Usage Example:
-- SELECT get_department_id('SADS');
-- SELECT * FROM Instructor WHERE Department_ID = get_department_id('SADS');


-- Function 3: Check reservation conflicts
-- Purpose: Validates if a room reservation conflicts with existing bookings
-- Returns: TABLE with conflicting reservation IDs (empty if no conflicts)
-- Logic: Checks for time overlaps on same room and date
CREATE OR REPLACE FUNCTION check_reservation(
    p_building text,
    p_roomno text,
    p_date date,
    p_start_time time,
    p_end_time time
)
RETURNS TABLE(conflicting_reservation_id integer) AS $$
    SELECT Reservation_ID
    FROM Reservation
    WHERE Building = $1
      AND RoomNo = $2
      AND Reserv_Date = $3
      AND (
          -- Scenario 1: New reservation starts during existing one
          ($4 >= Start_Time AND $4 < End_Time)
          OR
          -- Scenario 2: New reservation ends during existing one
          ($5 > Start_Time AND $5 <= End_Time)
          OR
          -- Scenario 3: New reservation encompasses existing one
          ($4 <= Start_Time AND $5 >= End_Time)
      );
$$ LANGUAGE SQL;

-- Usage Examples:
-- Check for conflicts (should return empty for new date)
-- SELECT * FROM check_reservation('B', '022', '2026-12-20', '09:00:00', '12:00:00');

-- Check for conflicts (should return ID 1 for existing reservation)
-- SELECT * FROM check_reservation('B', '022', '2006-10-15', '09:00:00', '12:00:00');


-- ----------------------------------------------------------------------------
-- SECTION 3.2: Transactions - Required Work
-- ----------------------------------------------------------------------------

-- Transaction Example 1: Simple Enrollment Registration
-- Purpose: Enroll a student in a course with initial grade record
-- Ensures both records are created atomically
/*
BEGIN;

    -- Insert enrollment record
    INSERT INTO Enrollment (Student_ID, Course_ID, Department_ID, Enrollment_Date, Status)
    VALUES (1, 2, 1, '2006-09-15', 'Active');

    -- Create initial grade placeholder
    INSERT INTO Grade (Student_ID, Course_ID, Department_ID, Grade_Type, Grade_Value, Max_Points, Grade_Date, Comments)
    VALUES (1, 2, 1, 'Initial', 0, 0, '2006-09-15', 'Enrollment placeholder');

COMMIT;
*/

-- Transaction Example 2: Room Capacity Update with Audit
-- Purpose: Update room capacity and log the change
-- Note: Requires Room_Capacity_History table (created below)

-- Create audit table for room capacity changes
CREATE TABLE IF NOT EXISTS Room_Capacity_History (
    History_ID SERIAL PRIMARY KEY,
    Building varchar(1),
    RoomNo varchar(10),
    Old_Capacity integer,
    New_Capacity integer,
    Change_Date date DEFAULT CURRENT_DATE,
    Changed_By varchar(50) DEFAULT CURRENT_USER
);

/*
BEGIN;

    -- Store old capacity for audit
    INSERT INTO Room_Capacity_History (Building, RoomNo, Old_Capacity, New_Capacity)
    SELECT
        Building,
        RoomNo,
        Capacity,
        25  -- New capacity
    FROM Room
    WHERE Building = 'B' AND RoomNo = '020';

    -- Update room capacity
    UPDATE Room
    SET Capacity = 25
    WHERE Building = 'B' AND RoomNo = '020';

COMMIT;
*/


-- Transaction Example 3: Batch Grade Entry with Savepoints
-- Purpose: Insert multiple grades, rolling back only invalid ones
/*
BEGIN;

    -- Grade 1: Valid
    SAVEPOINT grade1;
    INSERT INTO Grade (Student_ID, Course_ID, Department_ID, Grade_Type, Grade_Value, Max_Points, Grade_Date)
    VALUES (1, 1, 1, 'Quiz', 18, 20, '2006-10-20');

    -- Grade 2: Valid
    SAVEPOINT grade2;
    INSERT INTO Grade (Student_ID, Course_ID, Department_ID, Grade_Type, Grade_Value, Max_Points, Grade_Date)
    VALUES (2, 1, 1, 'Quiz', 15, 20, '2006-10-20');

    -- Grade 3: Invalid (would violate CHECK constraint if attempted)
    -- SAVEPOINT grade3;
    -- This would fail: INSERT INTO Grade VALUES (..., 25, 20, ...); -- grade > max
    -- ROLLBACK TO SAVEPOINT grade3;

    -- Grade 4: Valid
    SAVEPOINT grade4;
    INSERT INTO Grade (Student_ID, Course_ID, Department_ID, Grade_Type, Grade_Value, Max_Points, Grade_Date)
    VALUES (4, 1, 1, 'Quiz', 16, 20, '2006-10-20');

COMMIT;
*/




-- ============================================================================
-- LAB 4: TRIGGERS
-- ============================================================================

-- ----------------------------------------------------------------------------
-- SECTION 4.1: Audit Trigger Setup - Required Work
-- ----------------------------------------------------------------------------

-- Step 1: Create Audit Log Table
-- Purpose: Stores audit records for Student table operations
CREATE TABLE Student_Audit_Log (
    LogID SERIAL PRIMARY KEY,
    OperationType VARCHAR(50) NOT NULL,
    OperationTime TIMESTAMP NOT NULL,
    Description TEXT
);


-- Step 2: Create Trigger Function
-- Purpose: Logs statement-level DML operations on Student table
-- Type: Statement-level (fires once per SQL statement)
-- Returns: NULL (required for statement-level triggers)
CREATE OR REPLACE FUNCTION audit_student_changes_statement()
RETURNS TRIGGER AS $$
BEGIN
    -- Insert audit log entry
    INSERT INTO Student_Audit_Log (
        OperationType,
        OperationTime,
        Description
    )
    VALUES (
        TG_OP,  -- Special variable: 'INSERT', 'UPDATE', or 'DELETE'
        CURRENT_TIMESTAMP,  -- Current timestamp
        'A statement-level DML operation occurred on Students table.'
    );

    -- Statement-level triggers must return NULL
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;


-- Step 3: Create the Trigger
-- Purpose: Attaches audit function to Student table
-- Timing: AFTER (only logs successful operations)
-- Scope: FOR EACH STATEMENT (fires once per SQL command)
CREATE TRIGGER trg_audit_students_statement
AFTER INSERT OR UPDATE OR DELETE ON Student
FOR EACH STATEMENT
EXECUTE FUNCTION audit_student_changes_statement();


-- Testing the Audit Trigger:
-- Uncomment to test after creating the trigger

-- Test 1: Single INSERT
-- INSERT INTO Student VALUES (6, 'Hassan', 'Benali', '2001-03-15', '12 Rue', 'Algiers', '16000', NULL, NULL, 'hassan@email.dz');
-- SELECT * FROM Student_Audit_Log ORDER BY LogID DESC LIMIT 1;

-- Test 2: Bulk INSERT
-- INSERT INTO Student VALUES
--     (7, 'Amina', 'Kadri', '2002-05-20', '45 Blvd', 'Oran', '31000', NULL, NULL, 'amina@email.dz'),
--     (8, 'Karim', 'Mansouri', '2001-11-08', '78 Ave', 'Constantine', '25000', NULL, NULL, 'karim@email.dz');
-- SELECT * FROM Student_Audit_Log ORDER BY LogID DESC LIMIT 1;

-- Test 3: UPDATE
-- UPDATE Student SET City = 'Algiers' WHERE Student_ID IN (2, 3, 4);
-- SELECT * FROM Student_Audit_Log ORDER BY LogID DESC LIMIT 1;

-- Test 4: DELETE
-- DELETE FROM Student WHERE Student_ID = 6;
-- SELECT * FROM Student_Audit_Log ORDER BY LogID DESC LIMIT 1;



-- ============================================================================
-- DATA VERIFICATION QUERIES
-- ============================================================================
/*
-- Count records in each main table
SELECT 'Department' AS table_name, COUNT(*) AS record_count FROM Department
UNION ALL
SELECT 'Student', COUNT(*) FROM Student
UNION ALL
SELECT 'Instructor', COUNT(*) FROM Instructor
UNION ALL
SELECT 'Course', COUNT(*) FROM Course
UNION ALL
SELECT 'Room', COUNT(*) FROM Room
UNION ALL
SELECT 'Reservation', COUNT(*) FROM Reservation
UNION ALL
SELECT 'Enrollment', COUNT(*) FROM Enrollment
UNION ALL
SELECT 'Grade', COUNT(*) FROM Grade
ORDER BY table_name;
/*

-- ============================================================================
-- CLEANUP QUERIES (USE WITH CAUTION)
-- ============================================================================
-- Uncomment these only if you need to start fresh

/*
-- Drop all triggers
DROP TRIGGER IF EXISTS trg_audit_students_statement ON Student;
DROP TRIGGER IF EXISTS track_student_updates ON Student;


-- Drop all functions
DROP FUNCTION IF EXISTS audit_student_changes_statement() CASCADE;
DROP FUNCTION IF EXISTS track_student_changes() CASCADE;
DROP FUNCTION IF EXISTS get_rooms_by_capacity(integer) CASCADE;
DROP FUNCTION IF EXISTS get_department_id(varchar) CASCADE;
DROP FUNCTION IF EXISTS check_reservation(text, text, date, time, time) CASCADE;

-- Drop all views
DROP VIEW IF EXISTS instructor_reservations CASCADE;
DROP MATERIALIZED VIEW IF EXISTS instructor_reservations_summary CASCADE;


-- Drop all tables (in correct order due to foreign keys)
DROP TABLE IF EXISTS Student_Change_History CASCADE;
DROP TABLE IF EXISTS Student_Audit_Log CASCADE;
DROP TABLE IF EXISTS Enrollment_Audit_Log CASCADE;
DROP TABLE IF EXISTS Room_Capacity_History CASCADE;
DROP TABLE IF EXISTS Grade CASCADE;
DROP TABLE IF EXISTS Enrollment CASCADE;
DROP TABLE IF EXISTS Reservation CASCADE;
DROP TABLE IF EXISTS Course CASCADE;
DROP TABLE IF EXISTS Room CASCADE;
DROP TABLE IF EXISTS Instructor CASCADE;
DROP TABLE IF EXISTS Student CASCADE;
DROP TABLE IF EXISTS Department CASCADE;
*/


-- ============================================================================
-- END OF SCRIPT
-- ============================================================================
-- All labs completed successfully!
-- ============================================================================
