from flask_apscheduler import APScheduler
from app.config import Config

class Scheduler(object):

    def __init__(self, app):
        app.config.from_object(Config)
        self.scheduler = APScheduler()
        
        self.scheduler.init_app(app)
        self.scheduler.start()

    def exec_email(self, msg):
        return