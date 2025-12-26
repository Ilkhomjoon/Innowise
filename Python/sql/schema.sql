-- Drop tables if exist (tozalash uchun)
DROP TABLE IF EXISTS students CASCADE;
DROP TABLE IF EXISTS rooms CASCADE;

-- Rooms jadvali yaratish
CREATE TABLE rooms (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Students jadvali yaratish
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birthday TIMESTAMP NOT NULL,
    sex CHAR(1) NOT NULL CHECK (sex IN ('M', 'F')),
    room_id INTEGER,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE SET NULL
);

-- Ma'lumotlarni tekshirish uchun
COMMENT ON TABLE rooms IS 'Xonalar ro''yxati';
COMMENT ON TABLE students IS 'Talabalar ro''yxati';
COMMENT ON COLUMN students.room_id IS 'Talaba yashaydigan xona (rooms jadvaliga bog''lanadi)';

