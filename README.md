# VkAnkiBot
VK bot for checking knowledge of English words.

install

1. установка зависимостей - docker и docker-compose
2. скачать проект c github
```
$ git clone git@github.com:vshagur/VkAnkiBot.git
$ cd VkAnkiBot/
```

первоначальная настрока
$ cat .env-example > .env
откройте файл .env в любом редакторе и установите значения 
переменных окружения - VK_API_KEY и VK_GROUP_ID

cat db/database.env-example > db/database.en
установите значения переменных окружения -POSTGRES_USER,POSTGRES_PASSWORD, POSTGRES_DB

cat server/config/api.yaml-example > server/config/api.yaml
установите значения database, user, password




3. запустить 
```
docker-compose build
```

4. запустить 
```
docker-compose up
```
подключиться к серверу с другого теминала
$ docker-compose exec server /bin/bash
применить миграции 
$ alembic upgrade head
заполнить базу данных
$ python db/db_init.py

