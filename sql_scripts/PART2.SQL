
CREATE TABLE Activity (
    -- Partial Key
    Activity_Type VARCHAR(20) NOT NULL CHECK (Activity_Type IN ('Lecture', 'Tutorial', 'Practical')),

    -- Foreign Key to owner entity (Course) - part of primary key
    Course_ID INTEGER NOT NULL,
    Department_ID INTEGER NOT NULL,

    Hours_Per_Week NUMERIC(3,1) NOT NULL CHECK (Hours_Per_Week > 0),

    -- Constraints
    -- Primary Key: Combination of owner's key + discriminator (weak entity pattern)
    CONSTRAINT PK_Activity PRIMARY KEY (Course_ID, Department_ID, Activity_Type),

    -- Foreign Key: Activity MUST belong to a course (total participation)
    CONSTRAINT FK_Activity_Course FOREIGN KEY (Course_ID, Department_ID)
        REFERENCES Course (Course_ID, Department_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE  -- If course is deleted, its activities are deleted (weak entity)
);

 -- Add comments for documentation
COMMENT ON TABLE Activity IS 'Weak entity: Activities depend on Course. Primary key includes Course keys + Activity_Type discriminator.';
COMMENT ON COLUMN Activity.Activity_Type IS 'Discriminator: Lecture (mandatory), Tutorial (optional), or Practical (optional)';

CREATE TABLE Exam (
    -- Partial Key (Discriminator)
    Exam_ID INTEGER NOT NULL,

    -- Foreign Keys (Parent Entity Keys)
    Course_ID INTEGER NOT NULL,
    Department_ID INTEGER NOT NULL,

    Exam_Type VARCHAR(30) NOT NULL CHECK (Exam_Type IN ('Midterm', 'Final', 'Quiz', 'Practical Test', 'Oral Exam', 'Resit')),
    Exam_Name VARCHAR(100) NOT NULL,
    Duration_Minutes INTEGER NOT NULL CHECK (Duration_Minutes > 0),
    Total_Points NUMERIC(5,2) NOT NULL CHECK (Total_Points > 0),
    Instructions TEXT,

    -- Constraints
    -- PRIMARY KEY: The identifying relationship.

    CONSTRAINT PK_Exam PRIMARY KEY (Course_ID, Department_ID, Exam_ID),

    -- Foreign Key: Defining the identifying relationship
    CONSTRAINT FK_Exam_Course FOREIGN KEY (Course_ID, Department_ID)
        REFERENCES Course (Course_ID, Department_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Documentation
COMMENT ON TABLE Exam IS 'Weak Entity: Exam_ID is the partial key (discriminator) within a specific Course.';


CREATE TABLE Exam_Schedule (
    -- Primary Key
    Schedule_ID SERIAL PRIMARY KEY,


    Exam_ID INTEGER NOT NULL,
    Course_ID INTEGER NOT NULL,
    Department_ID INTEGER NOT NULL,

    -- Room Link
    Building VARCHAR(1) NOT NULL,
    RoomNo VARCHAR(10) NOT NULL,

    -- Personnel
    Invigilator_ID INTEGER,

    -- Scheduling attributes
    Exam_Date DATE NOT NULL,
    Start_Time TIME NOT NULL,
    End_Time TIME NOT NULL,

    -- Additional info
    Status VARCHAR(20) DEFAULT 'Scheduled' CHECK (Status IN ('Scheduled', 'In Progress', 'Completed', 'Cancelled')),

    -- Constraints
    CONSTRAINT CK_ExamSchedule_Time CHECK (Start_Time < End_Time),

    -- FOREIGN KEY
    CONSTRAINT FK_ExamSchedule_Exam FOREIGN KEY (Course_ID, Department_ID, Exam_ID)
        REFERENCES Exam (Course_ID, Department_ID, Exam_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT FK_ExamSchedule_Room FOREIGN KEY (Building, RoomNo)
        REFERENCES Room (Building, RoomNo)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT FK_ExamSchedule_Invigilator FOREIGN KEY (Invigilator_ID)
        REFERENCES Instructor (Instructor_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    -- LOGICAL CONSTRAINT: Prevent the same room being used for two exams at once
    CONSTRAINT UN_Room_Time_Date UNIQUE (Building, RoomNo, Exam_Date, Start_Time)
);

CREATE TABLE Student_Exam (
    -- Primary Key
    Participation_ID SERIAL PRIMARY KEY,

    -- Foreign Keys
    Student_ID INTEGER NOT NULL,

    -- COMPOSITE KEY for the Weak Entity "Exam"
    Exam_ID INTEGER NOT NULL,
    Course_ID INTEGER NOT NULL,
    Department_ID INTEGER NOT NULL,

    -- Link to the specific sitting
    Schedule_ID INTEGER NOT NULL,

    -- Participation tracking
    Attended BOOLEAN DEFAULT FALSE,
    Attendance_Time TIME,
    Seat_Number VARCHAR(10),
    Special_Accommodations TEXT,

    -- Constraints
    CONSTRAINT FK_StudentExam_Student FOREIGN KEY (Student_ID)
        REFERENCES Student (Student_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT,

   -- FOREIGN KEY
    CONSTRAINT FK_StudentExam_Exam FOREIGN KEY (Course_ID, Department_ID, Exam_ID)
        REFERENCES Exam (Course_ID, Department_ID, Exam_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT,

    CONSTRAINT FK_StudentExam_Schedule FOREIGN KEY (Schedule_ID)
        REFERENCES Exam_Schedule (Schedule_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT,

    -- Logical Constraint: A student cannot take the same exam twice
    CONSTRAINT UN_StudentExam UNIQUE (Student_ID, Course_ID, Department_ID, Exam_ID)
);

COMMENT ON TABLE Student_Exam IS 'Tracks student exam registration and attendance. Linked via composite keys to the weak Exam entity.';

-- the previous Grade and Reservation should be dropped and recreated as follows:

CREATE TABLE Grade (
    -- Primary Key
    Student_ID INTEGER NOT NULL,
    Course_ID INTEGER NOT NULL,
    Department_ID INTEGER NOT NULL,
    Grade_Type VARCHAR(30) NOT NULL,
    Grade_Date DATE NOT NULL DEFAULT CURRENT_DATE,


    Grade_Source VARCHAR(10) NOT NULL DEFAULT 'Other'
        CHECK (Grade_Source IN ('Exam', 'Other')),

    -- Foreign Keys for Exam-specific records (Nullable for non-exam work)
    Exam_ID INTEGER,         -- Weak Entity "Exam"
    Participation_ID INTEGER,  -- Links to the specific Student_Exam record

    -- Grade attributes
    Grade_Value NUMERIC(5,2) NOT NULL,
    Max_Points NUMERIC(5,2) NOT NULL,
    Comments VARCHAR(500),

    -- 1. PRIMARY KEY DEFINITION
    CONSTRAINT PK_Grade PRIMARY KEY (Student_ID, Course_ID, Department_ID, Grade_Type, Grade_Date),

    -- 2. DOMAIN CONSTRAINTS
    CONSTRAINT CK_Grade_Value CHECK (Grade_Value >= 0 AND Grade_Value <= Max_Points),
    CONSTRAINT CK_Max_Points CHECK (Max_Points > 0),
    CONSTRAINT CK_Grade_Type CHECK (Grade_Type IN (
        'Quiz', 'Midterm', 'Final', 'Assignment', 'Project', 'Practical', 'Participation', 'Homework'
    )),

    -- 3. CONDITIONAL INTEGRITY (The Exam-Source Logic)
    -- This ensures that if it is an 'Exam', we MUST have the exam IDs.
    -- If it is 'Other', those IDs MUST be NULL to maintain 3NF/BCNF integrity.
    CONSTRAINT CK_Grade_Exam_Required CHECK (
        (Grade_Source = 'Exam' AND Exam_ID IS NOT NULL AND Participation_ID IS NOT NULL)
        OR
        (Grade_Source = 'Other' AND Exam_ID IS NULL AND Participation_ID IS NULL)
    ),

    -- 4. FOREIGN KEY CONSTRAINTS
    CONSTRAINT FK_Grade_Student FOREIGN KEY (Student_ID)
        REFERENCES Student (Student_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    -- Link to the identifying Course (Strong reference to parent)
    CONSTRAINT FK_Grade_Course FOREIGN KEY (Course_ID, Department_ID)
        REFERENCES Course (Course_ID, Department_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT FK_Grade_Exam FOREIGN KEY (Course_ID, Department_ID, Exam_ID)
        REFERENCES Exam (Course_ID, Department_ID, Exam_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT FK_Grade_Participation FOREIGN KEY (Participation_ID)
        REFERENCES Student_Exam (Participation_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- Documentation
COMMENT ON TABLE Grade IS 'Stores all student marks. Uses conditional constraints to link to specific Exams when applicable.';


CREATE TABLE Reservation (
    -- Primary Key
    Reservation_ID INTEGER PRIMARY KEY,

    -- Foreign Keys to the Room
    Building VARCHAR(1) NOT NULL,
    RoomNo VARCHAR(20) NOT NULL,

    -- Foreign Keys to the identifying Course (Weak Entity Hierarchy)
    Course_ID INTEGER NOT NULL,
    Department_ID INTEGER NOT NULL,

    -- Link to the specific Activity (Lecture, Tutorial, or Practical)
    Activity_Type VARCHAR(20) NOT NULL,

    -- Link to the Instructor making the reservation
    Instructor_ID INTEGER NOT NULL,

    -- Reservation details
    Reserv_Date DATE NOT NULL DEFAULT CURRENT_DATE,
    Start_Time TIME NOT NULL DEFAULT CURRENT_TIME,
    End_Time TIME NOT NULL DEFAULT '23:00:00',
    Hours_Number INTEGER NOT NULL,

    -- 1. DOMAIN CONSTRAINTS
    CONSTRAINT CK_Reservation_Hours CHECK (Hours_Number >= 1),
    CONSTRAINT CK_Reservation_Time CHECK (Start_Time < End_Time),
    CONSTRAINT CK_Activity_Type_Limit CHECK (Activity_Type IN ('Lecture', 'Tutorial', 'Practical')),

    -- 2. FOREIGN KEY CONSTRAINTS

    -- Link to Room
    CONSTRAINT FK_Reservation_Room FOREIGN KEY (Building, RoomNo)
        REFERENCES Room (Building, RoomNo)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    -- Since Activity is a weak entity of Course, we must reference all three parts
    CONSTRAINT FK_Reservation_Activity FOREIGN KEY (Course_ID, Department_ID, Activity_Type)
        REFERENCES Activity (Course_ID, Department_ID, Activity_Type)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    -- Link to Instructor
    CONSTRAINT FK_Reservation_Instructor FOREIGN KEY (Instructor_ID)
        REFERENCES Instructor (Instructor_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    -- 3. LOGICAL INTEGRITY: Anti-Collision Constraint
    -- This prevents the same room from being booked twice at the same time/date
    CONSTRAINT UN_Room_Schedule UNIQUE (Building, RoomNo, Reserv_Date, Start_Time)
);

-- Documentation
COMMENT ON TABLE Reservation IS 'Manages room bookings for specific Course Activities (Lectures/Tutorials/Practicals).';
