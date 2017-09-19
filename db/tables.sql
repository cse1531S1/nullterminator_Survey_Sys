create table enrolments (
    user_id int NOT NULL,
    course_code char(8) NOT NULL,
    course_year char(4) NOT NULL
);


create table users (
    user_id int primary key,
    user_name varchar(20) NOT NULL,
    password varchar(255) NOT NULL

);


create table course(
    course_code char(8) NOT NULL,
    course_year char(4) NOT NULL

);
