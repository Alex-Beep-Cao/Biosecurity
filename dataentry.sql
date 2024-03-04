Insert into position_type
 values
 (1, 'apiarist'),
 (2, 'staff'),
 (3, 'admin');

Insert into apiarist 
values
(NULL, 'alex_cao_a', 'alex', 'cao', 'alex', '111 queen street', 'alex.cao@lincolnuni.ac.nz', '022-0101001', '2024-01-01', true, 1),
(NULL, 'alex_cao_b', 'alex', 'cao', 'alex', '111 queen street', 'alex.cao@lincolnuni.ac.nz', '022-0101001', '2024-01-01', true, 1);

Insert into users 
values
(1,'alex_cao_a', 'f001722cdd7f9371daedf315af63a5ffed19ea84a3788bbe7e7069c3ae11f4d0', 'alex.cao@lincolnuni.ac.nz', 1);
Insert into users 
values
(2,'alex_cao_b', 'f001722cdd7f9371daedf315af63a5ffed19ea84a3788bbe7e7069c3ae11f4d0', 'alex.cao@lincolnuni.ac.nz', 1);

select * from  apiarist ;
select * from  users ;
select * from  employee ;


Insert into employee 
values
(NULL, 'ac_staff_1','alex', 'cao', '123',  'alex.cao@lincolnuni.ac.nz', '022-0101001', '2024-01-01', 'Teach', true , 2),
(NULL, 'ac_admin_1','alex', 'cao', '123',  'alex.cao@lincolnuni.ac.nz', '022-0101001', '2024-01-01', 'Teach', true , 3);
Insert into users 
values
(1,'ac_staff_1', 'd9508122cd143d69df229bf3624b7bcb2b8ac81ed210a0c926455ef119c12abd', 'alex.cao@lincolnuni.ac.nz', 2),
(1,'ac_admin_1', 'd9508122cd143d69df229bf3624b7bcb2b8ac81ed210a0c926455ef119c12abd', 'alex.cao@lincolnuni.ac.nz', 3);

insert into item_type
values
(1, 'pest'),
(2, 'disease');

INSERT INTO bee (bee_id, item_type_id, present_in_NZ, common_name, scientific_name, key_characteristics, biology, symptoms, image_id)
VALUES(NULL, 1, true, 'Healthy brood', 'Healthy brood', 'Uniformly laid eggs, pearly white larvae, solid unperforated cappings.',
'Eggs hatch in 3 days, larvae undergo 5 stages over 6 days, pupation varies by caste.', 'Uniform brood pattern, absence of diseases and pests, vibrant white larvae.', 1 );

INSERT INTO bee (bee_id, item_type_id, present_in_NZ, common_name, scientific_name, key_characteristics, biology, symptoms, image_id)
VALUES(NULL, 2, true, 'European Foulbrood', 'Melissococcus plutoniusd', 'Bacteria infects bee larvae before cell capping, disrupting their digestion.',
'Spread through feeding, affects young larval stages, thrives in unhygienic conditions.', 'Uneven or sunken cappings, yellowish to brown discolored larvae, twisted larvae at the bottom of cells, foul smell.', 2 );

select * from bee;
select * from image;
select * from item_type;
