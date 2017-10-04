create table enrolments (
    user_id int NOT NULL,
    course_code char(8) NOT NULL,
    course_year char(4) NOT NULL,
    -- unique(user_id,course_code,course_year)

    -- set up a foreign key
    FOREIGN KEY (user_id) REFERENCES users(id)
);

create table users (
    id INTEGER PRIMARY KEY,
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
    type varchar(10) NOT NULL,
    pool_id int NOT NULL
);

create table answer(
    id INTEGER PRIMARY KEY,
    q_id int NOT NULL,
    answer int NOT NULL,
    FOREIGN KEY (q_id) REFERENCES question(id)
);

-- some test user
INSERT INTO users  (id,password,role) VALUES (2,"tecty","admin");


create table survey(
    id INTEGER PRIMARY KEY,
    course_id int NOT NULL,
    genQ_id varchar(1024) NOT NULL,
    optQ_id varchar(1024) NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    status INTEGER NOT NULL default 0,
    FOREIGN KEY (course_id) REFERENCES course(id)
);

create table respond(
    id INTEGER PRIMARY KEY,
    survey_id INTEGER NOT NULL,
    uid INTEGER NOT NULL,
    FOREIGN KEY (survey_id) REFERENCES survey(id),
    FOREIGN KEY (uid) REFERENCES users(id)
);

create table res_mcq(
    id INTEGER PRIMARY KEY,
    respond_id INTEGER NOT NULL,
    ans_list varchar(1024) NOT NULL,
    FOREIGN KEY (respond_id) REFERENCES respond(id)
);

create table res_text(
    id INTEGER PRIMARY KEY,
    respond_id INTEGER NOT NULL,
    ques_id INTEGER NOT NULL,
    answer varchar(255) NOT NULL,
    FOREIGN KEY (respond_id) REFERENCES respond(id)
);
