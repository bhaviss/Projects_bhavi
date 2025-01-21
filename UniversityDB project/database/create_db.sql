-- Create Database
CREATE DATABASE UniversityDB;

-- Use the database
USE UniversityDB;

-- Create table for Students
-- Create table for Students (Ensure the foreign key matches the primary key)
CREATE TABLE Students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_number VARCHAR(20) NOT NULL UNIQUE,
    subject_id INT,
    grade VARCHAR(2),
    FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id)
);


-- Create table for Subjects
CREATE TABLE Subjects (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL
);

-- Create table for Staff
CREATE TABLE Staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    position VARCHAR(100),
    contact_number VARCHAR(20)
);

-- Create table for Hostel Meal Plans
CREATE TABLE HostelMealPlans (
    meal_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    meal_plan VARCHAR(50),
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);
INSERT INTO Subjects (subject_name) VALUES 
('Computer Science'),
('Mechanical Engineering'),
('Electrical Engineering'),
('Civil Engineering'),
('Information Technology');

INSERT INTO Students (name, roll_number, subject_id, grade) VALUES 
('John Doe', 'S001', 1, 'A'),
('Jane Smith', 'S002', 2, 'B'),
('Michael Brown', 'S003', 3, 'C'),
('Emily Clark', 'S004', 4, 'B'),
('Daniel Lee', 'S005', 5, 'A'),
('Sophia White', 'S006', 1, 'A'),
('Liam Harris', 'S007', 2, 'B'),
('Olivia Johnson', 'S008', 3, 'B'),
('James Walker', 'S009', 4, 'C'),
('Isabella Lewis', 'S010', 5, 'A');


INSERT INTO Staff (name, position, contact_number) VALUES 
('Dr. Michael Johnson', 'Professor', '123-456-7890'),
('Ms. Linda Brown', 'Associate Professor', '234-567-8901'),
('Dr. Emily Clark', 'Assistant Professor', '345-678-9012'),
('Mr. Daniel Lee', 'Lecturer', '456-789-0123'),
('Ms. Olivia Harris', 'Lab Assistant', '567-890-1234');


INSERT INTO HostelMealPlans (student_id, meal_plan) VALUES 
(1, 'Vegetarian'),
(2, 'Non-Vegetarian'),
(3, 'Vegan'),
(4, 'Vegetarian'),
(5, 'Non-Vegetarian'),
(6, 'Vegan'),
(7, 'Vegetarian'),
(8, 'Non-Vegetarian'),
(9, 'Vegan'),
(10, 'Vegetarian');


SELECT s.name AS student_name, s.roll_number, su.subject_name, s.grade 
FROM Students s
JOIN Subjects su ON s.subject_id = su.subject_id;


SELECT staff_id, name, position, contact_number FROM Staff;


SELECT st.name AS student_name, mp.meal_plan 
FROM Students st
JOIN HostelMealPlans mp ON st.student_id = mp.student_id;


SELECT name, roll_number, grade 
FROM Students 
WHERE grade = 'A';


SELECT st.name AS student_name, su.subject_name 
FROM Students st
JOIN Subjects su ON st.subject_id = su.subject_id
WHERE su.subject_name = 'Computer Science';


UPDATE Students 
SET grade = 'A' 
WHERE roll_number = 'S003';

UPDATE Staff 
SET position = 'Senior Lecturer' 
WHERE staff_id = 2;


DELETE FROM Staff 
WHERE staff_id = 5;

DELETE FROM HostelMealPlans 
WHERE student_id = 7;


START TRANSACTION;

-- Insert new student
INSERT INTO Students (name, roll_number, subject_id, grade) 
VALUES ('Chris Williams', 'S011', 1, 'A');

-- Insert meal plan for the new student
INSERT INTO HostelMealPlans (student_id, meal_plan) 
VALUES (LAST_INSERT_ID(), 'Non-Vegetarian');

COMMIT;

START TRANSACTION;

-- Insert new student
INSERT INTO Students (name, roll_number, subject_id, grade) 
VALUES ('Mark Taylor', 'S012', 2, 'B');

-- Insert meal plan for the new student (simulate error)
INSERT INTO HostelMealPlans (student_id, meal_plan) 
VALUES (LAST_INSERT_ID(), 'InvalidPlan'); -- This will cause an error

ROLLBACK;
