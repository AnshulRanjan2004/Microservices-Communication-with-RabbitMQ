CREATE USER 'root'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
CREATE DATABASE student_records;
USE student_records;
CREATE TABLE STOCK_ITEMS (ProductID INT PRIMARY KEY AUTO_INCREMENT, ProductName VARCHAR(100), Quantity INT, UnitPrice VARCHAR(10));