-- Active: 1712417447158@@localhost@33066@inventory

CREATE TABLE inventory_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    order_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    item_id INT,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (item_id) REFERENCES inventory_items(item_id)
);

INSERT INTO inventory_items (name, description, price, quantity, category) 
VALUES 
('Laptop', 'A powerful laptop for everyday use', 999.99, 10, 'Electronics'),
('Headphones', 'High-quality headphones with noise cancellation feature', 149.99, 20, 'Electronics'),
('Backpack', 'A durable backpack with multiple compartments', 49.99, 30, 'Accessories'),
('Smartphone', 'The latest smartphone with advanced features', 699.99, 15, 'Electronics'),
('Water Bottle', 'Stainless steel water bottle, leak-proof', 19.99, 25, 'Accessories');

INSERT INTO orders (customer_name, total_amount, order_date) 
VALUES 
('John Doe', 1149.97, '2024-04-01'),
('Jane Smith', 849.98, '2024-04-02'),
('Alice Johnson', 69.98, '2024-04-03');

INSERT INTO order_items (order_id, item_id, quantity, price) 
VALUES 
(1, 1, 1, 999.99),
(1, 2, 1, 149.99),
(2, 4, 1, 699.99),
(3, 5, 2, 39.98);