-- Insert Course
INSERT INTO COURSES (COURSE_CODE, COURSE_TITLE) VALUES
('CS101', 'Computer Programming with Python');

-- Insert Lab Tasks for the Course
INSERT INTO LAB_TASK (COURSE_CODE, LAB_NO, LAB_TITLE) VALUES
('CS101', 1, 'Variables and Data Types'),
('CS101', 2, 'Control Flow and Loops'),
('CS101', 3, 'Functions and Modules'),
('CS101', 4, 'File Handling'),
('CS101', 5, 'Object-Oriented Programming');

-- Insert Lab Info
INSERT INTO LAB_INFO (LAB_TITLE, DEADLINE) VALUES
('Variables and Data Types', '2025-04-10'),
('Control Flow and Loops', '2025-04-17'),
('Functions and Modules', '2025-04-24'),
('File Handling', '2025-05-01'),
('Object-Oriented Programming', '2025-05-08');

-- Insert Questions for Lab #1 (Variables and Data Types)
INSERT INTO QUESTION (COURSE_CODE, LAB_NO, TASK_NO, QUESTION_TEXT) VALUES
('CS101', 1, 1, 'How do you declare a variable in Python?'),
('CS101', 1, 2, 'What are the different data types available in Python?'),
('CS101', 1, 3, 'How can you perform type conversion in Python?'),
('CS101', 1, 4, 'What is the difference between mutable and immutable data types in Python?'),
('CS101', 1, 5, 'Write a Python program to swap two variables without using a third variable.');

-- Insert Questions for Lab #2 (Control Flow and Loops)
INSERT INTO QUESTION (COURSE_CODE, LAB_NO, TASK_NO, QUESTION_TEXT) VALUES
('CS101', 2, 1, 'What is the difference between "if", "elif", and "else" statements?'),
('CS101', 2, 2, 'How do you implement a "for" loop in Python?'),
('CS101', 2, 3, 'Explain the "while" loop with an example.'),
('CS101', 2, 4, 'Write a Python program that prints all even numbers from 1 to 50 using a loop.'),
('CS101', 2, 5, 'Write a Python program that calculates the sum of all numbers in a given list.');

-- Insert Questions for Lab #3 (Functions and Modules)
INSERT INTO QUESTION (COURSE_CODE, LAB_NO, TASK_NO, QUESTION_TEXT) VALUES
('CS101', 3, 1, 'How do you define a function in Python?'),
('CS101', 3, 2, 'What is the difference between arguments and parameters?'),
('CS101', 3, 3, 'Explain the concept of recursion with an example.'),
('CS101', 3, 4, 'Write a Python function that takes a list of numbers as input and returns their average.'),
('CS101', 3, 5, 'Write a Python function that checks whether a given number is prime or not.');

-- Insert Questions for Lab #4 (File Handling)
INSERT INTO QUESTION (COURSE_CODE, LAB_NO, TASK_NO, QUESTION_TEXT) VALUES
('CS101', 4, 1, 'How do you open a file in Python?'),
('CS101', 4, 2, 'What are the different file modes available in Python?'),
('CS101', 4, 3, 'How do you read and write to a file in Python?'),
('CS101', 4, 4, 'Write a Python program that reads a text file and counts the number of words in it.'),
('CS101', 4, 5, 'Write a Python program that appends user input to an existing text file.');

-- Insert Questions for Lab #5 (Object-Oriented Programming)
INSERT INTO QUESTION (COURSE_CODE, LAB_NO, TASK_NO, QUESTION_TEXT) VALUES
('CS101', 5, 1, 'What is a class in Python? How do you define one?'),
('CS101', 5, 2, 'What is the difference between instance and class variables?'),
('CS101', 5, 3, 'Explain the concept of inheritance with an example.'),
('CS101', 5, 4, 'Write a Python class named "Car" with attributes make, model, and year, and a method to display car details.'),
('CS101', 5, 5, 'Write a Python program that demonstrates method overriding in inheritance.');
