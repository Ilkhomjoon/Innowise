-- =====================================================
-- INDEKSLAR - Query Optimizatsiyasi
-- =====================================================

-- 1. Students.room_id ustuniga indeks
-- Sabab: Har bir query da students va rooms ni JOIN qilamiz
-- Bu indeks JOIN operatsiyasini tezlashtiradi
CREATE INDEX IF NOT EXISTS idx_students_room_id 
ON students(room_id);

-- 2. Students.birthday ustuniga indeks
-- Sabab: Yosh hisoblash uchun birthday ustunidan foydalanamiz
-- Query 2 va 3 da AGE() funksiyasini ishlatamiz
CREATE INDEX IF NOT EXISTS idx_students_birthday 
ON students(birthday);

-- 3. Students.sex ustuniga indeks
-- Sabab: Query 4 da jins bo'yicha filtrlash kerak
-- Bu indeks COUNT(DISTINCT sex) ni tezlashtiradi
CREATE INDEX IF NOT EXISTS idx_students_sex 
ON students(sex);

-- 4. Composite indeks (room_id, sex)
-- Sabab: Query 4 da bir vaqtda room_id va sex bo'yicha ishlash kerak
-- Bu indeks mixed gender rooms so'rovini juda tezlashtiradi
CREATE INDEX IF NOT EXISTS idx_students_room_sex 
ON students(room_id, sex);

-- 5. Composite indeks (room_id, birthday)
-- Sabab: Query 2 va 3 da bir vaqtda room_id va birthday kerak
-- Bu indeks yosh hisoblashlarni tezlashtiradi
CREATE INDEX IF NOT EXISTS idx_students_room_birthday 
ON students(room_id, birthday);

-- =====================================================
-- INDEKSLAR HAQIDA STATISTIKA
-- =====================================================

-- Barcha indekslarni ko'rish
SELECT 
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;

-- Indeks o'lchamlarini ko'rish
SELECT
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC;