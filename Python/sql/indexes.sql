CREATE INDEX IF NOT EXISTS idx_students_room_id 
ON students(room_id);

CREATE INDEX IF NOT EXISTS idx_students_birthday 
ON students(birthday);

CREATE INDEX IF NOT EXISTS idx_students_sex 
ON students(sex);

CREATE INDEX IF NOT EXISTS idx_students_room_sex 
ON students(room_id, sex);

CREATE INDEX IF NOT EXISTS idx_students_room_birthday 
ON students(room_id, birthday);

SELECT 
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;

SELECT
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC;