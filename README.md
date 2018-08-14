API для таск менеджера.
Проект висит на 7777 порту
Авторизация через jwt, т.е. в header запароса добавляем запись Authorization: JWT <token>
Токен можно получить Post запросом на /api/token-auth, отправив json вида: {"username": <username>, "password": <password>}

Собрать образ:
docker build -t task_manager .

Запуск контейнера:
docker-compose up