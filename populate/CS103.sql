-- Insert Course
INSERT INTO COURSES (COURSE_CODE, COURSE_TITLE) VALUES
('CS103', 'Data Structures and Algorithms with Python');

-- Insert Lab Tasks for CS103
INSERT INTO LAB_TASK (COURSE_CODE, LAB_NO, LAB_TITLE) VALUES
('CS103', 1, 'Lists, Stacks, and Queues'),
('CS103', 2, 'Linked Lists'),
('CS103', 3, 'Recursion and Sorting Algorithms'),
('CS103', 4, 'Trees and Graphs'),
('CS103', 5, 'Hashing and Searching Algorithms');

-- Insert Lab Info for CS103
INSERT INTO LAB_INFO (LAB_TITLE, DEADLINE) VALUES
('Lists, Stacks, and Queues', '2025-04-10'),
('Linked Lists', '2025-04-17'),
('Recursion and Sorting Algorithms', '2025-04-24'),
('Trees and Graphs', '2025-05-01'),
('Hashing and Searching Algorithms', '2025-05-08');

-- Insert Questions for Lab #1 (Lists, Stacks, and Queues)
INSERT INTO QUESTION (COURSE_CODE, LAB_NO, TASK_NO, QUESTION_TEXT) VALUES
('CS103', 1, 1, 'What is the difference between a list, stack, and queue in Python?'),
('CS103', 1, 2, 'How do you implement a stack using Python lists? Provide an example.'),
('CS103', 1, 3, 'Write a Python program to implement a queue using collections.deque.'),
('CS103', 1, 4, 'How does a stack operate in Last-In-First-Out (LIFO) order?'),
('CS103', 1, 5, 'Implement a function to reverse a string using a stack.');

-- Insert Questions for Lab #2 (Linked Lists)
INSERT INTO QUESTION (COURSE_CODE, LAB_NO, TASK_NO, QUESTION_TEXT) VALUES
('CS103', 2, 1, 'What is a linked list, and how is it different from an array?'),
('CS103', 2, 2, 'Write a Python class for a singly linked list with insertion and deletion methods.'),
('CS103', 2, 3, 'How do you traverse a linked list and print all its elements?'),
('CS103', 2, 4, 'Write a function to detect a cycle in a linked list using Floyd’s Cycle Detection Algorithm.'),
('CS103', 2, 5, 'Implement a function to reverse a singly linked list.');

-- Insert Questions for Lab #3 (Recursion and Sorting Algorithms)
INSERT INTO QUESTION (COURSE_CODE, LAB_NO, TASK_NO, QUESTION_TEXT) VALUES
('CS103', 3, 1, 'What is recursion in Python? Give an example.'),
('CS103', 3, 2, 'Explain the base case and recursive case in recursion.'),
('CS103', 3, 3, 'Write a recursive Python function to compute the factorial of a number.'),
('CS103', 3, 4, 'Write a Python function to implement the QuickSort algorithm.'),
('CS103', 3, 5, 'Implement the MergeSort algorithm and explain its time complexity.');

-- Insert Questions for Lab #4 (Trees and Graphs)
INSERT INTO QUESTION (COURSE_CODE, LAB_NO, TASK_NO, QUESTION_TEXT) VALUES
('CS103', 4, 1, 'What is a binary tree? How is it different from a binary search tree?'),
('CS103', 4, 2, 'Write a Python class to implement a binary search tree with insertion and search methods.'),
('CS103', 4, 3, 'How do you perform an in-order traversal of a binary tree?'),
('CS103', 4, 4, 'What is the difference between DFS and BFS in graph traversal?'),
('CS103', 4, 5, 'Write a Python function to perform BFS traversal on a graph.');

-- Insert Questions for Lab #5 (Hashing and Searching Algorithms)
INSERT INTO QUESTION (COURSE_CODE, LAB_NO, TASK_NO, QUESTION_TEXT) VALUES
('CS103', 5, 1, 'What is hashing, and how does a hash table work?'),
('CS103', 5, 2, 'Explain the concept of collisions in hashing and how they are handled.'),
('CS103', 5, 3, 'Write a Python function to implement linear search and binary search.'),
('CS103', 5, 4, 'How do you implement a hash table using Python’s dictionary?'),
('CS103', 5, 5, 'Write a Python function to implement a simple hash function and handle collisions using chaining.');
