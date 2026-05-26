# ЛитВечер — Платформа для организации литературных вечеров онлайн

## Запуск проекта

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Тестовые данные
- Логин: admin / admin123
- Логин: reader / reader123

## Структура
- events/ — приложение мероприятий (модели, представления, формы)
- accounts/ — аутентификация и профили
- templates/ — HTML-шаблоны
- static/ — CSS и JS
