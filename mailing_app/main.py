from flask import Blueprint, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from . import db

import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from smtplib import SMTPRecipientsRefused, SMTPHeloError, SMTPSenderRefused, SMTPDataError, SMTPNotSupportedError, SMTPAuthenticationError, SMTPException
from socket import timeout
from ssl import SSLError
from sqlalchemy.orm.exc import NoResultFound

import locale
import time

from .models import Config, Recipient, Content, Result
from .forms import ConfigForm, MsgForm, ReportForm, UploadForm, DeleteForm, UploadMsgForm, MsgFileForm


main = Blueprint('main', __name__)


# Main View
@main.route('/', methods=['GET', 'POST'])
def index():

    db.create_all()
        
    recipients = []
    for item in Recipient.query.all():
        recipients.append(item.recipient)

    report = {}

    # Send mails
    form = MsgForm()
    if form.send_btn.data:
        if form.validate_on_submit():

            for recipient in recipients:
                result = send(recipient, form.subject.data, form.msg.data)
                timestamp = time.strftime('%d %b %Y %H:%M:%S')
                report[recipient] = result + ' (' + timestamp + ')'

            session['report'] =  report                    
            return redirect(url_for('main.report', report=report))

        else:
            for field, errorMessages in form.errors.items():
                for err in errorMessages:
                    flash("ERROR: " + err)

    # Upload contacts (recipients)
    formFile = UploadForm()    
    if formFile.upload_btn.data:
        if formFile.validate_on_submit():
            recipients = []
            try:
                for line in formFile.file.data.readlines():
                    line = line.decode("utf-8")
                    recipients.append(line)
                    db.session.add(Recipient(recipient=line))
            except Exception as error:
                flash("ERROR: No se ha podido procesar el fichero ")
            else:
                db.session.commit()           

        else:
            for field, errorMessages in formFile.errors.items():
                for err in errorMessages:
                    flash("ERROR: " + err)
    
    # Upload Message
    formMsgUpload = UploadMsgForm()
    if formMsgUpload.upload_msg_btn.data:
        if formMsgUpload.validate_on_submit():
            Content.query.delete()
            try:
                text = formMsgUpload.file_msg.data.read()
                text = text.decode("utf-8")                
                db.session.add(Content(msg=text))
            except Exception as error:
                flash("ERROR: No se ha podido procesar el fichero. ")
            else:
                db.session.commit()           

        else:
            for field, errorMessages in formMsgUpload.errors.items():
                for err in errorMessages:
                    flash("ERROR: " + err)
    
    # Send file msg
    formMsgFile = MsgFileForm()
    if formMsgFile.send_msg_btn.data:
        if formMsgFile.validate_on_submit():

            # Delete previous info on Result table.
            Result.query.delete()

            msg = Content.query.get(1).msg            
            for recipient in recipients:
                result_msg = send(recipient, formMsgFile.subject_msg.data, msg)                
                timestamp = time.strftime('%d %b %Y %H:%M:%S')
                result_msg = result_msg + ' [' + formMsgFile.subject_msg.data + ']' + ' (' + timestamp + ')'
                result = Result(email=recipient, result=result_msg)
                db.session.add(result)
                db.session.commit()
            
            return redirect(url_for('main.report'))         

        else:
            for field, errorMessages in formMsgFile.errors.items():
                for err in errorMessages:
                    flash("ERROR: " + err)
    

    # Delete contacts    
    formDelete = DeleteForm()    
    if formDelete.delete_btn.data:
        if formDelete.validate_on_submit():
            recipients = []           
            Recipient.query.delete()
            db.session.commit()

        else:
            for field, errorMessages in formDelete.errors.items():
                for err in errorMessages:
                    flash("ERROR: " + err)    
    
    return render_template('main/index.html', form=form, formFile=formFile, formDelete=formDelete, formMsgUpload=formMsgUpload, formMsgFile=formMsgFile, recipients=recipients)


# Report view (when mailing is sent)
@main.route('/report', methods=['GET', 'POST'])
def report():    
    report = Result.query.all()
    
    form = ReportForm()
    if form.send_btn.data:
        if form.validate_on_submit():
            msg = '<html><h1>Infome de Mailing</h1>'
            msg = msg + '<table style="border:1px solid #cecece; padding: 2px;">'
            for result in report:            
                msg = msg + '<tr><td style="border:1px solid #cecece; padding: 2px;">{0}</td><td style="border:1px solid #cecece; padding: 2px;">{1}</td></tr>'.format(result.email, result.result)
            msg = msg + '</table></html>'
            send(recipient=form.sender_address.data, subject="Informe del mailing", message=msg)

        else:
            for field, errorMessages in form.errors.items():
                for err in errorMessages:
                    flash("ERROR: " + err)

    return render_template('main/report.html', report=report, form=form)

# Preview view
@main.route('/preview')
def preview():    
    html = None

    try:
        html = Content.query.get(1).msg
    except Exception as error:
        html = "<h1>No se ha cargado ningún fichero</h1>"

    return html

# Config view
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


# Send one email
def send(recipient: str, subject: str, message: str):

    login_error = ""
    send_report = ""    

    # set up the SMTP server (2)
    try:        
        config = Config.query.one()

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

    except NoResultFound:
        login_error = "ERROR. No se pudo recuperar datos de la configuración."    
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
