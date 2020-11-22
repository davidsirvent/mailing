from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class ConfigForm(FlaskForm):
    sender_address = StringField('sender', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    smtp_server = StringField('SMTP server', validators=[DataRequired()])
    smtp_port = IntegerField('SMTP port', validators=[DataRequired()])