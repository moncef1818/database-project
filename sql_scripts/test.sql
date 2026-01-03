
-- =====================================================================
-- 1. DEPARTMENTS (10 entries)
-- =====================================================================
INSERT INTO Department (name) VALUES
('Network Security'),
('Cryptography'),
('Digital Forensics'),
('Application Security'),
('System Security'),
('Cyber Intelligence'),
('Ethical Hacking'),
('Security Operations'),
('Risk Management'),
('Secure Software Development');

-- =====================================================================
-- 2. SECTIONS (10 entries)
-- =====================================================================
INSERT INTO Section (Name) VALUES
('L1 Cybersécurité - Section A'),
('L1 Cybersécurité - Section B'),
('L2 Cybersécurité - Section A'),
('L2 Cybersécurité - Section B'),
('L3 Cybersécurité - Section A'),
('M1 Sécurité Réseaux - Section A'),
('M1 Cryptographie - Section A'),
('M2 Forensics - Section A'),
('M2 Pentesting - Section A'),
('Doctorat - Section Recherche');

-- =====================================================================
-- 3. GROUPS (10 entries)
-- =====================================================================
INSERT INTO "Group" (Section_ID, Group_Name) VALUES
(1, 'Groupe 01'),
(1, 'Groupe 02'),
(2, 'Groupe 01'),
(3, 'Groupe 01'),
(3, 'Groupe 02'),
(4, 'Groupe 01'),
(5, 'Groupe 01'),
(6, 'Groupe 01'),
(7, 'Groupe 01'),
(8, 'Groupe 01');

-- =====================================================================
-- 4. STUDENTS (10 entries - Realistic Algerian names)
-- =====================================================================
INSERT INTO Student (Group_ID, Last_Name, First_Name, DOB, Address, City, Zip_Code, Phone, Email) VALUES
(1, 'Benali', 'Yacine', '2005-03-15', 'Cité 1000 Logements', 'Sétif', '19000', '0770123456', 'y.benali@student.ensc.dz'),
(1, 'Khelifi', 'Amina', '2005-07-22', 'Rue Larbi Ben M''hidi', 'Sétif', '19000', '0771234567', 'a.khelifi@student.ensc.dz'),
(2, 'Boudiaf', 'Rayan', '2005-11-08', 'Cité El Hidhab', 'Sétif', '19000', '0772345678', 'r.boudiaf@student.ensc.dz'),
(3, 'Cherif', 'Lina', '2004-02-14', 'Résidence Ain El Fouara', 'Sétif', '19000', '0773456789', 'l.cherif@student.ensc.dz'),
(4, 'Mokhtar', 'Amine', '2004-06-30', 'Cité Maabouda', 'Sétif', '19000', '0774567890', 'a.mokhtar@student.ensc.dz'),
(5, 'Rahmouni', 'Salma', '2003-09-12', 'Cité 20 Août', 'Sétif', '19000', '0775678901', 's.rahmouni@student.ensc.dz'),
(6, 'Mebarki', 'Karim', '2003-12-25', 'Nouvelle Ville', 'Sétif', '19000', '0776789012', 'k.mebarki@student.ensc.dz'),
(7, 'Zerrouki', 'Yasmine', '2002-04-18', 'Cité Chouf Lekdad', 'Sétif', '19000', '0777890123', 'y.zerrouki@student.ensc.dz'),
(8, 'Lahlou', 'Mehdi', '2002-08-05', 'Cité Tlidjene', 'Sétif', '19000', '0778901234', 'm.lahlou@student.ensc.dz'),
(9, 'Bouzidi', 'Nour', '2001-01-20', 'Cité El Bez', 'Sétif', '19000', '0779012345', 'n.bouzidi@student.ensc.dz');

