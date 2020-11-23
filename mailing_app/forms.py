from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Email


class ConfigForm(FlaskForm):
    sender_address = StringField('Correo del remitente', validators=[DataRequired(), Email("Correo no válido.")])
    password = PasswordField('Clave', validators=[DataRequired()])
    smtp_server = StringField('Servidor SMTP', validators=[DataRequired()])
    smtp_port = IntegerField('Puerto SMTP', validators=[DataRequired("Introduzca un puerto SMTP válido.")])