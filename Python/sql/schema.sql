DROP TABLE IF EXISTS students CASCADE;
DROP TABLE IF EXISTS rooms CASCADE;

CREATE TABLE rooms (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birthday TIMESTAMP NOT NULL,
    sex CHAR(1) NOT NULL CHECK (sex IN ('M', 'F')),
    room_id INTEGER,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE SET NULL
);

COMMENT ON TABLE rooms IS 'List of rooms';
COMMENT ON TABLE students IS 'List of students';
COMMENT ON COLUMN students.room_id IS 'reference column to rooms ttable';