-- =====================================================================
-- 5. INSTRUCTORS (10 entries - Algerian professors)
-- =====================================================================
INSERT INTO Instructor (Department_ID, Last_Name, First_Name, Rank, Phone, Email) VALUES
(1, 'Hadj Aissa', 'Farid', 'PROF', '0550111222', 'f.hadjaissa@ensc.dz'),
(2, 'Meftah', 'Samira', 'PROF', '0550222333', 's.meftah@ensc.dz'),
(3, 'Belkacem', 'Tarek', 'MCA', '0550333444', 't.belkacem@ensc.dz'),
(4, 'Djebbar', 'Leila', 'MCA', '0550444555', 'l.djebbar@ensc.dz'),
(5, 'Hamidi', 'Nabil', 'MCB', '0550555666', 'n.hamidi@ensc.dz'),
(6, 'Boukhalfa', 'Amira', 'MCB', '0550666777', 'a.boukhalfa@ensc.dz'),
(7, 'Slimani', 'Youcef', 'PROF', '0550777888', 'y.slimani@ensc.dz'),
(8, 'Khelladi', 'Asma', 'MCA', '0550888999', 'a.khelladi@ensc.dz'),
(9, 'Bencheikh', 'Omar', 'MCB', '0550999000', 'o.bencheikh@ensc.dz'),
(10, 'Rahmani', 'Siham', 'Substitute', '0550000111', 's.rahmani@ensc.dz');

-- =====================================================================
-- 6. ROOMS (10 entries)
-- =====================================================================
INSERT INTO Room (Building, RoomNo, Capacity) VALUES
('A', '101', 40),
('A', '102', 40),
('A', '201', 35),
('B', '101', 30),
('B', '102', 30),
('B', 'LAB01', 20),
('C', 'LAB02', 20),
('C', 'LAB03', 25),
('D', 'AMP01', 120),
('D', 'AMP02', 150);

-- =====================================================================
-- 7. SEMESTERS (10 entries)
-- =====================================================================
INSERT INTO Semester (Name, Start_Date, End_Date) VALUES
('Automne 2023', '2023-09-15', '2024-01-31'),
('Printemps 2024', '2024-02-15', '2024-06-30'),
('Automne 2024', '2024-09-15', '2025-01-31'),
('Printemps 2025', '2025-02-15', '2025-06-30'),
('Automne 2025', '2025-09-15', '2026-01-31'),
('Printemps 2026', '2026-02-15', '2026-06-30'),
('Session d''été 2024', '2024-07-01', '2024-08-31'),
('Session d''été 2025', '2025-07-01', '2025-08-31'),
('Session intensive 2024', '2024-06-01', '2024-06-30'),
('Session rattrapage 2025', '2025-09-01', '2025-09-14');

-- =====================================================================
-- 8. COURSES (10 entries - Cybersecurity focused)
-- =====================================================================
INSERT INTO Course (Department_ID, name, Description) VALUES
(1, 'Fundamentals of Network Security', 'Introduction to network protocols, TCP/IP security, firewalls, and intrusion detection systems'),
(2, 'Applied Cryptography', 'Study of encryption algorithms, public key infrastructure, digital signatures, and cryptographic protocols'),
(3, 'Digital Forensics and Incident Response', 'Techniques for investigating cyber crimes, evidence collection, and incident handling procedures'),
(4, 'Web Application Security', 'OWASP Top 10, XSS, CSRF, SQL injection, and secure coding practices for web applications'),
(5, 'Operating System Security', 'Linux/Windows hardening, access control, privilege escalation, and system-level vulnerabilities'),
(6, 'Cyber Threat Intelligence', 'Threat modeling, APT analysis, malware analysis, and intelligence gathering techniques'),
(7, 'Ethical Hacking and Penetration Testing', 'Hands-on pentesting methodology, vulnerability assessment, exploitation techniques, and reporting'),
(8, 'Security Operations Center (SOC)', 'SIEM configuration, log analysis, security monitoring, and incident response workflows'),
(9, 'Risk Assessment and Compliance', 'ISO 27001, NIST frameworks, risk management, security auditing, and compliance strategies'),
(10, 'Secure Software Development Lifecycle', 'DevSecOps, secure coding standards, code review, SAST/DAST tools, and SDL implementation');

-- =====================================================================
-- 9. ACTIVITIES (30 entries - 3 per course: Lecture, Tutorial, Practical)
-- =====================================================================
INSERT INTO Activity (Course_ID, Department_ID, Activity_Type) VALUES
(1, 1, 'Lecture'),
(1, 1, 'Tutorial'),
(1, 1, 'Practical'),
(2, 2, 'Lecture'),
(2, 2, 'Tutorial'),
(2, 2, 'Practical'),
(3, 3, 'Lecture'),
(3, 3, 'Tutorial'),
(3, 3, 'Practical'),
(4, 4, 'Lecture'),
(4, 4, 'Tutorial'),
(4, 4, 'Practical'),
(5, 5, 'Lecture'),
(5, 5, 'Tutorial'),
(5, 5, 'Practical'),
(6, 6, 'Lecture'),
(6, 6, 'Tutorial'),
(6, 6, 'Practical'),
(7, 7, 'Lecture'),
(7, 7, 'Tutorial'),
(7, 7, 'Practical'),
(8, 8, 'Lecture'),
(8, 8, 'Tutorial'),
(8, 8, 'Practical'),
(9, 9, 'Lecture'),
(9, 9, 'Tutorial'),
(9, 9, 'Practical'),
(10, 10, 'Lecture'),
(10, 10, 'Tutorial'),
(10, 10, 'Practical');

-- =====================================================================
-- 10. LECTURES (10 entries)
-- =====================================================================
INSERT INTO Lecture (Activity_ID) VALUES
(1), (4), (7), (10), (13), (16), (19), (22), (25), (28);

-- =====================================================================
-- 11. TUTORIALS (10 entries)
-- =====================================================================
INSERT INTO Tutorial (Activity_ID) VALUES
(2), (5), (8), (11), (14), (17), (20), (23), (26), (29);

-- =====================================================================
-- 12. PRACTICALS (10 entries)
-- =====================================================================
INSERT INTO Practical (Activity_ID) VALUES
(3), (6), (9), (12), (15), (18), (21), (24), (27), (30);

-- =====================================================================
-- 13. STUDENT TUTORIAL ATTENDANCE (10 entries)
-- =====================================================================
INSERT INTO Student_Tutorial_Attendance (Student_ID, Activity_ID, Attendance_Date, Attended, Attendance_Time) VALUES
(1, 2, '2024-09-20', TRUE, '10:15:00'),
(2, 2, '2024-09-20', TRUE, '10:12:00'),
(3, 5, '2024-09-21', FALSE, NULL),
(4, 8, '2024-09-22', TRUE, '14:20:00'),
(5, 11, '2024-09-23', TRUE, '08:30:00'),
(6, 14, '2024-09-24', TRUE, '11:05:00'),
(7, 17, '2024-09-25', FALSE, NULL),
(8, 20, '2024-09-26', TRUE, '13:15:00'),
(9, 23, '2024-09-27', TRUE, '09:45:00'),
(10, 26, '2024-09-28', TRUE, '15:30:00');

-- =====================================================================
-- 14. STUDENT PRACTICAL ATTENDANCE (10 entries)
-- =====================================================================
INSERT INTO Student_Practical_Attendance (Student_ID, Activity_ID, Attendance_Date, Attended, Attendance_Time, Special_Accommodations) VALUES
(1, 3, '2024-09-25', TRUE, '14:00:00', NULL),
(2, 3, '2024-09-25', TRUE, '13:58:00', NULL),
(3, 6, '2024-09-26', TRUE, '10:30:00', NULL),
(4, 9, '2024-09-27', TRUE, '16:15:00', NULL),
(5, 12, '2024-09-28', FALSE, NULL, 'Medical absence'),
(6, 15, '2024-09-29', TRUE, '08:45:00', NULL),
(7, 18, '2024-09-30', TRUE, '14:30:00', NULL),
(8, 21, '2024-10-01', TRUE, '11:00:00', NULL),
(9, 24, '2024-10-02', TRUE, '15:45:00', NULL),
(10, 27, '2024-10-03', TRUE, '09:15:00', 'Extended time for practical exam');

-- =====================================================================
-- 15. ENROLLMENTS (10 entries)
-- =====================================================================
INSERT INTO Enrollment (Student_ID, Course_ID, Department_ID, Semester_ID, Status) VALUES
(1, 1, 1, 3, 'Enrolled'),
(2, 1, 1, 3, 'Enrolled'),
(3, 2, 2, 3, 'Enrolled'),
(4, 3, 3, 3, 'Enrolled'),
(5, 4, 4, 3, 'Passed'),
(6, 5, 5, 3, 'Enrolled'),
(7, 6, 6, 3, 'Enrolled'),
(8, 7, 7, 3, 'Resit Eligible'),
(9, 8, 8, 3, 'Enrolled'),
(10, 9, 9, 3, 'Enrolled');

