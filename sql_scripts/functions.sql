
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
        sa.Last_Name::VARCHAR,
        sa.First_Name::VARCHAR,
        ROUND(sa.avg_value, 2) AS student_avg,
        ROUND(pa.promo_avg, 2) AS promo_avg
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
    WITH student_totals AS (
        -- First, calculate each student's weighted total
        SELECT
            S.Student_ID,
            S.Group_ID,
            SUM(
                CASE G.Grade_Type
                    WHEN 'Quiz' THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                    WHEN 'Midterm' THEN (G.Grade_Value / G.Max_Points) * 20 * 0.30
                    WHEN 'Final' THEN (G.Grade_Value / G.Max_Points) * 20 * 0.40
                    WHEN 'Assignment' THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                    WHEN 'Project' THEN (G.Grade_Value / G.Max_Points) * 20 * 0.10
                    ELSE 0
                END
            ) AS student_total
        FROM Student S
        JOIN Grade G ON S.Student_ID = G.Student_ID
        WHERE G.Course_ID = p_course_id
          AND G.Department_ID = p_department_id
        GROUP BY S.Student_ID, S.Group_ID
    )
    -- Then, average those totals by group
    SELECT
        C.Course_ID,
        C.Name::VARCHAR AS Course_Name,
        GR.Group_ID,
        GR.Group_Name::VARCHAR,
        ROUND(AVG(st.student_total), 2) AS Avg_Mark
    FROM student_totals st
    JOIN "Group" GR ON st.Group_ID = GR.Group_ID
    CROSS JOIN Course C
    WHERE C.Course_ID = p_course_id
      AND C.Department_ID = p_department_id
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

-- this function used on the results processing submenu
CREATE OR REPLACE FUNCTION get_semester_overview(p_semester_id INTEGER)
RETURNS TABLE (
    total_students BIGINT,
    passed_count BIGINT,
    failed_count BIGINT,
    resit_count BIGINT,
    average_grade NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT
 COUNT(DISTINCT e.student_id)::BIGINT as total_students,
        COUNT(DISTINCT CASE WHEN e.status = 'Passed' THEN e.student_id END)::BIGINT as passed_count,
        COUNT(DISTINCT CASE WHEN e.status = 'Failed' THEN e.student_id END)::BIGINT as failed_count,
        COUNT(DISTINCT CASE WHEN e.status = 'Resit Eligible' THEN e.student_id END)::BIGINT as resit_count,
        ROUND(AVG(
            CASE
                WHEN g.grade_value IS NOT NULL AND g.max_points > 0
                THEN (g.grade_value / g.max_points) * 20
                ELSE 0
            END
        ), 2) as average_grade
    FROM Enrollment e
    LEFT JOIN Grade g ON e.student_id = g.student_id
        AND e.course_id = g.course_id
        AND e.department_id = g.department_id
        AND e.semester_id = g.semester_id
    WHERE e.semester_id = p_semester_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_course_comparison(p_semester_id INTEGER)
RETURNS TABLE (
    course_name VARCHAR,
    student_count BIGINT,
    average_grade NUMERIC,
    pass_rate NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.name::VARCHAR as course_name,
        COUNT(DISTINCT e.student_id)::BIGINT as student_count,
        ROUND(AVG(
            CASE g.grade_type
                WHEN 'Quiz' THEN (g.grade_value / g.max_points) * 20 * 0.10
                WHEN 'Assignment' THEN (g.grade_value / g.max_points) * 20 * 0.10
                WHEN 'Midterm' THEN (g.grade_value / g.max_points) * 20 * 0.30
                WHEN 'Project' THEN (g.grade_value / g.max_points) * 20 * 0.10
                WHEN 'Final' THEN (g.grade_value / g.max_points) * 20 * 0.40
                ELSE 0
            END
        ), 2) as average_grade,
        ROUND(
            100.0 * COUNT(CASE WHEN e.status = 'Passed' THEN 1 END)::NUMERIC /
            NULLIF(COUNT(DISTINCT e.student_id), 0),
            1
        ) as pass_rate
    FROM Course c
    JOIN Enrollment e ON c.course_id = e.course_id AND c.department_id = e.department_id
    LEFT JOIN Grade g ON e.student_id = g.student_id
        AND e.course_id = g.course_id
        AND e.department_id = g.department_id
        AND e.semester_id = g.semester_id
    WHERE e.semester_id = p_semester_id
    GROUP BY c.course_id, c.name
    ORDER BY average_grade DESC;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_grade_distribution(
    p_course_id INTEGER,
    p_department_id INTEGER
)
RETURNS TABLE (
    grade_range VARCHAR,
    student_count BIGINT,
    percentage NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    WITH student_averages AS (
        SELECT
            g.student_id,
            SUM(
                CASE g.grade_type
                    WHEN 'Quiz' THEN (g.grade_value / g.max_points) * 20 * 0.10
                    WHEN 'Assignment' THEN (g.grade_value / g.max_points) * 20 * 0.10
                    WHEN 'Midterm' THEN (g.grade_value / g.max_points) * 20 * 0.30
                    WHEN 'Project' THEN (g.grade_value / g.max_points) * 20 * 0.10
                    WHEN 'Final' THEN (g.grade_value / g.max_points) * 20 * 0.40
                    ELSE 0
                END
            ) as weighted_avg
        FROM Grade g
        WHERE g.course_id = p_course_id AND g.department_id = p_department_id
        GROUP BY g.student_id
    )
    SELECT
        CASE
            WHEN weighted_avg >= 0 AND weighted_avg < 5 THEN '0-5 (Fail)'
            WHEN weighted_avg >= 5 AND weighted_avg < 10 THEN '5-10 (Fail)'
            WHEN weighted_avg >= 10 AND weighted_avg < 15 THEN '10-15 (Pass)'
            WHEN weighted_avg >= 15 AND weighted_avg <= 20 THEN '15-20 (Excellent)'
        END::VARCHAR as grade_range,
        COUNT(*)::BIGINT as student_count,
        ROUND(100.0 * COUNT(*)::NUMERIC / SUM(COUNT(*)) OVER (), 1) as percentage
    FROM student_averages
    GROUP BY
        CASE
            WHEN weighted_avg >= 0 AND weighted_avg < 5 THEN '0-5 (Fail)'
            WHEN weighted_avg >= 5 AND weighted_avg < 10 THEN '5-10 (Fail)'
            WHEN weighted_avg >= 10 AND weighted_avg < 15 THEN '10-15 (Pass)'
            WHEN weighted_avg >= 15 AND weighted_avg <= 20 THEN '15-20 (Excellent)'
        END
    ORDER BY grade_range;
END;
$$ LANGUAGE plpgsql;
