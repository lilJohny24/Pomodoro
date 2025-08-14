from schema.category import Category
tasks = [
    {
        "id": 1,
        "name": "Прочитать документацию FastAPI",
        "pomodoro_count": 10,
        "category_id": 1
    },
    {
        "id": 2,
        "name": "Написать парсер для сайта",
        "pomodoro_count": 10,
        "category_id": 2
    },
    {
        "id": 3,
        "name": "Рефакторинг кода",
        "pomodoro_count": 10,
        "category_id": 3
    },
    {
        "id": 4,
        "name": "Протестировать новые фичи",
        "pomodoro_count": 10,
        "category_id": 4
    },
    {
        "id": 5,
        "name": "Оптимизировать SQL-запросы",
        "pomodoro_count": 10,
        "category_id": 5
    }
]

categories = [
    Category(id=1, name="Работа"),
    Category(id=2, name="Учеба"),
    Category(id=3, name='Прогулка'),
    Category(id=4, name='Чтение'),
    Category(id=5, name='Сон')
]