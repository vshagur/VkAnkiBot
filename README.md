# VkAnkiBot
VkAnkiBot is a game bot for creating quizzes on the Vkontakte social network.

#### DOCUMENTATION


#### Installation

To run the bot, you need a valid account on the Vkontakte social network, a group and a token. 
You can find out the details in the [documentation](https://vk.com/dev/manuals). 

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
```
Set the values for variables to VK_API_KEY, VK_GROUP_ID in the .env file.

Set the values for variables to POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB in the db/database.en file.

Set the values for variables to database, user, password in the server/config/api.yaml file.
```

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

Run.

To start the bot, run the command:

```
$ docker-compose up -d
```

Manage.

You can manage your bot data using the admin panel. It is available at 

```
\<you host\>:8080/api/doc
```

Tests.

```
$ python3 -m pytest tests/
```

#### Built With

* [aiohttp](https://docs.aiohttp.org/en/stable/) - Asynchronous HTTP Client/Server for asyncio and Python.
* [aiohttp-apispec](https://pypi.org/project/aiohttp-apispec/) - Build and document REST APIs with aiohttp and apispec
* [Alembic](https://alembic.sqlalchemy.org/en/latest/) - Alembic is a lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python.
* [gino](https://python-gino.org/) - GINO Is Not ORM - is a lightweight asynchronous ORM built on top of SQLAlchemy core for Python asyncio.
* [Pytest](https://docs.pytest.org/en/latest/) - The pytest framework makes it easy to write small tests, yet scales to support complex functional testing for applications and libraries.
* [aiohttp-swagger](https://aiohttp-swagger.readthedocs.io/en/latest/) - Swagger API Documentation builder for aiohttp server
* [PostgreSQL](https://www.postgresql.org/) - The World's Most Advanced Open Source Relational Database
* [Docker](https://www.docker.com/) - Docker is a set of platform as a service (PaaS) products that use OS-level virtualization to deliver software in packages called containers.


#### AUTHORS

* **Valeriy Shagur**  - [vshagur](https://github.com/vshagur), email: vshagur@gmail.com

#### LICENSE

This project is licensed under the MIT License - see the [LICENSE](https://github.com/vshagur/exgrex-py/blob/docs/LICENSE) file for details
