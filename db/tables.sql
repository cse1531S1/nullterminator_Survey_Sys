create table enrolments (
    user_id int NOT NULL,
    course_code char(8) NOT NULL,
    course_year char(4) NOT NULL
    -- unique(user_id,course_code,course_year)
);

create table users (
    user_id int primary key,
    user_name varchar(20) NOT NULL,
    password varchar(255) NOT NULL,
    -- use the unique to let the update work
    -- because the update method must have unique constrain
    -- then the database won't throw an error
    unique(user_id)
);

create table course(
    course_code char(8) NOT NULL,
    course_year char(4) NOT NULL,
    unique(course_code,course_year)
);
