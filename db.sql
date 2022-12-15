CREATE USER 'A'@'%' IDENTIFIED BY 'B';
GRANT ALL PRIVILEGES ON *.* to 'A'@'%';

--CREATE DATABASE student;
USE student;
CREATE TABLE students (studentName VARCHAR(255), email VARCHAR(255) NOT NULL, studentID INT NOT NULL AUTO_INCREMENT,
PRIMARY KEY(studentID));

INSERT INTO students (studentName, email) values ("first student", "firststudent@mydomain.ie"); 
INSERT INTO students (studentName, email) values ("second student", "secondstudent@mydomain.ie ");
SELECT * FROM students;
exit;

INSERT INTO students (studentName) values ("first student");
