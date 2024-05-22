# Library Management System
A simple flask app to manage users along with mysql service now with docker support.

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

# FB info
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DB=lms
```

## Setup Datbase
Export `lms.sql` database from within [db](https://github.com/hamza-avvan/library-management-system/tree/master/db) directory using Phpmyadmin or terminal

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

Start flask with auto reload on code change
```bash
flask run --reload
```
---------------------

# Getting Started with Docker
With this update, you can now easily get started with out-of-the-box support for a Docker environment. There's no need to set up a mysql service, import databases, or run multiple commands. Simply execute the `docker-compose` command, and it will handle everything for you.

Build & start the app:
```bash
docker-compose up --build
```

**OR**

Start app (without building):
```bash
docker-compose up
```
