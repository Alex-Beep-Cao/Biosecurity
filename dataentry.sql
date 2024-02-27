Insert into users 
values
(1,'alex_cao_a', 'f001722cdd7f9371daedf315af63a5ffed19ea84a3788bbe7e7069c3ae11f4d0', 'alex.cao@lincolnuni.ac.nz', 1),
				 
(2, 'alex_cao_s', '4d02d938b685b80130bb05420d9c98e34a31f7c4c6afff956eecc0a996f3d521', 'alex.cao@lincoln.ac.nz', 2),
(3, 'alex_cao_admin', '9e53c15190539c977f4e628a8b9d91c90f932089c83407c4c72c92a5f15700fc', 'alex.cao@lin.ac.nz', 3);


Insert into position_type
 values
 (1, 'apiarist'),
 (2, 'staff'),
 (3, 'admin');
 
 select * from  apiarist ;
Insert into apiarist 
values
(NULL, 'alex_cao_a', 'alex', 'cao', 'alex', '111 queen street', 'alex.cao@lincolnuni.ac.nz', '022-0101001', '2024-01-01', true, 1);
