-
CREATE OR REPLACE FUNCTION get_student_by_group(p_group_id INTEGER DEFAULT NULL)
RETURNS TABLE (
    student_id INTEGER,
    last_name VARCHAR,
    first_name VARCHAR,
    email VARCHAR,
    group_name VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        S.Student_ID,
        S.Last_Name,
        S.First_Name,
        S.Email,
        G.Group_Name
    FROM Student S
    LEFT JOIN "Group" G ON S.Group_ID = G.Group_ID
    WHERE (p_group_id IS NULL OR S.Group_ID = p_group_id)
    ORDER BY G.Group_Name, S.Last_Name;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_students_by_section(p_section_id INTEGER DEFAULT NULL)
RETURNS TABLE (
    student_id INTEGER,
    last_name VARCHAR,
    first_name VARCHAR,
    email VARCHAR,
    section_name VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        S.Student_ID,
        S.Last_Name,
        S.First_Name,
        S.Email,
        SEC.Name AS Section_Name
    FROM Student S
    LEFT JOIN "Group" G ON S.Group_ID = G.Group_ID
    LEFT JOIN Section SEC ON G.Section_ID = SEC.Section_ID
    WHERE (p_section_id IS NULL OR G.Section_ID = p_section_id)
    ORDER BY SEC.Name, S.Last_Name;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION get_instructor_timetable(p_instructor_id INTEGER)
RETURNS TABLE (
    reserv_date DATE,
    start_time TIME,
    end_time TIME,
    course_name VARCHAR,
    activity_type VARCHAR,
    building VARCHAR,
    roomno VARCHAR,
    hours_number NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        R.Reserv_Date,
        R.Start_Time,
        R.End_Time,
        C.name AS Course_Name,
        A.Activity_Type,
        R.Building,
        R.RoomNo,
        R.Hours_Number
    FROM Reservation R
    JOIN Activity A ON R.Course_ID = A.Course_ID
                    AND R.Department_ID = A.Department_ID
                    AND R.Activity_Type = A.Activity_Type
    JOIN Course C ON R.Course_ID = C.Course_ID
                  AND R.Department_ID = C.Department_ID
    WHERE R.Instructor_ID = p_instructor_id
    ORDER BY R.Reserv_Date, R.Start_Time;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_student_timetable_by_section_group(
    p_section_id INTEGER DEFAULT NULL,
    p_group_id INTEGER DEFAULT NULL
)
RETURNS TABLE (
    student_id INTEGER,
    last_name VARCHAR,
    first_name VARCHAR,
    section_name VARCHAR,
    group_name VARCHAR,
    reserv_date DATE,
    start_time TIME,
    end_time TIME,
    course_name VARCHAR,
    activity_type VARCHAR,
    building VARCHAR,
    roomno VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        S.Student_ID,
        S.Last_Name,
        S.First_Name,
        SEC.Name AS Section_Name,
        G.Group_Name,
        R.Reserv_Date,
        R.Start_Time,
        R.End_Time,
        C.name AS Course_Name,
        A.Activity_Type,
        R.Building,
        R.RoomNo
    FROM Student S
    LEFT JOIN "Group" G ON S.Group_ID = G.Group_ID
    LEFT JOIN Section SEC ON G.Section_ID = SEC.Section_ID
    JOIN Enrollment E ON S.Student_ID = E.Student_ID
    JOIN Reservation R ON E.Course_ID = R.Course_ID
                       AND E.Department_ID = R.Department_ID
    JOIN Activity A ON R.Course_ID = A.Course_ID
                    AND R.Department_ID = A.Department_ID
                    AND R.Activity_Type = A.Activity_Type
    JOIN Course C ON R.Course_ID = C.Course_ID
                  AND R.Department_ID = C.Department_ID
    WHERE (p_section_id IS NULL OR G.Section_ID = p_section_id)
      AND (p_group_id IS NULL OR S.Group_ID = p_group_id)
    ORDER BY SEC.Name, G.Group_Name, S.Last_Name, R.Reserv_Date, R.Start_Time;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_student_passed_semester(p_semester_id INTEGER)
RETURNS TABLE (
    student_id INTEGER,
    last_name VARCHAR,
    first_name VARCHAR,
    semester_name VARCHAR,
    avg_grade NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        S.Student_ID,
        S.Last_Name,
        S.First_Name,
        SEM.Name AS Semester_Name,
        (SUM(
            CASE G.Grade_Type
                WHEN 'Quiz'       THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                WHEN 'Assignment' THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                WHEN 'Midterm'    THEN (G.Grade_Value / G.Max_Points) * 20 * 0.30
                WHEN 'Project'    THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                WHEN 'Final'      THEN (G.Grade_Value / G.Max_Points) * 20 * 0.40
                ELSE 0
            END
        ) / COUNT(DISTINCT G.Course_ID))::NUMERIC AS avg_grade
    FROM Student S
    JOIN Enrollment E ON S.Student_ID = E.Student_ID
    JOIN Grade G ON E.Student_ID = G.Student_ID
                 AND E.Course_ID = G.Course_ID
                 AND E.Department_ID = G.Department_ID
                 AND E.Semester_ID = G.Semester_ID
    JOIN Semester SEM ON E.Semester_ID = SEM.Semester_ID
    WHERE E.Semester_ID = p_semester_id
    GROUP BY S.Student_ID, S.Last_Name, S.First_Name, SEM.Name
    HAVING (SUM(
            CASE G.Grade_Type
                WHEN 'Quiz'       THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                WHEN 'Assignment' THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                WHEN 'Midterm'    THEN (G.Grade_Value / G.Max_Points) * 20 * 0.30
                WHEN 'Project'    THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                WHEN 'Final'      THEN (G.Grade_Value / G.Max_Points) * 20 * 0.40
                ELSE 0
            END
        ) / COUNT(DISTINCT G.Course_ID)) >= 10
    ORDER BY S.Last_Name;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_disqualifying_marks_by_module(
    p_course_id INTEGER,
    p_department_id INTEGER
)
RETURNS TABLE (
    student_id INTEGER,
    last_name VARCHAR,
    first_name VARCHAR,
    student_avg NUMERIC,
    promo_avg NUMERIC
)
AS $$
BEGIN
    RETURN QUERY
    WITH student_averages AS (
        SELECT
            S.Student_ID,
            S.Last_Name,
            S.First_Name,
            SUM(
                CASE G.Grade_Type
                    WHEN 'Quiz' THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                    WHEN 'Assignment' THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                    WHEN 'Midterm' THEN (G.Grade_Value / G.Max_Points) * 20 * 0.30
                    WHEN 'Project' THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                    WHEN 'Final' THEN (G.Grade_Value / G.Max_Points) * 20 * 0.40
                    ELSE 0
                END
            ) AS avg_value
        FROM Student S
        JOIN Grade G ON S.Student_ID = G.Student_ID
        WHERE G.Course_ID = p_course_id
          AND G.Department_ID = p_department_id
        GROUP BY S.Student_ID, S.Last_Name, S.First_Name
    ),
    promo_average AS (
        SELECT AVG(avg_value) AS promo_avg
        FROM student_averages
    )
    SELECT
        sa.Student_ID,
        sa.Last_Name,
        sa.First_Name,
        sa.avg_value,
    FROM student_averages sa
    CROSS JOIN promo_average pa
    WHERE sa.avg_value < pa.promo_avg * 0.6
    ORDER BY sa.Last_Name;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_average_marks_by_course_group(
    p_course_id INTEGER,
    p_department_id INTEGER
)
RETURNS TABLE (
    course_id INTEGER,
    course_name VARCHAR,
    group_id INTEGER,
    group_name VARCHAR,
    avg_mark NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        C.Course_ID,
        C.Name AS Course_Name,
        GR.Group_ID,
        GR.Group_Name,
        AVG(
            CASE G.Grade_Type
                WHEN 'Quiz' THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                WHEN 'Midterm' THEN (G.Grade_Value / G.Max_Points) * 20 * 0.30
                WHEN 'Final' THEN (G.Grade_Value / G.Max_Points) * 20 * 0.40
                WHEN 'Assignment' THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                WHEN 'Project' THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                ELSE 0
            END
        ) AS Avg_Mark
    FROM Student S
    JOIN "Group" GR ON S.Group_ID = GR.Group_ID
    JOIN Grade G ON S.Student_ID = G.Student_ID
    JOIN Course C ON G.Course_ID = C.Course_ID
                  AND G.Department_ID = C.Department_ID
    WHERE G.Course_ID = p_course_id
      AND G.Department_ID = p_department_id
    GROUP BY C.Course_ID, C.Name, GR.Group_ID, GR.Group_Name
    ORDER BY C.Name, GR.Group_Name;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_students_failing_module(
    p_course_id INTEGER,
    p_department_id INTEGER
)
RETURNS TABLE (
    student_id INTEGER,
    last_name VARCHAR,
    first_name VARCHAR,
    failing_grade NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        S.Student_ID,
        S.Last_Name,
        S.First_Name,
        SUM(
            CASE G.Grade_Type
                WHEN 'Quiz'       THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                WHEN 'Assignment' THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                WHEN 'Midterm'    THEN (G.Grade_Value / G.Max_Points) * 20 * 0.30
                WHEN 'Project'    THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                WHEN 'Final'      THEN (G.Grade_Value / G.Max_Points) * 20 * 0.40
                ELSE 0
            END
        )::NUMERIC AS failing_grade
    FROM Student S
    JOIN Grade G ON S.Student_ID = G.Student_ID
    WHERE G.Course_ID = p_course_id
      AND G.Department_ID = p_department_id
    GROUP BY S.Student_ID, S.Last_Name, S.First_Name
    HAVING SUM(
            CASE G.Grade_Type
                WHEN 'Quiz'       THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                WHEN 'Assignment' THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                WHEN 'Midterm'    THEN (G.Grade_Value / G.Max_Points) * 20 * 0.30
                WHEN 'Project'    THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                WHEN 'Final'      THEN (G.Grade_Value / G.Max_Points) * 20 * 0.40
                ELSE 0
            END
        ) < 10
    ORDER BY S.Last_Name;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_students_resit_eligible(
    p_course_id INTEGER,
    p_department_id INTEGER
)
RETURNS TABLE (
    student_id INTEGER,
    last_name VARCHAR,
    first_name VARCHAR,
    course_avg NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        S.Student_ID,
        S.Last_Name,
        S.First_Name,
        SUM(
            CASE G.Grade_Type
                WHEN 'Quiz'       THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                WHEN 'Assignment' THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                WHEN 'Midterm'    THEN (G.Grade_Value / G.Max_Points) * 20 * 0.30
                WHEN 'Project'    THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                WHEN 'Final'      THEN (G.Grade_Value / G.Max_Points) * 20 * 0.40
                ELSE 0
            END
        )::NUMERIC AS course_avg
    FROM Student S
    JOIN Grade G ON S.Student_ID = G.Student_ID
    JOIN Enrollment E ON S.Student_ID = E.Student_ID
                      AND G.Course_ID = E.Course_ID
                      AND G.Department_ID = E.Department_ID
    WHERE G.Course_ID = p_course_id
      AND G.Department_ID = p_department_id
      AND E.Status = 'Resit Eligible'
    GROUP BY S.Student_ID, S.Last_Name, S.First_Name
    HAVING SUM(
            CASE G.Grade_Type
                WHEN 'Quiz'       THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                WHEN 'Assignment' THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                WHEN 'Midterm'    THEN (G.Grade_Value / G.Max_Points) * 20 * 0.30
                WHEN 'Project'    THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                WHEN 'Final'      THEN (G.Grade_Value / G.Max_Points) * 20 * 0.40
                ELSE 0
            END
        ) >= 8
       AND SUM(
            CASE G.Grade_Type
                WHEN 'Quiz'       THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                WHEN 'Assignment' THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                WHEN 'Midterm'    THEN (G.Grade_Value / G.Max_Points) * 20 * 0.30
                WHEN 'Project'    THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                WHEN 'Final'      THEN (G.Grade_Value / G.Max_Points) * 20 * 0.40
                ELSE 0
            END
        ) < 10
    ORDER BY S.Last_Name;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_students_excluded_from_module(
    p_course_id INTEGER,
    p_department_id INTEGER
)
RETURNS TABLE (
    student_id INTEGER,
    last_name VARCHAR,
    first_name VARCHAR,
    reason VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        S.Student_ID,
        S.Last_Name,
        S.First_Name,
        E.Status AS Reason
    FROM Student S
    JOIN Enrollment E ON S.Student_ID = E.Student_ID
    WHERE E.Course_ID = p_course_id
      AND E.Department_ID = p_department_id
      AND E.Status = 'Excluded'
    ORDER BY S.Last_Name;
END;
$$ LANGUAGE plpgsql;
