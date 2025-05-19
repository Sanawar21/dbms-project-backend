-- Insert Course
INSERT INTO COURSES (COURSE_CODE, COURSE_TITLE) VALUES
('CS102', 'Object Oriented Programming with Python');

-- Insert Lab Tasks for CS102
INSERT INTO LAB_TASK (COURSE_CODE, LAB_NO, LAB_TITLE) VALUES
('CS102', 1, 'Introduction to Classes and Objects'),
('CS102', 2, 'Encapsulation and Data Hiding'),
('CS102', 3, 'Inheritance and Polymorphism'),
('CS102', 4, 'Abstract Classes and Interfaces'),
('CS102', 5, 'File Handling with OOP');

-- Insert Lab Info
INSERT INTO LAB_INFO (LAB_TITLE, DEADLINE) VALUES
('Introduction to Classes and Objects', '2025-04-10'),
('Encapsulation and Data Hiding', '2025-04-17'),
('Inheritance and Polymorphism', '2025-04-24'),
('Abstract Classes and Interfaces', '2025-05-01'),
('File Handling with OOP', '2025-05-08');

-- Insert Questions for Lab #1 (Introduction to Classes and Objects)
INSERT INTO QUESTION (COURSE_CODE, LAB_NO, TASK_NO, QUESTION_TEXT) VALUES
('CS102', 1, 1, 'What is an object in Python OOP?'),
('CS102', 1, 2, 'How do you define a class in Python? Provide an example.'),
('CS102', 1, 3, 'How do you create an object from a class?'),
('CS102', 1, 4, 'Write a Python class named "Person" with attributes name and age, and a method to display them.'),
('CS102', 1, 5, 'Write a Python program that creates two instances of the "Person" class and prints their attributes.');

-- Insert Questions for Lab #2 (Encapsulation and Data Hiding)
INSERT INTO QUESTION (COURSE_CODE, LAB_NO, TASK_NO, QUESTION_TEXT) VALUES
('CS102', 2, 1, 'What is encapsulation in Python?'),
('CS102', 2, 2, 'Explain the difference between public, protected, and private attributes in Python.'),
('CS102', 2, 3, 'How do you use getter and setter methods in Python?'),
('CS102', 2, 4, 'Write a Python class "BankAccount" with private attributes balance and account_number. Implement methods to deposit and withdraw money.'),
('CS102', 2, 5, 'Modify the "BankAccount" class to include a getter method for balance and prevent direct access to it.');

-- Insert Questions for Lab #3 (Inheritance and Polymorphism)
INSERT INTO QUESTION (COURSE_CODE, LAB_NO, TASK_NO, QUESTION_TEXT) VALUES
('CS102', 3, 1, 'What is inheritance in Python OOP?'),
('CS102', 3, 2, 'What are the types of inheritance supported in Python?'),
('CS102', 3, 3, 'How does method overriding work in Python?'),
('CS102', 3, 4, 'Write a Python program demonstrating single inheritance with classes "Animal" and "Dog".'),
('CS102', 3, 5, 'Write a Python program demonstrating method overriding with a parent and child class.');

-- Insert Questions for Lab #4 (Abstract Classes and Interfaces)
INSERT INTO QUESTION (COURSE_CODE, LAB_NO, TASK_NO, QUESTION_TEXT) VALUES
('CS102', 4, 1, 'What is an abstract class in Python?'),
('CS102', 4, 2, 'How do you define an abstract class using the abc module?'),
('CS102', 4, 3, 'What is the purpose of an interface in OOP?'),
('CS102', 4, 4, 'Write an abstract class "Shape" with an abstract method "area()" and implement it in subclasses "Circle" and "Rectangle".'),
('CS102', 4, 5, 'Modify the previous program to include a method "perimeter()" in the abstract class and implement it in subclasses.');

-- Insert Questions for Lab #5 (File Handling with OOP)
INSERT INTO QUESTION (COURSE_CODE, LAB_NO, TASK_NO, QUESTION_TEXT) VALUES
('CS102', 5, 1, 'How do you open and read a file in Python?'),
('CS102', 5, 2, 'Explain the difference between "r", "w", and "a" modes in file handling.'),
('CS102', 5, 3, 'How can you store and retrieve objects from a file using pickle in Python?'),
('CS102', 5, 4, 'Write a Python class "Student" that allows writing student records to a file and reading them back.'),
('CS102', 5, 5, 'Modify the "Student" class to allow searching for a student by name in the file.');
