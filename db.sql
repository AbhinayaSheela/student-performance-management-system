CREATE DATABASE student1_db;
USE student1_db;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    subject VARCHAR(100),
    marks FLOAT
);