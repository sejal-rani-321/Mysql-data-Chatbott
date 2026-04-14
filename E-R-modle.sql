
    -- CREATE DATABASE loanDatabase;
    -- USE loanDatabase;
-- 1. CLEANUP (Optional: Remove existing tables to start fresh)
DROP TABLE IF EXISTS Combined_Loan_Data;
DROP TABLE IF EXISTS Loan;
DROP TABLE IF EXISTS Customer;

-- 2. CREATE TABLES
-- Strong Entity
CREATE TABLE Customer (
    C_id INT PRIMARY KEY,
    C_name VARCHAR(100)
);

-- Weak Entity (Depends on Customer)
CREATE TABLE Loan (
    C_id INT,
    L_name VARCHAR(100),
    L_date DATE,
    PRIMARY KEY (C_id, L_name),
    FOREIGN KEY (C_id) REFERENCES Customer(C_id)
);

-- 3. INSERT 12 ROWS OF DATA
INSERT INTO Customer (C_id, C_name) VALUES 
(1, 'Alice'), (2, 'Bob'), (3, 'Charlie'), (4, 'David'), 
(5, 'Eve'), (6, 'Frank'), (7, 'Grace'), (8, 'Heidi'), 
(9, 'Ivan'), (10, 'Judy'), (11, 'Karl'), (12, 'Leo');

INSERT INTO Loan (C_id, L_name, L_date) VALUES 
(1, 'Home Loan', '2024-01-01'), (2, 'Car Loan', '2024-01-05'),
(3, 'Education', '2024-01-10'), (4, 'Personal', '2024-01-15'),
(5, 'Business', '2024-02-01'), (6, 'Home Loan', '2024-02-05'),
(7, 'Car Loan', '2024-02-10'), (8, 'Education', '2024-02-15'),
(9, 'Personal', '2024-03-01'), (10, 'Business', '2024-03-05'),
(11, 'Home Loan', '2024-03-10'), (12, 'Car Loan', '2024-03-15');

-- 4. COMBINE AND STORE IN A NEW TABLE
CREATE TABLE Combined_Loan_Data AS 
SELECT  C.C_id, 
    C.C_name, 
    L.L_name, 
    L.L_date
FROM Customer C
JOIN Loan L ON C.C_id = L.C_id;

-- 5. VIEW FINAL TABLE
SELECT * FROM Combined_Loan_Data;


CREATE TABLE rag_documents AS  
SELECT 
    CONCAT('Customer ', C_name, ' (ID: ', C_id, ') holds a ', L_name, ' issued on ', L_date, '.') AS Row_As_Text
FROM Combined_Loan_Data