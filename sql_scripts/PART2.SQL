
CREATE TABLE Activity (
    -- Partial Key (Discriminator)
    Activity_Type VARCHAR(20) NOT NULL
        CHECK (Activity_Type IN ('Lecture', 'Tutorial', 'Practical')),

    -- Foreign Key to Owner Entity (Course)
    Course_ID INTEGER NOT NULL,
    Department_ID INTEGER NOT NULL,

    -- Activity Attributes
    Hours_Per_Week NUMERIC(3,1) NOT NULL CHECK (Hours_Per_Week > 0),

    -- Primary Key: Owner's Key + Discriminator
    CONSTRAINT PK_Activity PRIMARY KEY (Course_ID, Department_ID, Activity_Type),

    -- Foreign Key with CASCADE
    CONSTRAINT FK_Activity_Course FOREIGN KEY (Course_ID, Department_ID)
        REFERENCES Course (Course_ID, Department_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
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

    Student_ID INTEGER NOT NULL,

    Course_ID INTEGER NOT NULL,
    Department_ID INTEGER NOT NULL,
    Exam_ID INTEGER NOT NULL,

    -- 2. ATTRIBUTES
    -- Schedule is now just a mandatory attribute (where/when they sit it)
    Schedule_ID INTEGER NOT NULL,

    -- Participation tracking
    Attended BOOLEAN DEFAULT FALSE,
    Attendance_Time TIME,
    Seat_Number VARCHAR(10),
    Special_Accommodations TEXT,

    -- 3. PRIMARY KEY DEFINITION
    CONSTRAINT PK_Student_Exam PRIMARY KEY (Student_ID, Course_ID, Department_ID, Exam_ID),

    -- 4. FOREIGN KEYS
    CONSTRAINT FK_StudentExam_Student FOREIGN KEY (Student_ID)
        REFERENCES Student (Student_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT,

    CONSTRAINT FK_StudentExam_Exam FOREIGN KEY (Course_ID, Department_ID, Exam_ID)
        REFERENCES Exam (Course_ID, Department_ID, Exam_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT,

    CONSTRAINT FK_StudentExam_Schedule FOREIGN KEY (Schedule_ID)
        REFERENCES Exam_Schedule (Schedule_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

COMMENT ON TABLE Student_Exam IS ' (N:M) linking Students and Exams. PK is composite of Student and Exam keys.';

-- the previous Grade and Reservation should be dropped and recreated as follows:

CREATE TABLE Grade (
    -- 1. SIMPLIFIED PRIMARY KEY
    Grade_ID SERIAL PRIMARY KEY,

    -- 2. FOREIGN KEYS (Who and What)
    Student_ID INTEGER NOT NULL,
    Course_ID INTEGER NOT NULL,
    Department_ID INTEGER NOT NULL,

    -- 3. EXAM LINKS (Nullable)
    -- We removed Participation_ID because it no longer exists in the other table.
    -- We just need to know which Exam this grade belongs to.
    Exam_ID INTEGER,

    -- 4. DATA ATTRIBUTES
    Grade_Type VARCHAR(30) NOT NULL,
    Grade_Date DATE NOT NULL DEFAULT CURRENT_DATE,
    Grade_Source VARCHAR(10) NOT NULL DEFAULT 'Other' CHECK (Grade_Source IN ('Exam', 'Other')),
    Grade_Value NUMERIC(5,2) NOT NULL,
    Max_Points NUMERIC(5,2) NOT NULL,
    Comments VARCHAR(500),

    -- 5. CONSTRAINTS
    CONSTRAINT CK_Grade_Value CHECK (Grade_Value >= 0 AND Grade_Value <= Max_Points),
    CONSTRAINT CK_Max_Points CHECK (Max_Points > 0),
    CONSTRAINT CK_Grade_Type CHECK (Grade_Type IN ('Quiz', 'Midterm', 'Final', 'Assignment', 'Project', 'Practical Test', 'Homework', 'Oral Exam', 'Resit')),

    -- Logic: If it is an Exam, we must have the Exam_ID.
    CONSTRAINT CK_Grade_Exam_Required CHECK (
        (Grade_Source = 'Exam' AND Exam_ID IS NOT NULL)
        OR
        (Grade_Source = 'Other' AND Exam_ID IS NULL)
    ),

    -- 6. LOGICAL UNIQUENESS (The "Real" Key)
    -- This prevents a student from having two grades of the same type (e.g., two Final Exams)
    -- for the same course on the same day, even though we are using Grade_ID.
    CONSTRAINT UN_Student_Grade UNIQUE (Student_ID, Course_ID, Department_ID, Grade_Type, Grade_Date),

    -- 7. FOREIGN KEY REFERENCES
    CONSTRAINT FK_Grade_Student FOREIGN KEY (Student_ID)
        REFERENCES Student (Student_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT,

    CONSTRAINT FK_Grade_Course FOREIGN KEY (Course_ID, Department_ID)
        REFERENCES Course (Course_ID, Department_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT,

    CONSTRAINT FK_Grade_Exam FOREIGN KEY (Course_ID, Department_ID, Exam_ID)
        REFERENCES Exam (Course_ID, Department_ID, Exam_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

COMMENT ON TABLE Grade IS 'Stores student marks. Uses Grade_ID for simplicity but enforces uniqueness via constraint.';

CREATE TABLE Reservation (
    -- Primary Key
    Reservation_ID SERIAL PRIMARY KEY,

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
    CONSTRAINT CK_Reservation_Hours_Sync CHECK (Hours_Number = EXTRACT(EPOCH FROM (End_Time - Start_Time)) / 3600),

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
