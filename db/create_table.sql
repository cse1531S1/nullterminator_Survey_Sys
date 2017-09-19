create table enrolments (
    user_id int,
    course_code char(8),
    course_year char(4)
);


create table users (
    user_id int primary key,
    user_name varchar(20),
    password varchar(255)

);


create table course(
    course_code char(8),
    course_year char(4)

);