-- =====================================================================
-- 16. EXAMS (10 entries)
-- =====================================================================
INSERT INTO Exam (Exam_ID, Course_ID, Department_ID, Exam_Type, Exam_Name, Duration_Minutes, Total_Points, Instructions) VALUES
(1, 1, 1, 'Midterm', 'Network Security Midterm Exam', 90, 20.00, 'Answer all questions. Use of notes is not permitted.'),
(2, 1, 1, 'Final', 'Network Security Final Exam', 120, 30.00, 'Comprehensive exam covering all course material.'),
(3, 2, 2, 'Midterm', 'Cryptography Theory Test', 90, 20.00, 'Mathematical proofs required for all questions.'),
(4, 3, 3, 'Practical Test', 'Forensics Lab Exam', 180, 25.00, 'Analyze the provided disk image and document findings.'),
(5, 4, 4, 'Quiz', 'OWASP Top 10 Quiz', 45, 10.00, 'Multiple choice and short answer questions.'),
(6, 5, 5, 'Final', 'OS Security Comprehensive', 150, 35.00, 'Includes both theoretical and practical components.'),
(7, 6, 6, 'Midterm', 'Threat Intelligence Assessment', 90, 20.00, 'Analyze APT scenarios and propose mitigation strategies.'),
(8, 7, 7, 'Practical Test', 'Pentesting Practical Exam', 240, 40.00, 'Complete penetration test on provided target network.'),
(9, 8, 8, 'Final', 'SOC Operations Final', 120, 30.00, 'SIEM configuration and incident response scenarios.'),
(10, 9, 9, 'Midterm', 'Risk Management Case Study', 90, 20.00, 'Analyze compliance requirements for given scenario.');

-- =====================================================================
-- 17. EXAM SCHEDULES (10 entries)
-- =====================================================================
INSERT INTO Exam_Schedule (Exam_ID, Course_ID, Department_ID, Building, RoomNo, Invigilator_ID, Exam_Date, Start_Time, End_Time, Status) VALUES
(1, 1, 1, 'D', 'AMP01', 1, '2024-11-15', '08:00:00', '09:30:00', 'Completed'),
(2, 1, 1, 'D', 'AMP02', 1, '2025-01-20', '09:00:00', '11:00:00', 'Scheduled'),
(3, 2, 2, 'A', '101', 2, '2024-11-16', '10:00:00', '11:30:00', 'Completed'),
(4, 3, 3, 'B', 'LAB01', 3, '2024-11-17', '14:00:00', '17:00:00', 'Completed'),
(5, 4, 4, 'A', '102', 4, '2024-11-10', '08:30:00', '09:15:00', 'Completed'),
(6, 5, 5, 'D', 'AMP01', 5, '2025-01-21', '13:00:00', '15:30:00', 'Scheduled'),
(7, 6, 6, 'A', '201', 6, '2024-11-18', '08:00:00', '09:30:00', 'Completed'),
(8, 7, 7, 'C', 'LAB02', 7, '2024-12-05', '08:00:00', '12:00:00', 'Scheduled'),
(9, 8, 8, 'B', '101', 8, '2025-01-22', '10:00:00', '12:00:00', 'Scheduled'),
(10, 9, 9, 'A', '101', 9, '2024-11-19', '14:00:00', '15:30:00', 'Completed');

-- =====================================================================
-- 18. STUDENT EXAM (10 entries)
-- =====================================================================
INSERT INTO Student_Exam (Student_ID, Course_ID, Department_ID, Exam_ID, Schedule_ID, Attended, Attendance_Time, Seat_Number) VALUES
(1, 1, 1, 1, 1, TRUE, '07:55:00', 'A15'),
(2, 1, 1, 1, 1, TRUE, '07:58:00', 'A16'),
(3, 2, 2, 3, 3, TRUE, '09:57:00', 'B10'),
(4, 3, 3, 4, 4, TRUE, '13:55:00', 'LAB-05'),
(5, 4, 4, 5, 5, TRUE, '08:28:00', 'C12'),
(6, 5, 5, 6, 6, FALSE, NULL, 'D08'),
(7, 6, 6, 7, 7, TRUE, '07:52:00', 'A20'),
(8, 7, 7, 8, 8, TRUE, '07:45:00', 'LAB-12'),
(9, 8, 8, 9, 9, TRUE, '09:58:00', 'B05'),
(10, 9, 9, 10, 10, TRUE, '13:55:00', 'A08');

