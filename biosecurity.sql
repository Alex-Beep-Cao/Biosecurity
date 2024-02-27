DROP SCHEMA IF EXISTS biosecurity;
CREATE SCHEMA biosecurity;
USE biosecurity;

CREATE TABLE IF NOT EXISTS item_type
(
item_type_id INT PRIMARY KEY NOT NULL,
item_type_DESC VARCHAR(200) NOT NULL
);

CREATE TABLE IF NOT EXISTS position_type
(
position_type_id INT PRIMARY KEY NOT NULL,
position_type_DESC VARCHAR(200) NOT NULL
);

CREATE TABLE IF NOT EXISTS image
(
image_id INT PRIMARY KEY NOT NULL,
image_path VARCHAR(50) NOT NULL,
primary_image BOOL NOT NULL
);

CREATE TABLE IF NOT EXISTS users
(
user_id INT PRIMARY KEY NOT NULL,
username VARCHAR(25) NOT NULL,
hashed_password VARCHAR(100) NOT NULL,
email VARCHAR(50) NOT NULL,
position_type_id INT NOT NULL
);

CREATE TABLE IF NOT EXISTS apiarist
(
apiarist_id INT auto_increment PRIMARY KEY NOT NULL,
username  VARCHAR(200) NOT NULL,
first_name VARCHAR(25) NOT NULL,
last_name VARCHAR(25) NOT NULL,
plain_password  VARCHAR(100) NOT NULL,
address VARCHAR(50),
email VARCHAR(50) NULL,
phone_number VARCHAR(25),
date_joined DATE,
employee_status BOOL NOT NULL,
position_type_id INT NOT NULL,
FOREIGN KEY (position_type_id) REFERENCES position_type(position_type_id)
ON UPDATE CASCADE
ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS employee
(
employee_id INT auto_increment PRIMARY KEY NOT NULL,
first_name VARCHAR(25) NOT NULL,
last_name VARCHAR(25) NOT NULL,
email VARCHAR(50) NOT NULL,
phone_number VARCHAR(25),
hire_date DATE,
department VARCHAR(25),
employee_status BOOL NOT NULL,
position_type_id INT NOT NULL,
FOREIGN KEY (position_type_id) REFERENCES position_type(position_type_id)
ON UPDATE CASCADE
ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS bee
(
bee_id INT auto_increment PRIMARY KEY NOT NULL,
item_type_id INT NOT NULL,
present_in_NZ BOOL NOT NULL,
common_name VARCHAR(50),
scientific_name VARCHAR(50) NOT NULL,
key_characteristics VARCHAR(200),
biology VARCHAR(200),
symptoms VARCHAR(200),
image_id INT NOT NULL,
FOREIGN KEY (item_type_id) REFERENCES item_type(item_type_id)
ON UPDATE CASCADE
ON DELETE CASCADE,
FOREIGN KEY (image_id) REFERENCES image(image_id)
ON UPDATE CASCADE
ON DELETE CASCADE
);

Insert into position_type
 values
 (1, 'apiarist'),
 (2, 'staff'),
 (3, 'admin');
 
select * from  apiarist ;
Insert into apiarist 
values
(NULL, 'alex_cao_a', 'alex', 'cao', 'alex', '111 queen street', 'alex.cao@lincolnuni.ac.nz', '022-0101001', '2024-01-01', true, 1);

Insert into users 
values
(1,'alex_cao_a', 'f001722cdd7f9371daedf315af63a5ffed19ea84a3788bbe7e7069c3ae11f4d0', 'alex.cao@lincolnuni.ac.nz', 1)




