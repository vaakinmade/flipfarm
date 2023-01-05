from threading import Thread

from flask_mail import Message, Mail
from flask import render_template, Flask

from src.domain.ports.user_service import get_user_token
from src.main import config

app = Flask(__name__)
app.config.from_object(config)
mail = Mail(app)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


class Email:
    token_use: str
    token: str
    user: dict
    subject: str
    template_html: str
    template_text: str

    def __init__(self, token_use, user, subject, template_html, template_text):
        self.token_use = token_use
        self.user = user
        self.subject = subject
        self.template_text = template_text
        self.template_html = template_html

    def send_email(self, sender, recipients, text_body, html_body):
        msg = Message(self.subject, sender=sender, recipients=recipients)
        msg.body = text_body
        msg.html = html_body
        Thread(target=send_async_email, args=(app, msg)).start()

    def send_user_email(self):
        self.token = get_user_token(self.user.get("id_"), self.token_use)
        self.send_email(sender=config.MAIL_DEFAULT_SENDER,
                        recipients=[self.user.get("email")],
                        text_body=render_template(self.template_text,
                                                  user=self.user, token=self.token),
                        html_body=render_template(self.template_html,
                                                  user=self.user, token=self.token))
