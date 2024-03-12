Insert into position_type
 values
 (1, 'apiarist'),
 (2, 'staff'),
 (3, 'admin');

Insert into apiarist 
values
(NULL, 'alex_cao_a', 'alex', 'cao', 'alex', '111 queen street', 'alex.cao@lincolnuni.ac.nz', '022-0101001', '2024-01-01', true, 1),
(NULL, 'alex_cao_b', 'alex', 'cao', 'alex', '111 queen street', 'alex.cao@lincolnuni.ac.nz', '022-0101001', '2024-01-01', true, 1),
(NULL, 'alex_cao_c', 'alex', 'cao', 'alex', '111 queen street', 'alex.cao@lincolnuni.ac.nz', '022-0101001', '2024-01-01', true, 1),
(NULL, 'alex_cao_d', 'alex', 'cao', 'alex', '111 queen street', 'alex.cao@lincolnuni.ac.nz', '022-0101001', '2024-01-01', true, 1),
(NULL, 'alex_cao_e', 'alex', 'cao', 'alex', '111 queen street', 'alex.cao@lincolnuni.ac.nz', '022-0101001', '2024-01-01', true, 1);

Insert into users 
values
(1,'alex_cao_a', 'f001722cdd7f9371daedf315af63a5ffed19ea84a3788bbe7e7069c3ae11f4d0', 'alex.cao@lincolnuni.ac.nz', 1),
(2,'alex_cao_b', 'f001722cdd7f9371daedf315af63a5ffed19ea84a3788bbe7e7069c3ae11f4d0', 'alex.cao@lincolnuni.ac.nz', 1),
(3,'alex_cao_c', 'f001722cdd7f9371daedf315af63a5ffed19ea84a3788bbe7e7069c3ae11f4d0', 'alex.cao@lincolnuni.ac.nz', 1),
(4,'alex_cao_d', 'f001722cdd7f9371daedf315af63a5ffed19ea84a3788bbe7e7069c3ae11f4d0', 'alex.cao@lincolnuni.ac.nz', 1),
(5,'alex_cao_e', 'f001722cdd7f9371daedf315af63a5ffed19ea84a3788bbe7e7069c3ae11f4d0', 'alex.cao@lincolnuni.ac.nz', 1);




Insert into employee 
values
(NULL, 'ac_staff_1','alex', 'cao', 'alex',  'alex.cao@lincolnuni.ac.nz', '022-0101001', '2024-01-01', 'Teach', true , 2),
(NULL, 'ac_staff_2','alex', 'cao', 'alex',  'alex.cao@lincolnuni.ac.nz', '022-0101001', '2024-01-01', 'Teach', true , 2),
(NULL, 'ac_staff_3','alex', 'cao', 'alex',  'alex.cao@lincolnuni.ac.nz', '022-0101001', '2024-01-01', 'Teach', true , 2),
(NULL, 'ac_admin_1','alex', 'cao', 'alex',  'alex.cao@lincolnuni.ac.nz', '022-0101001', '2024-01-01', 'Teach', true , 3);

Insert into users 
values
(1,'ac_staff_1', 'f001722cdd7f9371daedf315af63a5ffed19ea84a3788bbe7e7069c3ae11f4d0', 'alex.cao@lincolnuni.ac.nz', 2),
(2,'ac_staff_2', 'f001722cdd7f9371daedf315af63a5ffed19ea84a3788bbe7e7069c3ae11f4d0', 'alex.cao@lincolnuni.ac.nz', 2),
(3,'ac_staff_3', 'f001722cdd7f9371daedf315af63a5ffed19ea84a3788bbe7e7069c3ae11f4d0', 'alex.cao@lincolnuni.ac.nz', 2),
(4,'ac_admin_1', 'f001722cdd7f9371daedf315af63a5ffed19ea84a3788bbe7e7069c3ae11f4d0', 'alex.cao@lincolnuni.ac.nz', 3);


insert into item_type
values
(1, 'pest'),
(2, 'disease');
