-- Вставка категорий (если их ещё нет)
INSERT INTO "Categories" (id, type, name) VALUES
(1, 'work', 'Работа'),
(2, 'study', 'Учёба'),
(3, 'personal', 'Личное')
ON CONFLICT (id) DO NOTHING;

-- Вставка задач (если их ещё нет)
INSERT INTO "Tasks_table" (id, name, pomodoro_count, category_id) VALUES
(1, 'task1', 10, 1),
(2, 'task2', 5, 2),
(3, 'task3', 15, 3);