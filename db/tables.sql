create table enrolments (
    user_id int NOT NULL,
    course_code char(8) NOT NULL,
    course_year char(4) NOT NULL
    -- unique(user_id,course_code,course_year)
);

create table users (
    id int primary key,
    password varchar(93) NOT NULL,
    role     varchar(15) NOT NULL,
    -- use the unique to let the update work
    -- because the update method must have unique constrain
    -- then the database won't throw an error
    unique(id)
);

create table course(
    course_code char(8) NOT NULL,
    course_year char(4) NOT NULL,
    unique(course_code,course_year)
);
