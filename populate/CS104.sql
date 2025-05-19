-- Insert Course
INSERT INTO COURSES (COURSE_CODE, COURSE_TITLE) VALUES
('CS104', 'Computer Engineering Workshop with C');

-- Insert Lab Tasks for CS104
INSERT INTO LAB_TASK (COURSE_CODE, LAB_NO, LAB_TITLE) VALUES
('CS104', 1, 'Introduction to C Programming and Basic I/O'),
('CS104', 2, 'Control Structures and Functions'),
('CS104', 3, 'Arrays, Pointers, and Strings'),
('CS104', 4, 'Structures, File Handling, and Memory Management'),
('CS104', 5, 'Interfacing C with Hardware (Embedded C Basics)');

-- Insert Lab Info for CS104
INSERT INTO LAB_INFO (LAB_TITLE, DEADLINE) VALUES
('Introduction to C Programming and Basic I/O', '2025-04-10'),
('Control Structures and Functions', '2025-04-17'),
('Arrays, Pointers, and Strings', '2025-04-24'),
('Structures, File Handling, and Memory Management', '2025-05-01'),
('Interfacing C with Hardware (Embedded C Basics)', '2025-05-08');

-- Insert Questions for Lab #1 (Introduction to C Programming and Basic I/O)
INSERT INTO QUESTION (COURSE_CODE, LAB_NO, TASK_NO, QUESTION_TEXT) VALUES
('CS104', 1, 1, 'What are the main features of the C programming language?'),
('CS104', 1, 2, 'Write a C program to print "Hello, World!" to the console.'),
('CS104', 1, 3, 'How do you take user input in C using scanf()? Provide an example.'),
('CS104', 1, 4, 'Explain the purpose of the main() function in a C program.'),
('CS104', 1, 5, 'Write a C program to swap two numbers without using a third variable.');

-- Insert Questions for Lab #2 (Control Structures and Functions)
INSERT INTO QUESTION (COURSE_CODE, LAB_NO, TASK_NO, QUESTION_TEXT) VALUES
('CS104', 2, 1, 'What are the different types of control structures in C?'),
('CS104', 2, 2, 'Write a C program using a switch case to display a day of the week based on user input.'),
('CS104', 2, 3, 'How do you define and call a function in C? Provide an example.'),
('CS104', 2, 4, 'Write a recursive function in C to calculate the factorial of a number.'),
('CS104', 2, 5, 'What is the difference between call by value and call by reference? Explain with an example.');

-- Insert Questions for Lab #3 (Arrays, Pointers, and Strings)
INSERT INTO QUESTION (COURSE_CODE, LAB_NO, TASK_NO, QUESTION_TEXT) VALUES
('CS104', 3, 1, 'How are arrays declared and initialized in C?'),
('CS104', 3, 2, 'Write a C program to find the largest element in an array.'),
('CS104', 3, 3, 'What are pointers in C? Explain with an example.'),
('CS104', 3, 4, 'Write a C program to reverse a string using pointers.'),
('CS104', 3, 5, 'How do you dynamically allocate memory for an array in C?');

-- Insert Questions for Lab #4 (Structures, File Handling, and Memory Management)
INSERT INTO QUESTION (COURSE_CODE, LAB_NO, TASK_NO, QUESTION_TEXT) VALUES
('CS104', 4, 1, 'What is a structure in C, and how is it different from an array?'),
('CS104', 4, 2, 'Write a C program to create and display student records using structures.'),
('CS104', 4, 3, 'How do you read and write data to a file in C? Provide an example.'),
('CS104', 4, 4, 'Write a C program to copy the contents of one file to another.'),
('CS104', 4, 5, 'Explain malloc(), calloc(), and free() functions with examples.');

-- Insert Questions for Lab #5 (Interfacing C with Hardware - Embedded C Basics)
INSERT INTO QUESTION (COURSE_CODE, LAB_NO, TASK_NO, QUESTION_TEXT) VALUES
('CS104', 5, 1, 'What is Embedded C, and how is it different from standard C?'),
('CS104', 5, 2, 'Write a simple Embedded C program to blink an LED on an Arduino board.'),
('CS104', 5, 3, 'How do you use GPIO (General Purpose Input/Output) in Embedded C?'),
('CS104', 5, 4, 'Explain the concept of interrupts in Embedded C with an example.'),
('CS104', 5, 5, 'Write an Embedded C program to read input from a button and control an LED.');
