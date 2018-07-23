import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "novocore.settings")
django.setup()

from fieldwork.models import Fieldwork
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# --------------------------------------------------------------------------------------------------
# Functions


def fieldwork_complete_reminder(person, fieldwork):

    """Basic email function to
    send weekly summary email"""

    # set to/from
    fromaddr = "JobCore@novoco.com"
    toaddr = person.email

    line = (
        '<p style="font-family: sans-serif; font-size: 1em;">%s,</p><p style="font-family: sans-serif; font-size: 1em;">This is an automated message to notify you that a past <a href="https://goval1.novoco.com/jobcore/fieldwork/%s/view/"><b>Fieldwork Event</b></a> is still marked as active. If this fieldwork is complete, this <a href="https://goval1.novoco.com/jobcore/fieldwork/%s/complete/index"><b>link</b></a> will update the record. Alternatively, click the complete button on your JobCore home page.</p>'
        % (person.first, fieldwork.id, fieldwork.id)
    )

    message = line
    # Build message
    msg = MIMEMultipart()
    msg["From"] = fromaddr
    msg["To"] = toaddr
    msg["Subject"] = "Fieldwork Cleanup Reminder"
    msg.attach(MIMEText(message, "html"))

    # Send Email
    server = smtplib.SMTP("colomx2.novoco.com", 587)
    server.starttls()
    server.login("gis-requests@novoco.com", "x@qYv4ZE!j5AF3%8sXlhmWUbo")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def fieldwork_no_date(person, fieldwork):
    
    """Basic email function to
    send weekly summary email"""
    
    # set to/from
    fromaddr = "JobCore@novoco.com"
    toaddr = person.email
    
    line = (
        '<p style="font-family: sans-serif; font-size: 1em;">%s,</p><p style="font-family: sans-serif; font-size: 1em;">This is an automated message to notify you that your <a href="https://goval1.novoco.com/jobcore/fieldwork/%s/view/"><b>Fieldwork Event</b></a> does not have a scheduled date. You can add a fieldwork date by following this <a href="https://goval1.novoco.com/jobcore/fieldwork/%s/edit/"><b>link</b></a>. If this fieldwork has been completed, please mark it as "Fieldwork Completed".</p>'
        % (person.first, fieldwork.id, fieldwork.id)
    )
    
    message = line
    # Build message
    msg = MIMEMultipart()
    msg["From"] = fromaddr
    msg["To"] = toaddr
    msg["Subject"] = "Fieldwork: Date Needed"
    msg.attach(MIMEText(message, "html"))
    
    # Send Email
    server = smtplib.SMTP("colomx2.novoco.com", 587)
    server.starttls()
    server.login("gis-requests@novoco.com", "x@qYv4ZE!j5AF3%8sXlhmWUbo")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


# --------------------------------------------------------------------------------------------------
# Email Loops

today = datetime.today()
fw = Fieldwork.objects.filter(date__lt=today, is_complete=False)

for i in fw.iterator():
    person = i.assigned_to
    fieldwork_complete_reminder(person, i)
    
fw = Fieldwork.objects.filter(date=None)
for i in fw.iterator():
    person = i.assigned_to
    fieldwork_no_date(person, i)
