# Library Management System
A simple flask app to manage users along with mysql service now with [docker support](https://github.com/hamza-avvan/library-management-system?tab=readme-ov-file#getting-started-with-docker).

![Libray Management App - Flask](https://github.com/hamzaavvan/library-management-system/blob/master/ss/ss2.JPG?raw=true)

**Youtube Tutorial Walkthrough:** [https://www.youtube.com/watch?v=As90fkeMkyA](https://www.youtube.com/watch?v=As90fkeMkyA)


## Installation

To run the app flawlessly, satisfy the requirements
```bash
pip install -r requirements.txt
```

## Set Environment Variables
Replace `.env.example` with `.env` file and update the environment vaiables.

```bash
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True

# DB info
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DB=lms
```

**Note:** If you update the `MYSQL_DB` variable, remember to also update the corresponding value in the [docker-compose.yaml](https://github.com/hamza-avvan/library-management-system/blob/master/docker-compose.yaml#L12) file to ensure consistency when using Docker. There's an exceptioin for `MYSQL_HOST` which should set set within [docker-compose.yaml](https://github.com/hamza-avvan/library-management-system/blob/master/docker-compose.yaml#L29) file explicitly.

To setup a mail server you can set the below variable in `.env` file. 
```bash
# SMTP credentials
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587 
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_USE_TLS=True
MAIL_USE_SSL=
MAIL_DEBUG=1
MAIL_DEFAULT_SENDER=sender@domain.com
```

I'm using Flask-Mail for managing emails. For more information, visit [https://flask-mail.readthedocs.io/en/latest/](https://flask-mail.readthedocs.io/en/latest/)


## Setup Datbase
Export `lms.sql` database from within [db](https://github.com/hamza-avvan/library-management-system/tree/master/db) directory using Phpmyadmin or terminal:

```bash
mysql -u <username> -p <password> lms < lms.sql
```

## Start Server
```bash
flask run
```

Or run this command 
```bash
python -m flask run
```

### Debugging

Start flask with auto reload on code change
```bash
flask run --reload
```
---------------------

# Getting Started with Docker
With this update, you can now easily get an out-of-the-box support for a Docker environment. There's no need to set up a mysql service, import databases, or run multiple commands. 

Create an `.env` file as described in the [Set Environment Variables](https://github.com/hamza-avvan/library-management-system?tab=readme-ov-file#set-environment-variables) section, then execute the `docker-compose` command. This will automate the entire setup process for you.

Build & start the app:
```bash
docker-compose up --build
```

**OR**

Start app (without building):
```bash
docker-compose up
```
