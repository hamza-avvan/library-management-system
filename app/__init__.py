import os
from flask import Flask
from app.utils.functions import ago

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = os.environ.get('SECRET_KEY')

from app.extensions.mailer import Mailer
from app.extensions.scheduler import Scheduler
from app.database.dao import DAO

Scheduler = Scheduler(app)
DAO = DAO(app)
mailer = Mailer(app)

from app.dependencies import configure_services

configure_services(DAO, mailer, Scheduler)

from app.controllers.admin import admin_view
from app.controllers.book import book_view
from app.controllers.user import user_view

app.jinja_env.globals.update(
    ago=ago,
    str=str,
)

app.register_blueprint(user_view)
app.register_blueprint(book_view)
app.register_blueprint(admin_view)
