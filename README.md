# VkAnkiBot
VkAnkiBot - игровой бот для создания викторин в социальной сети "ВКонтакте". 

## DOCUMENTATION


#### Installation
1. Install [docker](https://docs.docker.com/engine/install/) и [docker-compose](https://docs.docker.com/compose/install/) 

2. Clone the project from github and go to the project directory:
```
$ git clone git@github.com:vshagur/VkAnkiBot.git
$ cd VkAnkiBot/
```

3. Creation of settings files from templates.
```
$ cat .env-example > .env
$ cat db/database.env-example > db/database.env
$ cat server/config/api.yaml-example > server/config/api.yaml
```

4. Open the configuration files in your favorite editor and set the values of the environment variables.

Set the values for variables to VK_API_KEY, VK_GROUP_ID in the .env file.
Set the values for variables to POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB in the db/database.en file.
Set the values for variables to database, user, password in the server/config/api.yaml file.


5. Start building containers.
```
$ docker-compose build
```

6. Start containers.
```
$ docker-compose up
```
7. Open a new terminal and connect to a running container.
```
$ docker-compose exec server /bin/bash
```
8. Go to your project directory and apply migrations.
```
$ alembic upgrade head
```
9. Add the quiz data to the database. You don't need to follow this step if you want to create your own quiz. 
```
$ python db/db_init.py
```
End your session with the container. 

#### Usage


## AUTHORS

* **Valeriy Shagur**  - [vshagur](https://github.com/vshagur), email: vshagur@gmail.com

## LICENSE

This project is licensed under the MIT License - see the [LICENSE](https://github.com/vshagur/exgrex-py/blob/docs/LICENSE) file for details
