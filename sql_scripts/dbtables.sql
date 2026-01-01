-- Final University DB Schema
-- Notes: EERD Mapping - Option 2 (Super table + subtype tables with FK).
-

CREATE TABLE Department (
    Department_id SERIAL PRIMARY KEY,
    name VARCHAR(25) NOT NULL,
    CONSTRAINT UN_Department_Name UNIQUE (name)
);

CREATE TABLE Section (
    Section_ID SERIAL PRIMARY KEY,
    Name VARCHAR(50) NOT NULL
);
COMMENT ON TABLE Section IS 'Academic sections for organizing student groups';
COMMENT ON COLUMN Section.Name IS 'Section identifier (e.g., Year 2 Section A)';


CREATE TABLE "Group" (
    Group_ID SERIAL PRIMARY KEY,
    Section_ID INTEGER NOT NULL,
    Group_Name VARCHAR(50) NOT NULL,
    CONSTRAINT FK_Group_Section FOREIGN KEY (Section_ID)
        REFERENCES Section (Section_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT
);
COMMENT ON TABLE "Group" IS 'Student groups organized within sections';
COMMENT ON COLUMN "Group".Group_Name IS 'Group identifier within section';


CREATE TABLE Student (
    Student_ID SERIAL PRIMARY KEY,
    Group_ID INTEGER,
    Last_Name VARCHAR(25) NOT NULL,
    First_Name VARCHAR(25) NOT NULL,
    DOB DATE NOT NULL,
    Address VARCHAR(50) DEFAULT NULL,
    City VARCHAR(25) DEFAULT NULL,
    Zip_Code VARCHAR(9) DEFAULT NULL,
    Phone VARCHAR(10) DEFAULT NULL,
    Fax VARCHAR(10) DEFAULT NULL,
    Email VARCHAR(100) DEFAULT NULL,
    CONSTRAINT FK_Student_Group FOREIGN KEY (Group_ID)
        REFERENCES "Group" (Group_ID)
        ON UPDATE CASCADE ON DELETE SET NULL
);
COMMENT ON TABLE Student IS 'Student personal and contact information';
COMMENT ON COLUMN Student.Group_ID IS 'Optional link to student group for organizational queries';
COMMENT ON COLUMN Student.DOB IS 'Date of birth for age verification and records';




CREATE TABLE Instructor (
    Instructor_ID SERIAL PRIMARY KEY,
    Department_ID INTEGER NOT NULL,
    Last_Name VARCHAR(25) NOT NULL,
    First_Name VARCHAR(25) NOT NULL,
    Rank VARCHAR(25),
    Phone VARCHAR(10) DEFAULT NULL,
    Fax VARCHAR(10) DEFAULT NULL,
    Email VARCHAR(100) DEFAULT NULL,
    CONSTRAINT CK_Instructor_Rank CHECK (Rank IN ('Substitute', 'MCB', 'MCA', 'PROF')),
    CONSTRAINT FK_Instructor_Department_ID FOREIGN KEY (Department_ID)
        REFERENCES Department (Department_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT
);
COMMENT ON TABLE Instructor IS 'Faculty members and their academic ranks';
COMMENT ON COLUMN Instructor.Rank IS 'Academic rank: Substitute, MCB (Assistant), MCA (Associate), PROF (Full Professor)';


CREATE TABLE Room (
    Building VARCHAR(1),
    RoomNo VARCHAR(20),
    Capacity INTEGER CHECK (Capacity >= 1),
    CONSTRAINT PK_Room PRIMARY KEY (Building, RoomNo)
);
COMMENT ON TABLE Room IS 'Physical rooms for activities and exams';
COMMENT ON COLUMN Room.Building IS 'Building identifier (single letter)';
COMMENT ON COLUMN Room.Capacity IS 'Maximum occupancy for scheduling purposes';


CREATE TABLE Semester (
    Semester_ID SERIAL PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Start_Date DATE NOT NULL,
    End_Date DATE NOT NULL,
    CHECK (Start_Date < End_Date)
);
COMMENT ON TABLE Semester IS 'Academic semester/term definitions';
COMMENT ON COLUMN Semester.Name IS 'Semester identifier (e.g., Fall 2025, Spring 2026)';



CREATE TABLE Course (
    Course_ID SERIAL NOT NULL,
    Department_ID INTEGER NOT NULL,
    name VARCHAR(60) NOT NULL,
    Description VARCHAR(1000),
    CONSTRAINT PK_Course PRIMARY KEY (Course_ID, Department_ID),
    CONSTRAINT FK_Course_Department FOREIGN KEY (Department_ID)
        REFERENCES Department (Department_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT
);
COMMENT ON TABLE Course IS 'Academic courses with composite PK (Course_ID, Department_ID)';
COMMENT ON COLUMN Course.Description IS 'Course syllabus and learning objectives';

CREATE TABLE Activity (
    Activity_ID SERIAL PRIMARY KEY,
    Course_ID INTEGER NOT NULL,
    Department_ID INTEGER NOT NULL,
    Activity_Type VARCHAR(20) NOT NULL,
    CONSTRAINT CK_Activity_Type CHECK (Activity_Type IN ('Lecture', 'Tutorial', 'Practical')),
    CONSTRAINT UN_Activity_Type_Per_Course UNIQUE (Course_ID, Department_ID, Activity_Type),
    CONSTRAINT FK_Activity_Course FOREIGN KEY (Course_ID, Department_ID)
        REFERENCES Course (Course_ID, Department_ID)
        ON UPDATE CASCADE ON DELETE CASCADE
);
COMMENT ON TABLE Activity IS 'Supertype for all course activities. Weak entity dependent on Course.';
COMMENT ON COLUMN Activity.Activity_Type IS 'Discriminator: Lecture, Tutorial, or Practical';
COMMENT ON CONSTRAINT UN_Activity_Type_Per_Course ON Activity IS 'Each course can have only one activity of each type';


CREATE TABLE Lecture (
    Activity_ID INTEGER PRIMARY KEY,
    CONSTRAINT FK_Lecture_Activity FOREIGN KEY (Activity_ID)
        REFERENCES Activity (Activity_ID)
        ON UPDATE CASCADE ON DELETE CASCADE
);
COMMENT ON TABLE Lecture IS 'Lecture specialization - mandatory per course (enforced by trigger)';

CREATE TABLE Tutorial (
    Activity_ID INTEGER PRIMARY KEY,
    CONSTRAINT FK_Tutorial_Activity FOREIGN KEY (Activity_ID)
        REFERENCES Activity (Activity_ID)
        ON UPDATE CASCADE ON DELETE CASCADE
);
COMMENT ON TABLE Tutorial IS 'Tutorial specialization - optional supplementary instruction';


CREATE TABLE Practical (
    Activity_ID INTEGER PRIMARY KEY,
    CONSTRAINT FK_Practical_Activity FOREIGN KEY (Activity_ID)
        REFERENCES Activity (Activity_ID)
        ON UPDATE CASCADE ON DELETE CASCADE
);
COMMENT ON TABLE Practical IS 'Practical specialization - optional laboratory work';




CREATE TABLE Student_Tutorial_Attendance (
    Student_ID INTEGER NOT NULL,
    Activity_ID INTEGER NOT NULL,
    Attendance_Date DATE NOT NULL DEFAULT CURRENT_DATE, -
    Attended BOOLEAN DEFAULT FALSE,
    Attendance_Time TIME,
    Special_Accommodations TEXT,
    CONSTRAINT PK_Student_Tutorial_Attendance PRIMARY KEY (Student_ID, Activity_ID, Attendance_Date),
    CONSTRAINT FK_StudentTutorial_Student FOREIGN KEY (Student_ID)
        REFERENCES Student (Student_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT FK_StudentTutorial_Tutorial FOREIGN KEY (Activity_ID)
        REFERENCES Tutorial (Activity_ID) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE Student_Practical_Attendance (
    Student_ID INTEGER NOT NULL,
    Activity_ID INTEGER NOT NULL,
    Attendance_Date DATE NOT NULL DEFAULT CURRENT_DATE,
    Attended BOOLEAN DEFAULT FALSE,
    Attendance_Time TIME,
    Special_Accommodations TEXT,
    CONSTRAINT PK_Student_Practical_Attendance PRIMARY KEY (Student_ID, Activity_ID, Attendance_Date),
    CONSTRAINT FK_StudentPractical_Student FOREIGN KEY (Student_ID)
        REFERENCES Student (Student_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT FK_StudentPractical_Practical FOREIGN KEY (Activity_ID)
        REFERENCES Practical (Activity_ID) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- =====================================================================
-- SECTION 6: ENROLLMENT & EXAMS
-- =====================================================================

CREATE TABLE Enrollment (
    Enrollment_ID SERIAL PRIMARY KEY,
    Student_ID INTEGER NOT NULL,
    Course_ID INTEGER NOT NULL,
    Department_ID INTEGER NOT NULL,
    Semester_ID INTEGER NOT NULL,
    Status VARCHAR(20) DEFAULT 'Enrolled' CHECK (Status IN ('Enrolled', 'Passed', 'Failed', 'Excluded', 'Resit Eligible')),
    CONSTRAINT UN_Enrollment_Unique UNIQUE (Student_ID, Course_ID, Department_ID, Semester_ID),
    CONSTRAINT FK_Enrollment_Student FOREIGN KEY (Student_ID)
        REFERENCES Student (Student_ID) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT FK_Enrollment_Course FOREIGN KEY (Course_ID, Department_ID)
        REFERENCES Course (Course_ID, Department_ID) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT FK_Enrollment_Semester FOREIGN KEY (Semester_ID)
        REFERENCES Semester (Semester_ID) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE Exam (
    Exam_ID INTEGER NOT NULL,
    Course_ID INTEGER NOT NULL,
    Department_ID INTEGER NOT NULL,
    Exam_Type VARCHAR(30) NOT NULL CHECK (Exam_Type IN ('Midterm', 'Final', 'Quiz', 'Practical Test', 'Oral Exam', 'Resit')),
    Exam_Name VARCHAR(100) NOT NULL,
    Duration_Minutes INTEGER NOT NULL CHECK (Duration_Minutes > 0),
    Total_Points NUMERIC(5,2) NOT NULL CHECK (Total_Points > 0),
    Instructions TEXT,
    CONSTRAINT PK_Exam PRIMARY KEY (Course_ID, Department_ID, Exam_ID),
    CONSTRAINT FK_Exam_Course FOREIGN KEY (Course_ID, Department_ID)
        REFERENCES Course (Course_ID, Department_ID)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Exam_Schedule (
    Schedule_ID SERIAL PRIMARY KEY,
    Exam_ID INTEGER NOT NULL,
    Course_ID INTEGER NOT NULL,
    Department_ID INTEGER NOT NULL,
    Building VARCHAR(1) NOT NULL,
    RoomNo VARCHAR(10) NOT NULL,
    Invigilator_ID INTEGER,
    Exam_Date DATE NOT NULL,
    Start_Time TIME NOT NULL,
    End_Time TIME NOT NULL,
    Status VARCHAR(20) DEFAULT 'Scheduled' CHECK (Status IN ('Scheduled', 'In Progress', 'Completed', 'Cancelled')),
    CONSTRAINT CK_ExamSchedule_Time CHECK (Start_Time < End_Time),
    CONSTRAINT FK_ExamSchedule_Exam FOREIGN KEY (Course_ID, Department_ID, Exam_ID)
        REFERENCES Exam (Course_ID, Department_ID, Exam_ID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT FK_ExamSchedule_Room FOREIGN KEY (Building, RoomNo)
        REFERENCES Room (Building, RoomNo)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT FK_ExamSchedule_Invigilator FOREIGN KEY (Invigilator_ID)
        REFERENCES Instructor (Instructor_ID)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT UN_Room_Time_Date UNIQUE (Building, RoomNo, Exam_Date, Start_Time)
);

CREATE TABLE Student_Exam (
    Student_ID INTEGER NOT NULL,
    Course_ID INTEGER NOT NULL,
    Department_ID INTEGER NOT NULL,
    Exam_ID INTEGER NOT NULL,
    Schedule_ID INTEGER NOT NULL,
    Attended BOOLEAN DEFAULT FALSE,
    Attendance_Time TIME,
    Seat_Number VARCHAR(10),
    Special_Accommodations TEXT,
    CONSTRAINT PK_Student_Exam PRIMARY KEY (Student_ID, Course_ID, Department_ID, Exam_ID),
    CONSTRAINT FK_StudentExam_Student FOREIGN KEY (Student_ID)
        REFERENCES Student (Student_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT FK_StudentExam_Exam FOREIGN KEY (Course_ID, Department_ID, Exam_ID)
        REFERENCES Exam (Course_ID, Department_ID, Exam_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT FK_StudentExam_Schedule FOREIGN KEY (Schedule_ID)
        REFERENCES Exam_Schedule (Schedule_ID) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE Grade (
    Grade_ID SERIAL PRIMARY KEY,
    Student_ID INTEGER NOT NULL,
    Course_ID INTEGER NOT NULL,
    Department_ID INTEGER NOT NULL,
    Exam_ID INTEGER,
    Semester_ID INTEGER NOT NULL,
    Grade_Type VARCHAR(30) NOT NULL,
    Grade_Date DATE NOT NULL DEFAULT CURRENT_DATE,
    Grade_Source VARCHAR(10) NOT NULL DEFAULT 'Other' CHECK (Grade_Source IN ('Exam', 'Other')),
    Grade_Value NUMERIC(5,2) NOT NULL,
    Max_Points NUMERIC(5,2) NOT NULL,
    Comments VARCHAR(500),
    CONSTRAINT CK_Grade_Value CHECK (Grade_Value >= 0 AND Grade_Value <= Max_Points),
    CONSTRAINT CK_Max_Points CHECK (Max_Points > 0),
    CONSTRAINT CK_Grade_Type CHECK (Grade_Type IN ('Quiz', 'Midterm', 'Final', 'Assignment', 'Project', 'Practical Test', 'Homework', 'Oral Exam', 'Resit')),
    CONSTRAINT CK_Grade_Exam_Required CHECK (
        (Grade_Source = 'Exam' AND Exam_ID IS NOT NULL) OR
        (Grade_Source = 'Other' AND Exam_ID IS NULL)
    ),
    CONSTRAINT UN_Student_Grade UNIQUE (Student_ID, Course_ID, Department_ID, Grade_Type, Grade_Date),
    CONSTRAINT FK_Grade_Student FOREIGN KEY (Student_ID)
        REFERENCES Student (Student_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT FK_Grade_Course FOREIGN KEY (Course_ID, Department_ID)
        REFERENCES Course (Course_ID, Department_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT FK_Grade_Exam FOREIGN KEY (Course_ID, Department_ID, Exam_ID)
        REFERENCES Exam (Course_ID, Department_ID, Exam_ID) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT FK_Grade_Semester FOREIGN KEY (Semester_ID)
        REFERENCES Semester (Semester_ID) ON UPDATE CASCADE ON DELETE RESTRICT
);



CREATE TABLE Reservation (
    Reservation_ID SERIAL PRIMARY KEY,
    Building VARCHAR(1) NOT NULL,
    RoomNo VARCHAR(20) NOT NULL,
    Course_ID INTEGER NOT NULL,
    Department_ID INTEGER NOT NULL,
    Activity_Type VARCHAR(20) NOT NULL,
    Instructor_ID INTEGER NOT NULL,
    Reserv_Date DATE NOT NULL DEFAULT CURRENT_DATE,
    Start_Time TIME NOT NULL DEFAULT CURRENT_TIME,
    End_Time TIME NOT NULL DEFAULT '23:00:00',

    Hours_Number NUMERIC(4,2) NOT NULL,
    CONSTRAINT CK_Reservation_Hours CHECK (Hours_Number >= 0.5),
    CONSTRAINT CK_Reservation_Time CHECK (Start_Time < End_Time),
    CONSTRAINT CK_Activity_Type_Limit CHECK (Activity_Type IN ('Lecture', 'Tutorial', 'Practical')),
    CONSTRAINT CK_Reservation_Hours_Sync CHECK (Hours_Number = EXTRACT(EPOCH FROM (End_Time - Start_Time)) / 3600),
    CONSTRAINT FK_Reservation_Room FOREIGN KEY (Building, RoomNo)
        REFERENCES Room (Building, RoomNo)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT FK_Reservation_Activity FOREIGN KEY (Course_ID, Department_ID, Activity_Type)
        REFERENCES Activity (Course_ID, Department_ID, Activity_Type)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT FK_Reservation_Instructor FOREIGN KEY (Instructor_ID)
        REFERENCES Instructor (Instructor_ID)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT UN_Room_Schedule UNIQUE (Building, RoomNo, Reserv_Date, Start_Time)
);
