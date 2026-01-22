-- 1. DROP REFERENTIAL INTEGRITY FIRST
-- We remove the foreign keys that point to Department or use the old composite Course key
ALTER TABLE Course DROP CONSTRAINT IF EXISTS FK_Course_Department;
ALTER TABLE Instructor DROP CONSTRAINT IF EXISTS FK_Instructor_Department_ID;
ALTER TABLE Reservation DROP CONSTRAINT IF EXISTS FK_Reservation_Course;
ALTER TABLE Enrollment DROP CONSTRAINT IF EXISTS FK_Enrollment_Course;
ALTER TABLE Grade DROP CONSTRAINT IF EXISTS FK_Grade_Course;

-- 2. TRANSFORM COURSE (FROM WEAK TO STRONG)
-- Remove the old composite Primary Key (Course_ID, Department_ID)
ALTER TABLE Course DROP CONSTRAINT IF EXISTS PK_Course;
-- Create the new simple Primary Key
ALTER TABLE Course ADD CONSTRAINT PK_Course PRIMARY KEY (Course_ID);
-- Remove the orphaned column
ALTER TABLE Course DROP COLUMN IF EXISTS Department_ID;

ALTER TABLE Instructor
    ADD COLUMN IF NOT EXISTS Dept_Name varchar(25),
    ADD COLUMN IF NOT EXISTS Dept_Building varchar(1),
    ADD COLUMN IF NOT EXISTS Dept_Budget numeric(15, 2);

ALTER TABLE Instructor DROP COLUMN IF EXISTS Department_ID;

ALTER TABLE Reservation DROP COLUMN IF EXISTS Department_ID;
ALTER TABLE Enrollment DROP COLUMN IF EXISTS Department_ID;
ALTER TABLE Grade DROP COLUMN IF EXISTS Department_ID;

ALTER TABLE Reservation ADD CONSTRAINT FK_Reservation_Course
    FOREIGN KEY (Course_ID) REFERENCES Course (Course_ID);
ALTER TABLE Enrollment ADD CONSTRAINT FK_Enrollment_Course
    FOREIGN KEY (Course_ID) REFERENCES Course (Course_ID);
ALTER TABLE Grade ADD CONSTRAINT FK_Grade_Course
    FOREIGN KEY (Course_ID) REFERENCES Course (Course_ID);

DROP TABLE IF EXISTS Department;
