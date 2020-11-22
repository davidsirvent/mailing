from flask import Blueprint, render_template, flash
from . import db

import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .models import Config
from .forms import ConfigForm


main = Blueprint('main', __name__)


@main.route('/')
def index():    
    return render_template('main/index.html')


@main.route('/config', methods=('GET', 'POST'))
def config():
    form = ConfigForm()
    if form.validate_on_submit():
        flash("INFO: Todo ok.")
    else:    
        flash("ERROR.")

    return render_template('main/configuration.html', form=form)


def send():
    message = '<H2>This is a</H3><H1>MESSAGE</H1>'

    config = Config.query.one()

    # set up the SMTP server
    s = smtplib.SMTP_SSL(host=config.smtp_server, port=config.smtp_port)    
    s.login(config.sender_address, config.password)

    # create a message
    msg = MIMEMultipart()       

    # setup the parameters of the message
    msg['From'] = config.sender_address
    msg['To'] = 'dav.sir.can@gmail.com'
    msg['Subject'] = "This is TEST"

    # add in the message body
    msg.attach(MIMEText(message, 'html'))

    # send the message via the server set up earlier.
    s.send_message(msg)
    del msg

    # Terminate the SMTP session and close the connection
    s.quit()