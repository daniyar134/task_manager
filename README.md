API для таск менеджера.
Проект висит на 7777 порту
Авторизация через jwt, т.е. в header запароса добавляем запись Authorization: JWT <token>
Токен можно получить Post запросом на /api/token-auth, отправив json вида: {"username": <username>, "password": <password>}

Запускать контейнер:
docker-compose up