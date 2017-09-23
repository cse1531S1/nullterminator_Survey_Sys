create table enrolments(
    user_id int NOT NULL,
    course_id int NOT NULL,
    FOREIGN KEY (course_id) REFERENCES course(id),
    -- set up a foreign key
    FOREIGN KEY (user_id) REFERENCES users(id)
);

create table users(
    id int primary key,
    password varchar(93) NOT NULL,
    role     varchar(15) NOT NULL,
    -- use the unique to let the update work
    -- because the update method must have unique constrain
    -- then the database won't throw an error
    unique(id)
);

create table course(
    id INTEGER PRIMARY KEY,
    course_code char(8) NOT NULL,
    course_year char(4) NOT NULL,
    unique(course_code,course_year)
);

create table question(
    -- INTEGER PRIMARY KEY is for auto increament in sqlite3
    id INTEGER PRIMARY KEY,
    question varchar(255) NOT NULL,
    -- record how many time the question have been linked
    link int NOT NULL default 0,
    -- decide whether this question showing to question manage system
    -- every linked question won't be actually deleted in database
    show int NOT NULL default 1,
    pool_id int NOT NULL
);

create table answer(
    id INTEGER PRIMARY KEY,
    q_id int NOT NULL,
    answer int NOT NULL,
    FOREIGN KEY (q_id) REFERENCES question(id)
);

create table survey(
    id INTEGER PRIMARY KEY,
    course_id int NOT NULL,
    q_id varchar(1024) NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    status INTEGER NOT NULL default 0,
    FOREIGN KEY (course_id) REFERENCES course(id)
);