-- =====================================================================
-- 19. GRADES (10 entries)
-- =====================================================================
INSERT INTO Grade (Student_ID, Course_ID, Department_ID, Exam_ID, Semester_ID, Grade_Type, Grade_Date, Grade_Source, Grade_Value, Max_Points, Comments) VALUES
(1, 1, 1, 1, 3, 'Midterm', '2024-11-20', 'Exam', 16.50, 20.00, 'Excellent understanding of firewall concepts'),
(2, 1, 1, 1, 3, 'Midterm', '2024-11-20', 'Exam', 14.00, 20.00, 'Good work, review TCP/IP security'),
(3, 2, 2, 3, 3, 'Midterm', '2024-11-21', 'Exam', 18.00, 20.00, 'Outstanding cryptographic analysis'),
(4, 3, 3, 4, 3, 'Practical Test', '2024-11-22', 'Exam', 22.00, 25.00, 'Thorough forensic investigation'),
(5, 4, 4, 5, 3, 'Quiz', '2024-11-15', 'Exam', 9.50, 10.00, 'Excellent knowledge of web vulnerabilities'),
(6, 5, 5, NULL, 3, 'Assignment', '2024-10-30', 'Other', 18.00, 20.00, 'Comprehensive Linux hardening guide'),
(7, 6, 6, 7, 3, 'Midterm', '2024-11-23', 'Exam', 15.50, 20.00, 'Good threat modeling approach'),
(8, 7, 7, NULL, 3, 'Project', '2024-11-28', 'Other', 32.00, 40.00, 'Complete pentest report with detailed findings'),
(9, 8, 8, NULL, 3, 'Homework', '2024-10-15', 'Other', 17.00, 20.00, 'Well-configured SIEM rules'),
(10, 9, 9, 10, 3, 'Midterm', '2024-11-24', 'Exam', 17.50, 20.00, 'Solid risk assessment methodology');

-- =====================================================================
-- 20. RESERVATIONS (10 entries)
-- =====================================================================
INSERT INTO Reservation (Building, RoomNo, Course_ID, Department_ID, Activity_Type, Instructor_ID, Reserv_Date, Start_Time, End_Time, Hours_Number) VALUES
('A', '101', 1, 1, 'Lecture', 1, '2024-09-16', '08:00:00', '10:00:00', 2.00),
('A', '102', 2, 2, 'Lecture', 2, '2024-09-16', '10:30:00', '12:30:00', 2.00),
('B', 'LAB01', 1, 1, 'Practical', 1, '2024-09-18', '14:00:00', '17:00:00', 3.00),
('C', 'LAB02', 2, 2, 'Practical', 2, '2024-09-19', '14:00:00', '17:00:00', 3.00),
('A', '201', 3, 3, 'Lecture', 3, '2024-09-17', '08:30:00', '10:30:00', 2.00),
('B', '101', 4, 4, 'Tutorial', 4, '2024-09-20', '13:00:00', '15:00:00', 2.00),
('C', 'LAB03', 7, 7, 'Practical', 7, '2024-09-21', '08:00:00', '12:00:00', 4.00),
('D', 'AMP01', 5, 5, 'Lecture', 5, '2024-09-22', '09:00:00', '11:00:00', 2.00),
('B', '102', 6, 6, 'Tutorial', 6, '2024-09-23', '14:30:00', '16:00:00', 1.50),
('A', '101', 8, 8, 'Lecture', 8, '2024-09-24', '11:00:00', '13:00:00', 2.00);



-- Scenario 1: Student with FAILING grade (< 10/20)
-- Student: Boudiaf Rayan (ID=3) fails Network Security (Course 1)
INSERT INTO Grade (Student_ID, Course_ID, Department_ID, Exam_ID, Semester_ID, Grade_Type, Grade_Date, Grade_Source, Grade_Value, Max_Points, Comments) VALUES
(3, 1, 1, 1, 3, 'Midterm', '2024-11-20', 'Exam', 8.00, 20.00, 'Needs improvement in firewall configuration'),
(3, 1, 1, 2, 3, 'Final', '2025-01-20', 'Exam', 10.00, 30.00, 'Slightly better but still below passing'),
(3, 1, 1, NULL, 3, 'Quiz', '2024-10-10', 'Other', 4.00, 10.00, 'Struggled with basic concepts'),
(3, 1, 1, NULL, 3, 'Assignment', '2024-10-20', 'Other', 6.00, 20.00, 'Incomplete submission');
-- Total for Student 3: (8/20)*20*0.3 + (10/30)*20*0.4 + (4/10)*20*0.1 + (6/20)*20*0.1 = 2.4 + 2.67 + 0.8 + 0.6 = 6.47/20 (FAILING)

