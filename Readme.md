# Сервис управления рассылками, администрирования и получения статистики.

### Проект используется для отправки сообщений по расписанию. С полным администрированием, возможностью использовать несколько рассылок одновременно.

### Запуск проекта:
1. Необходимо установить зависимости для проекта из файла "pyproject.toml".
2. Создайте файл .env и напишите свои данные для настройки проекта. Поля для данных находятся в файле ".env.sample".
3. Создайте базу данных для проекта.
4. Примените миграции к созданной вами базе данных командой "python manage.py migrate".
5. Используйте команду "python manage.py csu" для создания суперпользователя.
6. В проекте используется кеширование, поэтому для работы нужно запустить сервер Redis. Ссылка на инструкцию https://redis.io/docs/latest/develop/.
7. Запустите сервер командой "python manage.py runserver".
8. После создания клиентов и рассылок, используйте команду "python manage.py "runapscheduler".