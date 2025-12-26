-- ============================================================================
--  NORMALIZATION TO BCNF
-- Assumption: The previous script (sql_for_dep_drop.sql) has been executed,
-- ============================================================================
-- 1. CREATE THE NEW INDEPENDENT ENTITY (DEPARTMENT REGISTRY)
-- This removes the transitive dependency from the Instructor table.
CREATE TABLE Department_Registry (
    Dept_Name varchar(25) PRIMARY KEY,
    Dept_Building varchar(1),
    Dept_Budget numeric(15, 2)
);

-- 2. RESTRUCTURE THE INSTRUCTOR TABLE
-- We keep Dept_Name as a Foreign Key, but move Building and Budget to the Registry.
-- First,we  ensure that we don't lose data (if you had data, you would insert it into the registry here)
-- Then, remove the attributes that cause the 3NF/BCNF violation.
ALTER TABLE Instructor DROP COLUMN IF EXISTS Dept_Building;
ALTER TABLE Instructor DROP COLUMN IF EXISTS Dept_Budget;

-- 3. ESTABLISH THE NEW REFERENTIAL INTEGRITY
-- Now Instructor is in BCNF because all non-prime attributes depend only on Instructor_ID.
ALTER TABLE Instructor
    ADD CONSTRAINT FK_Instructor_Dept_Registry
    FOREIGN KEY (Dept_Name) REFERENCES Department_Registry (Dept_Name)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
-- ============================================================================

-- END OF SCRIPT
