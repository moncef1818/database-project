
-- 1. Department (5 examples)
INSERT INTO Department (Department_id, name) VALUES (100, 'Cyber Defense');
INSERT INTO Department (Department_id, name) VALUES (101, 'Network Security');
INSERT INTO Department (Department_id, name) VALUES (102, 'Cryptography');
INSERT INTO Department (Department_id, name) VALUES (103, 'Ethical Hacking');
INSERT INTO Department (Department_id, name) VALUES (104, 'Digital Forensics');

-- 2. Student (5 examples, with Algerian addresses/cities)
INSERT INTO Student (Student_ID, Last_Name, First_Name, DOB, Address, City, Zip_Code, Phone, Fax, Email)
VALUES (100, 'Belkacem', 'Ahmed', '2002-03-15', '12 Rue Alger Centre', 'Algiers', '16000', '0551234567', NULL, 'ahmed.belkacem@ensc.dz');
INSERT INTO Student (Student_ID, Last_Name, First_Name, DOB, Address, City, Zip_Code, Phone, Fax, Email)
VALUES (101, 'Zahra', 'Fatima', '2001-07-22', '45 Boulevard Oran', 'Oran', '31000', '0662345678', NULL, 'fatima.zahra@ensc.dz');
INSERT INTO Student (Student_ID, Last_Name, First_Name, DOB, Address, City, Zip_Code, Phone, Fax, Email)
VALUES (102, 'Khalid', 'Mohamed', '2003-11-05', '78 Avenue Constantine', 'Constantine', '25000', '0773456789', '0773456790', 'mohamed.khalid@ensc.dz');
INSERT INTO Student (Student_ID, Last_Name, First_Name, DOB, Address, City, Zip_Code, Phone, Fax, Email)
VALUES (103, 'Aicha', 'Nadia', '2000-05-18', '23 Rue Annaba', 'Annaba', '23000', '0554567890', NULL, 'nadia.aicha@ensc.dz');
INSERT INTO Student (Student_ID, Last_Name, First_Name, DOB, Address, City, Zip_Code, Phone, Fax, Email)
VALUES (104, 'Hassan', 'Omar', '2004-09-30', '56 Boulevard Batna', 'Batna', '05000', '0665678901', NULL, 'omar.hassan@ensc.dz');

-- 3. Instructor (5 examples, ranks as per schema)
INSERT INTO Instructor (Instructor_ID, Department_ID, Last_Name, First_Name, Rank, Phone, Fax, Email)
VALUES (100, 100, 'Djoudi', 'Karim', 'PROF', '0556789012', '0556789013', 'karim.djoudi@ensc.dz');
INSERT INTO Instructor (Instructor_ID, Department_ID, Last_Name, First_Name, Rank, Phone, Fax, Email)
VALUES (101, 101, 'Benslimane', 'Amina', 'MCA', '0667890123', NULL, 'amina.benslimane@ensc.dz');
INSERT INTO Instructor (Instructor_ID, Department_ID, Last_Name, First_Name, Rank, Phone, Fax, Email)
VALUES (102, 102, 'Meziane', 'Rachid', 'MCB', '0778901234', '0778901235', 'rachid.meziane@ensc.dz');
INSERT INTO Instructor (Instructor_ID, Department_ID, Last_Name, First_Name, Rank, Phone, Fax, Email)
VALUES (103, 103, 'Lounis', 'Sofia', 'Substitute', '0559012345', NULL, 'sofia.lounis@ensc.dz');
INSERT INTO Instructor (Instructor_ID, Department_ID, Last_Name, First_Name, Rank, Phone, Fax, Email)
VALUES (104, 104, 'Cherif', 'Youssef', 'PROF', '0660123456', NULL, 'youssef.cherif@ensc.dz');

-- 4. Room (5 examples)
INSERT INTO Room (Building, RoomNo, Capacity) VALUES ('A', '101', 30);
INSERT INTO Room (Building, RoomNo, Capacity) VALUES ('B', '202', 50);
INSERT INTO Room (Building, RoomNo, Capacity) VALUES ('C', '303', 20);
INSERT INTO Room (Building, RoomNo, Capacity) VALUES ('D', '404', 100);
INSERT INTO Room (Building, RoomNo, Capacity) VALUES ('E', '505', 40);

-- 5. Course (5 examples, cybersecurity-themed)
INSERT INTO Course (Course_ID, Department_ID, name, Description)
VALUES (100, 100, 'Introduction to Cyber Defense', 'Basics of defensive security strategies and tools.');
INSERT INTO Course (Course_ID, Department_ID, name, Description)
VALUES (101, 101, 'Network Security Fundamentals', 'Covering firewalls, VPNs, and intrusion detection.');
INSERT INTO Course (Course_ID, Department_ID, name, Description)
VALUES (102, 102, 'Cryptography Principles', 'Encryption algorithms, key management, and crypto attacks.');
INSERT INTO Course (Course_ID, Department_ID, name, Description)
VALUES (103, 103, 'Ethical Hacking Techniques', 'Penetration testing methods using Kali Linux.');
INSERT INTO Course (Course_ID, Department_ID, name, Description)
VALUES (104, 104, 'Digital Forensics Investigation', 'Evidence collection, analysis, and reporting in cyber incidents.');

