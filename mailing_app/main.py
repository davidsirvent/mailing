from flask import Blueprint, render_template, flash, request
from . import db

import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from smtplib import SMTPRecipientsRefused, SMTPHeloError, SMTPSenderRefused, SMTPDataError, SMTPNotSupportedError, SMTPAuthenticationError, SMTPException
from socket import timeout
from ssl import SSLError

from .models import Config
from .forms import ConfigForm, MsgForm


main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():

    db.create_all()

    recipients = ["davsircan@gmail.com", "david.error#gmail.com", "dav.sir.can@gmail.com"]
    report = {}

    form = MsgForm()

    if form.validate_on_submit():
        for recipient in recipients:
            result = send(recipient, form.subject.data, form.msg.data)
            # flash("(" + recipient + ") " + result)
            report[recipient] = result

        return render_template('main/report.html', report=report)

    else:
        for field, errorMessages in form.errors.items():
            for err in errorMessages:
                flash("ERROR: " + err)

    return render_template('main/index.html', form=form, recipients=recipients)


@main.route('/config', methods=['GET', 'POST'])
def config():

    config = None

    try:
        config = Config.query.get(1)
    except Exception as error:
        flash("ERROR: No se pudo recuperar la configuración")

    form = ConfigForm()

    if form.validate_on_submit():

        if config is not None:
            config.sender_address = form.sender_address.data
            config.password = form.password.data
            config.smtp_server = form.smtp_server.data
            config.smtp_port = form.smtp_port.data
        else:
            config = Config(sender_address=form.sender_address.data, password=form.password.data, smtp_server=form.smtp_server.data, smtp_port=form.smtp_port.data)
            db.session.add(config)

        try:
            db.session.commit()
            flash("INFO: Configuración guardada.")
        except Exception as error:
            flash("ERROR: " + error.args[0])

    else:
        for field, errorMessages in form.errors.items():
            for err in errorMessages:
                flash("ERROR: " + err)

    return render_template('main/configuration.html', form=form, config=config)


def send(recipient: str, subject: str, message: str):

    login_error = ""
    send_report = ""

    config = Config.query.one()

    # set up the SMTP server (2)
    try:
        # set up the SMTP server
        s = smtplib.SMTP_SSL(host=config.smtp_server, port=config.smtp_port, timeout=5)
        s.login(config.sender_address, config.password)

        # create a message
        msg = MIMEMultipart()

        # setup the parameters of the message
        msg['From'] = config.sender_address
        msg['To'] = recipient
        msg['Subject'] = subject

        # add in the message body
        msg.attach(MIMEText(message, 'html'))

        # send the message via the server set up earlier.
        try:
            s.send_message(msg)
            send_report = "INFO. El correo ha sido enviado correctamente."
        except SMTPRecipientsRefused:
            send_report = "ERROR. El servidor ha rechazado la dirección de destino."
        except SMTPHeloError:
            send_report = "ERROR: El servidor ha rechazado la conexión."
        except SMTPSenderRefused:
            send_report = "ERROR: El servidor ha rechazado la dirección del remitente."
        except SMTPDataError:
            send_report = "ERROR: El servidor ha respondido de manera inesperada."
        except SMTPNotSupportedError:
            send_report = "ERROR: El servidor no soporta una o varias opciones incluidas en el mensaje."

        # Terminate the SMTP session and close the connection
        del msg
        s.quit()
        return send_report

    except SMTPHeloError:
        login_error = "ERROR: El servidor ha rechazado la conexión."
    except SMTPAuthenticationError:
        login_error = "ERROR: El servidor no reconoce la combinación de usuario/clave."
    except SMTPNotSupportedError:
        login_error = "ERROR: El comando AUTH no es soportado por el servidor."
    except SMTPException:
        login_error = "ERROR: No se encontró un método válido de autenticación."
    except timeout:
        login_error = "ERROR. El servidor tardó demasiado en contestar."
    except SSLError:
        login_error = "ERROR. Problema relacionado con SSL."
    except:
        login_error = "ERROR. No especificado."

    return login_error
