create database hms;
use hms;

create table hostels(
hostel_id int AUTO_INCREMENT,
hostel_name varchar(255) not null,
description text not null,
img varchar(100) not null,
primary key(hostel_id)
);

create table beds(
beds_id varchar(20),
bednum int not null,
price int not null,
hostel_id int not null,
primary key(beds_id),
foreign key(hostel_id) references hostels(hostel_id)
);

create table rooms(
roomnum varchar(100),
beds varchar(20) not null, 
price int not null,
hostel_id int not null,
room_gen varchar(11) not null,
primary key(roomnum),
foreign key(hostel_id) references hostels(hostel_id),
foreign key(beds) references beds(beds_id)
);

create table users(
id int AUTO_INCREMENT,
firstname varchar(50) not null,
lastname varchar(50) not null,
email varchar(120) not null,
number varchar(20) not null,
gender varchar(11) not null,
role varchar(10) default "student",
password varchar(60) not null,
hostel_id int,
room_id varchar(100),
primary key(id),
foreign key(hostel_id) references hostels(hostel_id),
foreign key(room_id) references rooms(roomnum)
);

create table payments(
payment_id int not null AUTO_INCREMENT,
user_id int,
amount_paid int not null,
amount_remaining int not null,
primary key(payment_id),
foreign key(user_id) references users(id)
);

create table images(
image_id int AUTO_INCREMENT,
image_file varchar(100),
date_posted datetime default CURRENT_TIMESTAMP,
processed varchar(10) default "False",
user_id int,
primary key(image_id),
foreign key(user_id) references users(id)
);

create table announcements(
id int AUTO_INCREMENT,
subject varchar(100) not null,
date_posted datetime default CURRENT_TIMESTAMP,
message text,
user_id int,
primary key(id),
foreign key(user_id) references users(id)
);

insert into hostels (hostel_name,description,img) values('Hosanna','This is the hostels description','static/hostel_pics/hosanna.jpg');
insert into hostels (hostel_name,description,img) values('Masere','This is the hostels description','static/hostel_pics/hosanna.jpg');
insert into hostels (hostel_name,description,img) values('Columbiana','This is the hostels description','static/hostel_pics/hosanna.jpg');
insert into hostels (hostel_name,description,img) values('Charlotte','This is the hostels description','static/hostel_pics/hosanna.jpg');
insert into hostels (hostel_name,description,img) values('Tanko','This is the hostels description','static/hostel_pics/hosanna.jpg');
insert into hostels (hostel_name,description,img) values('Dufie','This is the hostels description','static/hostel_pics/hosanna.jpg');

select * from hostels;
select * from users;

UPDATE users
SET role = 'admin'
WHERE lastname = "Hostel";

/*ALTER TABLE hostels CHANGE description desc text not null;*/

drop table hostels;
ALTER TABLE rooms
CHANGE COLUMN room_num room_num varchar(100);

select * from rooms;