-- 6. Activity (5 examples, one per course for variety)
INSERT INTO Activity (Activity_Type, Course_ID, Department_ID, Hours_Per_Week) VALUES ('Lecture', 100, 100, 3.0);
INSERT INTO Activity (Activity_Type, Course_ID, Department_ID, Hours_Per_Week) VALUES ('Lecture', 101, 101, 2.5);
INSERT INTO Activity (Activity_Type, Course_ID, Department_ID, Hours_Per_Week) VALUES ('Lecture', 102, 102, 4.0);
INSERT INTO Activity (Activity_Type, Course_ID, Department_ID, Hours_Per_Week) VALUES ('Lecture', 103, 103, 3.5);
INSERT INTO Activity (Activity_Type, Course_ID, Department_ID, Hours_Per_Week) VALUES ('Lecture', 104, 104, 2.0);

-- 7. Exam (5 examples, one per course)
INSERT INTO Exam (Exam_ID, Course_ID, Department_ID, Exam_Type, Exam_Name, Duration_Minutes, Total_Points, Instructions)
VALUES (100, 100, 100, 'Midterm', 'Cyber Defense Midterm', 120, 100.00, 'Closed book, no electronics.');
INSERT INTO Exam (Exam_ID, Course_ID, Department_ID, Exam_Type, Exam_Name, Duration_Minutes, Total_Points, Instructions)
VALUES (101, 101, 101, 'Final', 'Network Security Final', 180, 150.00, 'Open notes, practical section included.');
INSERT INTO Exam (Exam_ID, Course_ID, Department_ID, Exam_Type, Exam_Name, Duration_Minutes, Total_Points, Instructions)
VALUES (102, 102, 102, 'Quiz', 'Cryptography Quiz 1', 45, 50.00, 'Multiple choice only.');
INSERT INTO Exam (Exam_ID, Course_ID, Department_ID, Exam_Type, Exam_Name, Duration_Minutes, Total_Points, Instructions)
VALUES (103, 103, 103, 'Practical Test', 'Hacking Practical', 90, 80.00, 'Hands-on with virtual machines.');
INSERT INTO Exam (Exam_ID, Course_ID, Department_ID, Exam_Type, Exam_Name, Duration_Minutes, Total_Points, Instructions)
VALUES (104, 104, 104, 'Oral Exam', 'Forensics Oral Defense', 60, 70.00, 'Present your analysis.');

-- 8. Exam_Schedule (5 examples, referencing exams/rooms/instructors)
INSERT INTO Exam_Schedule (Exam_ID, Course_ID, Department_ID, Building, RoomNo, Invigilator_ID, Exam_Date, Start_Time, End_Time, Status)
VALUES (100, 100, 100, 'A', '101', 100, '2025-12-25', '09:00:00', '11:00:00', 'Scheduled');
INSERT INTO Exam_Schedule (Exam_ID, Course_ID, Department_ID, Building, RoomNo, Invigilator_ID, Exam_Date, Start_Time, End_Time, Status)
VALUES (101, 101, 101, 'B', '202', 101, '2025-12-26', '13:00:00', '16:00:00', 'Scheduled');
INSERT INTO Exam_Schedule (Exam_ID, Course_ID, Department_ID, Building, RoomNo, Invigilator_ID, Exam_Date, Start_Time, End_Time, Status)
VALUES (102, 102, 102, 'C', '303', 102, '2025-12-27', '10:00:00', '10:45:00', 'Scheduled');
INSERT INTO Exam_Schedule (Exam_ID, Course_ID, Department_ID, Building, RoomNo, Invigilator_ID, Exam_Date, Start_Time, End_Time, Status)
VALUES (103, 103, 103, 'D', '404', 103, '2025-12-28', '14:00:00', '15:30:00', 'Scheduled');
INSERT INTO Exam_Schedule (Exam_ID, Course_ID, Department_ID, Building, RoomNo, Invigilator_ID, Exam_Date, Start_Time, End_Time, Status)
VALUES (104, 104, 104, 'E', '505', 104, '2025-12-29', '11:00:00', '12:00:00', 'Scheduled');