-- Scenario 2: Student with RESIT ELIGIBLE grade (8-9.99/20)
-- Student: Mokhtar Amine (ID=5) gets 8.5/20 in Network Security
INSERT INTO Grade (Student_ID, Course_ID, Department_ID, Exam_ID, Semester_ID, Grade_Type, Grade_Date, Grade_Source, Grade_Value, Max_Points, Comments) VALUES
(5, 1, 1, 1, 3, 'Midterm', '2024-11-20', 'Exam', 10.00, 20.00, 'Borderline performance'),
(5, 1, 1, 2, 3, 'Final', '2025-01-20', 'Exam', 18.00, 30.00, 'Good improvement in final'),
(5, 1, 1, NULL, 3, 'Quiz', '2024-10-10', 'Other', 6.00, 10.00, 'Average quiz result'),
(5, 1, 1, NULL, 3, 'Assignment', '2024-10-20', 'Other', 10.00, 20.00, 'Decent assignment');
-- Total: (10/20)*20*0.3 + (18/30)*20*0.4 + (6/10)*20*0.1 + (10/20)*20*0.1 = 3.0 + 4.8 + 1.2 + 1.0 = 10.0/20 (RESIT - but we'll mark as Resit Eligible in enrollment)

-- Actually, let's make this one truly resit eligible (8-9.99):
UPDATE Grade SET Grade_Value = 16.00 WHERE Student_ID = 5 AND Course_ID = 1 AND Exam_ID = 2;
-- New total: 3.0 + 4.27 + 1.2 + 1.0 = 9.47/20 (RESIT ELIGIBLE)

-- Mark student as Resit Eligible in Enrollment
UPDATE Enrollment SET Status = 'Resit Eligible' WHERE Student_ID = 5 AND Course_ID = 1 AND Department_ID = 1;

-- Scenario 3: Student EXCLUDED from module
-- Student: Rahmouni Salma (ID=6) is excluded due to attendance/disciplinary issues
UPDATE Enrollment SET Status = 'Excluded' WHERE Student_ID = 6 AND Course_ID = 5 AND Department_ID = 5;

-- Scenario 4: More grades for DISQUALIFYING MARKS test
-- Add grades for students to create average disparity
-- Student: Khelifi Amina (ID=2) - Below average performance
INSERT INTO Grade (Student_ID, Course_ID, Department_ID, Exam_ID, Semester_ID, Grade_Type, Grade_Date, Grade_Source, Grade_Value, Max_Points, Comments) VALUES
(2, 2, 2, 3, 3, 'Midterm', '2024-11-21', 'Exam', 10.00, 20.00, 'Needs more cryptography practice'),
(2, 2, 2, NULL, 3, 'Quiz', '2024-10-15', 'Other', 5.00, 10.00, 'Weak on RSA concepts'),
(2, 2, 2, NULL, 3, 'Assignment', '2024-10-25', 'Other', 12.00, 20.00, 'Good effort on implementation'),
(2, 2, 2, NULL, 3, 'Final', '2025-01-25', 'Other', 18.00, 30.00, 'Improved in final exam');
-- Total: (10/20)*20*0.3 + (5/10)*20*0.1 + (12/20)*20*0.1 + (18/30)*20*0.4 = 3.0 + 1.0 + 1.2 + 4.8 = 10.0/20

-- Student: Benali Yacine (ID=1) - High performer (increases promo average)
-- Already has 16.50/20 on Network Security midterm
INSERT INTO Grade (Student_ID, Course_ID, Department_ID, Exam_ID, Semester_ID, Grade_Type, Grade_Date, Grade_Source, Grade_Value, Max_Points, Comments) VALUES
(1, 2, 2, 3, 3, 'Midterm', '2024-11-21', 'Exam', 18.00, 20.00, 'Excellent cryptographic analysis'),
(1, 2, 2, NULL, 3, 'Quiz', '2024-10-15', 'Other', 9.00, 10.00, 'Strong RSA understanding'),
(1, 2, 2, NULL, 3, 'Assignment', '2024-10-25', 'Other', 18.00, 20.00, 'Perfect implementation'),
(1, 2, 2, NULL, 3, 'Final', '2025-01-25', 'Other', 28.00, 30.00, 'Outstanding final performance');
-- Total: (18/20)*20*0.3 + (9/10)*20*0.1 + (18/20)*20*0.1 + (28/30)*20*0.4 = 5.4 + 1.8 + 1.8 + 7.47 = 16.47/20

-- Now Cryptography Course (ID=2) will have:
-- Student 1: 16.47/20
-- Student 2: 10.0/20
-- Student 3 (already exists): 18.00/20
-- Promo average: (16.47 + 10.0 + 18.0) / 3 = 14.82
-- 60% of promo: 14.82 * 0.6 = 8.89
-- Student 2 (10.0) is NOT disqualified (10.0 > 8.89)
-- Let's add a truly disqualified student:

-- Student: Zerrouki Yasmine (ID=7) - DISQUALIFIED (way below promo average)
INSERT INTO Grade (Student_ID, Course_ID, Department_ID, Exam_ID, Semester_ID, Grade_Type, Grade_Date, Grade_Source, Grade_Value, Max_Points, Comments) VALUES
(7, 2, 2, 3, 3, 'Midterm', '2024-11-21', 'Exam', 6.00, 20.00, 'Critical gaps in understanding'),
(7, 2, 2, NULL, 3, 'Quiz', '2024-10-15', 'Other', 3.00, 10.00, 'Very weak performance'),
(7, 2, 2, NULL, 3, 'Assignment', '2024-10-25', 'Other', 8.00, 20.00, 'Minimal effort'),
(7, 2, 2, NULL, 3, 'Final', '2025-01-25', 'Other', 12.00, 30.00, 'Still struggling');
-- Total: (6/20)*20*0.3 + (3/10)*20*0.1 + (8/20)*20*0.1 + (12/30)*20*0.4 = 1.8 + 0.6 + 0.8 + 3.2 = 6.4/20
-- 6.4 < 8.89 (60% of promo) -> DISQUALIFIED!

-- Need to enroll student 7 in Cryptography first
INSERT INTO Enrollment (Student_ID, Course_ID, Department_ID, Semester_ID, Status) VALUES
(7, 2, 2, 3, 'Enrolled');

-- Scenario 5: Average marks by GROUP
-- Add more students to different groups with different performance levels

-- Student: Lahlou Mehdi (ID=8) in Group 1 - High performer
INSERT INTO Grade (Student_ID, Course_ID, Department_ID, Exam_ID, Semester_ID, Grade_Type, Grade_Date, Grade_Source, Grade_Value, Max_Points, Comments) VALUES
(8, 1, 1, 1, 3, 'Midterm', '2024-11-20', 'Exam', 17.00, 20.00, 'Excellent network analysis'),
(8, 1, 1, 2, 3, 'Final', '2025-01-20', 'Exam', 26.00, 30.00, 'Outstanding final exam'),
(8, 1, 1, NULL, 3, 'Quiz', '2024-10-10', 'Other', 9.00, 10.00, 'Strong quiz performance'),
(8, 1, 1, NULL, 3, 'Assignment', '2024-10-20', 'Other', 18.00, 20.00, 'Thorough assignment');
-- Total: (17/20)*20*0.3 + (26/30)*20*0.4 + (9/10)*20*0.1 + (18/20)*20*0.1 = 5.1 + 6.93 + 1.8 + 1.8 = 15.63/20

-- Student: Bouzidi Nour (ID=9) in Group 1 - Medium performer
INSERT INTO Grade (Student_ID, Course_ID, Department_ID, Exam_ID, Semester_ID, Grade_Type, Grade_Date, Grade_Source, Grade_Value, Max_Points, Comments) VALUES
(9, 1, 1, 1, 3, 'Midterm', '2024-11-20', 'Exam', 12.00, 20.00, 'Average performance'),
(9, 1, 1, 2, 3, 'Final', '2025-01-20', 'Exam', 20.00, 30.00, 'Solid final exam'),
(9, 1, 1, NULL, 3, 'Quiz', '2024-10-10', 'Other', 7.00, 10.00, 'Decent quiz result'),
(9, 1, 1, NULL, 3, 'Assignment', '2024-10-20', 'Other', 14.00, 20.00, 'Good assignment');
-- Total: (12/20)*20*0.3 + (20/30)*20*0.4 + (7/10)*20*0.1 + (14/20)*20*0.1 = 3.6 + 5.33 + 1.4 + 1.4 = 11.73/20

-- Need enrollments for students 8 and 9
INSERT INTO Enrollment (Student_ID, Course_ID, Department_ID, Semester_ID, Status) VALUES
(8, 1, 1, 3, 'Enrolled'),
(9, 1, 1, 3, 'Enrolled');

-- Now Group 1 for Network Security Course has:
-- Student 1 (Benali): 16.50/20 (from original data)
-- Student 2 (Khelifi): 14.00/20 (from original data)
-- Student 8 (Lahlou): 15.63/20
-- Student 9 (Bouzidi): 11.73/20
-- Group 1 Average: (16.50 + 14.00 + 15.63 + 11.73) / 4 = 14.47/20

-- Add Group 2 students with different average
-- Student: Mebarki Karim (ID=7, but he's in Group 7... let's check)
-- Actually students 7-10 are in groups 7-10, so they're not comparable
-- Let's add grades for students in Group 2 (student ID 3)

-- Student 3 (Boudiaf) is in Group 2 and already failing with 6.47/20

-- Scenario 6: Students who PASSED the semester
-- Add complete grade sets for semester calculation
-- Student 1 needs grades in multiple courses for semester 3

-- Student 1 in Digital Forensics (Course 3)
INSERT INTO Enrollment (Student_ID, Course_ID, Department_ID, Semester_ID, Status) VALUES
(1, 3, 3, 3, 'Enrolled');

INSERT INTO Grade (Student_ID, Course_ID, Department_ID, Exam_ID, Semester_ID, Grade_Type, Grade_Date, Grade_Source, Grade_Value, Max_Points, Comments) VALUES
(1, 3, 3, NULL, 3, 'Midterm', '2024-11-22', 'Other', 16.00, 20.00, 'Strong forensic analysis'),
(1, 3, 3, NULL, 3, 'Quiz', '2024-10-18', 'Other', 8.00, 10.00, 'Good understanding'),
(1, 3, 3, NULL, 3, 'Assignment', '2024-11-05', 'Other', 17.00, 20.00, 'Excellent lab work'),
(1, 3, 3, NULL, 3, 'Final', '2025-01-23', 'Other', 27.00, 30.00, 'Outstanding investigation');
-- Total: (16/20)*20*0.3 + (8/10)*20*0.1 + (17/20)*20*0.1 + (27/30)*20*0.4 = 4.8 + 1.6 + 1.7 + 7.2 = 15.3/20

-- Now Student 1 in Semester 3 has:
-- Network Security (already enrolled): Not enough grades yet, add them
INSERT INTO Grade (Student_ID, Course_ID, Department_ID, Exam_ID, Semester_ID, Grade_Type, Grade_Date, Grade_Source, Grade_Value, Max_Points, Comments) VALUES
(1, 1, 1, 2, 3, 'Final', '2025-01-20', 'Exam', 28.00, 30.00, 'Excellent comprehensive exam'),
(1, 1, 1, NULL, 3, 'Quiz', '2024-10-10', 'Other', 9.00, 10.00, 'Strong fundamentals'),
(1, 1, 1, NULL, 3, 'Assignment', '2024-10-20', 'Other', 18.00, 20.00, 'Thorough network analysis');
-- Total for Course 1: (16.5/20)*20*0.3 + (28/30)*20*0.4 + (9/10)*20*0.1 + (18/20)*20*0.1 = 4.95 + 7.47 + 1.8 + 1.8 = 16.02/20

-- Cryptography (Course 2): 16.47/20 (calculated above)
-- Digital Forensics (Course 3): 15.3/20 (calculated above)
-- Semester 3 Average for Student 1: (16.02 + 16.47 + 15.3) / 3 = 15.93/20 -> PASSED!
