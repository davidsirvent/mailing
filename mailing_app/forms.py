from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email


class ConfigForm(FlaskForm):
    sender_address = StringField('Correo del remitente', validators=[DataRequired(), Email("Correo no válido.")])
    password = PasswordField('Clave', validators=[DataRequired()])
    smtp_server = StringField('Servidor SMTP', validators=[DataRequired()])
    smtp_port = IntegerField('Puerto SMTP', validators=[DataRequired("Introduzca un puerto SMTP válido.")])
    save_btn = SubmitField(label='Guardar Configuración')

class MsgForm(FlaskForm):
    subject = StringField('Asunto', validators=[DataRequired("El asunto no puede estar vacio")])
    msg = StringField('Mensaje', validators=[DataRequired("El mensaje no puede estar vacio")])
    send_btn = SubmitField(label='Enviar')

class ReportForm(FlaskForm):
    sender_address = StringField('Correo del remitente', validators=[DataRequired(), Email("Correo no válido.")])
    send_btn = SubmitField(label='Enviar informe por correo')    

class UploadForm(FlaskForm):
    file = FileField(validators=[DataRequired()])
    upload_btn = SubmitField(label='Subir')

class DeleteForm(FlaskForm):
    delete_btn = SubmitField(label='Borrar contactos')