-- 9. Student_Exam (5 examples, referencing students/exams/schedules)
INSERT INTO Student_Exam (Student_ID, Course_ID, Department_ID, Exam_ID, Schedule_ID, Attended, Attendance_Time, Seat_Number, Special_Accommodations)
VALUES (100, 100, 100, 100, 1, TRUE, '09:05:00', 'A1', NULL);  -- Assume Schedule_IDs are SERIAL starting from 1
INSERT INTO Student_Exam (Student_ID, Course_ID, Department_ID, Exam_ID, Schedule_ID, Attended, Attendance_Time, Seat_Number, Special_Accommodations)
VALUES (101, 101, 101, 101, 2, FALSE, NULL, NULL, 'Extra time due to disability');
INSERT INTO Student_Exam (Student_ID, Course_ID, Department_ID, Exam_ID, Schedule_ID, Attended, Attendance_Time, Seat_Number, Special_Accommodations)
VALUES (102, 102, 102, 102, 3, TRUE, '10:02:00', 'C3', NULL);
INSERT INTO Student_Exam (Student_ID, Course_ID, Department_ID, Exam_ID, Schedule_ID, Attended, Attendance_Time, Seat_Number, Special_Accommodations)
VALUES (103, 103, 103, 103, 4, TRUE, '14:10:00', 'D4', 'Quiet room');
INSERT INTO Student_Exam (Student_ID, Course_ID, Department_ID, Exam_ID, Schedule_ID, Attended, Attendance_Time, Seat_Number, Special_Accommodations)
VALUES (104, 104, 104, 104, 5, FALSE, NULL, NULL, NULL);

-- 10. Grade (5 examples, some with Exam_ID, using updated types)
INSERT INTO Grade (Student_ID, Course_ID, Department_ID, Exam_ID, Grade_Type, Grade_Date, Grade_Source, Grade_Value, Max_Points, Comments)
VALUES (100, 100, 100, 100, 'Midterm', '2025-12-25', 'Exam', 85.50, 100.00, 'Strong performance');
INSERT INTO Grade (Student_ID, Course_ID, Department_ID, Exam_ID, Grade_Type, Grade_Date, Grade_Source, Grade_Value, Max_Points, Comments)
VALUES (101, 101, 101, NULL, 'Assignment', '2025-12-26', 'Other', 92.00, 100.00, 'Excellent submission');
INSERT INTO Grade (Student_ID, Course_ID, Department_ID, Exam_ID, Grade_Type, Grade_Date, Grade_Source, Grade_Value, Max_Points, Comments)
VALUES (102, 102, 102, 102, 'Quiz', '2025-12-27', 'Exam', 45.00, 50.00, 'Good effort');
INSERT INTO Grade (Student_ID, Course_ID, Department_ID, Exam_ID, Grade_Type, Grade_Date, Grade_Source, Grade_Value, Max_Points, Comments)
VALUES (103, 103, 103, NULL, 'Project', '2025-12-28', 'Other', 78.75, 80.00, 'Creative approach');
INSERT INTO Grade (Student_ID, Course_ID, Department_ID, Exam_ID, Grade_Type, Grade_Date, Grade_Source, Grade_Value, Max_Points, Comments)
VALUES (104, 104, 104, 104, 'Oral Exam', '2025-12-29', 'Exam', 65.00, 70.00, 'Needs more practice');

INSERT INTO Reservation (Building, RoomNo, Course_ID, Department_ID, Activity_Type, Instructor_ID, Reserv_Date, Start_Time, End_Time, Hours_Number)
VALUES ('A', '101', 100, 100, 'Lecture', 100, '2025-12-25', '08:00:00', '11:00:00', 3);
INSERT INTO Reservation (Building, RoomNo, Course_ID, Department_ID, Activity_Type, Instructor_ID, Reserv_Date, Start_Time, End_Time, Hours_Number)
VALUES ('B', '202', 101, 101, 'Lecture', 101, '2025-12-26', '13:00:00', '15:30:00', 2);
INSERT INTO Reservation (Building, RoomNo, Course_ID, Department_ID, Activity_Type, Instructor_ID, Reserv_Date, Start_Time, End_Time, Hours_Number)
VALUES ('C', '303', 102, 102, 'Lecture', 102, '2025-12-27', '09:00:00', '13:00:00', 4);
INSERT INTO Reservation (Building, RoomNo, Course_ID, Department_ID, Activity_Type, Instructor_ID, Reserv_Date, Start_Time, End_Time, Hours_Number)
VALUES ('D', '404', 103, 103, 'Lecture', 103, '2025-12-28', '14:00:00', '17:00:00', 3);
INSERT INTO Reservation (Building, RoomNo, Course_ID, Department_ID, Activity_Type, Instructor_ID, Reserv_Date, Start_Time, End_Time, Hours_Number)
VALUES ('E', '505', 104, 104, 'Lecture', 104, '2025-12-29', '10:00:00', '12:00:00', 2);
