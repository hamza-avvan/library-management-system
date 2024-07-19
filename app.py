import os
from flask import Flask
from Misc.functions import *

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

# Setting DAO Class
from Models.DAO import DAO
from Models.Mailer import Mailer

DAO = DAO(app)
mailer = Mailer(app)

# Registering blueprints
from routes.user import user_view
from routes.book import book_view
from routes.admin import admin_view

# Registering custom functions to be used within templates
app.jinja_env.globals.update(
    ago=ago,
    str=str,
)

app.register_blueprint(user_view)
app.register_blueprint(book_view)
app.register_blueprint(admin_view)