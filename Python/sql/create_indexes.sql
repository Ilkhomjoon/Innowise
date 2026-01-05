CREATE INDEX IF NOT EXISTS idx_students_room_id ON students(room_id);
CREATE INDEX IF NOT EXISTS idx_students_birthday ON students(birthday);
CREATE INDEX IF NOT EXISTS idx_students_sex ON students(sex);
CREATE INDEX IF NOT EXISTS idx_students_room_sex ON students(room_id, sex);
CREATE INDEX IF NOT EXISTS idx_students_room_birthday ON students(room_id, birthday);