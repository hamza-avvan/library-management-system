import os
from flask_mail import Mail
from flask_mail import Message
from threading import Thread

class Mailer(object):
    """Initialize smtp service """
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL')
    MAIL_DEBUG = os.environ.get('MAIL_DEBUG')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    def __init__(self, app):
        app.config['MAIL_SERVER'] = self.MAIL_SERVER
        app.config['MAIL_PORT'] = self.MAIL_PORT
        app.config['MAIL_USERNAME'] = self.MAIL_USERNAME
        app.config['MAIL_PASSWORD'] = self.MAIL_PASSWORD
        app.config['MAIL_USE_TLS'] = self.MAIL_USE_TLS or False
        app.config['MAIL_USE_SSL'] = self.MAIL_USE_SSL
        app.config['MAIL_DEBUG'] = self.MAIL_DEBUG or False
        app.config['MAIL_DEFAULT_SENDER'] = self.MAIL_DEFAULT_SENDER
        
        self.app = app
        self.mail = Mail(app)
    
    
    def exec_email(self, msg):
        with self.app.app_context():
            self.mail.send(msg)

    def send_async_email(self, msg):
        thr = Thread(target=self.exec_email, args=[msg])
        thr.start()
        
    def message(self, subject, recipients, sender=None):
        return Message(subject=subject, recipients=recipients, sender=sender)