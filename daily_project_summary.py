import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "novocore.settings")
django.setup()

from helpdesk.models import Employee
from projects.models import Projects
from datetime import datetime
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# --------------------------------------------------------------------------------------------------
# Functions


def daily_project_summary(person, message):
    
    """Basic email function to
    send weekly summary email"""
    
    # set to/from
    fromaddr = "JobCore@novoco.com"
    toaddr = person.email
    
    # Build message
    msg = MIMEMultipart()
    msg["From"] = fromaddr
    msg["To"] = toaddr
    msg["Subject"] = "Daily Active Project Summary"
    msg.attach(MIMEText(message, "html"))
    
    # Send Email
    server = smtplib.SMTP("colomx2.novoco.com", 587)
    server.starttls()
    server.login("gis-requests@novoco.com", "x@qYv4ZE!j5AF3%8sXlhmWUbo")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def project_overdue_check(person, days, message):
    
    """Basic email function to
    send weekly summary email"""
    
    # set to/from
    fromaddr = "JobCore@novoco.com"
    toaddr = person.email
    
    # Build message
    msg = MIMEMultipart()
    msg["From"] = fromaddr
    msg["To"] = toaddr
    msg["Subject"] = "Project %s days past Client Due Date" % (abs(days))
    msg.attach(MIMEText(message, "html"))
    
    # Send Email
    server = smtplib.SMTP("colomx2.novoco.com", 587)
    server.starttls()
    server.login("gis-requests@novoco.com", "x@qYv4ZE!j5AF3%8sXlhmWUbo")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


# --------------------------------------------------------------------------------------------------
# Manager Weekly Summary
manager = Employee.objects.filter(is_active=True, is_manager=True)

for j, i in enumerate(manager.iterator()):
    projects = Projects.objects.filter(manager=i.manager, is_active=True).order_by(
        "client_due_date"
    )
    if len(projects) > 0:
        overdue = 0
        table = (
            '<table border="1"><thead><tr><th width="40%" style="text-align:center;">Project</th><th width="20%" style="text-align:center;">Status</th><th width="20%" style="text-align:center;">Client Due Date</th><th width="20%" style="text-align:center;">Remaining Workdays (excludes weekends)</th></tr></thead><tbody>'
        )
        for project in projects.iterator():
            days = np.busday_count(datetime.today(), project.client_due_date)
            if days < 0:
                overdue = overdue + 1
            row = (
                '<tr class="text-center"><td style="text-align:center;"><a href="http://goval1.novoco.com/jobcore/projects/%s/view/">%s</a></td><td style="text-align:center;">%s</td><td style="text-align:center;">%s</td><td style="text-align:center;">%s</td></tr>'
                % (
                    project.id,
                    project.name,
                    project.stage,
                    project.client_due_date,
                    days,
                )
            )
            table = table + row
        table = table + "</tbody></table>"

        line1 = (
            '<p style="font-family: sans-serif; font-size: 1em;">%s,</p><p style="font-family: sans-serif; font-size: 1em;">This is an automated summary of active projects under your management.</p>'
            % (i.first)
        )

        line2 = (
            '<p style="font-family: sans-serif; font-size: 1em;">There are currently %s projects past their due date. If any of the listed projects are completed, please update the project status to "Complete"</p>'
            % (overdue)
        )

        message = line1 + line2 + table

        daily_project_summary(i, message)

# --------------------------------------------------------------------------------------------------
# Partner Weekly Summary
partner = Employee.objects.filter(is_active=True, is_partner=True)

for j, i in enumerate(partner.iterator()):
    projects = Projects.objects.filter(partner=i.partner, is_active=True).order_by(
        "client_due_date"
    )
    if len(projects) > 0:
        overdue = 0
        table = (
            '<table border="1"><thead><tr><th width="40%" style="text-align:center;">Project</th><th width="20%" style="text-align:center;">Status</th><th width="20%" style="text-align:center;">Client Due Date</th><th width="20%" style="text-align:center;">Remaining Workdays (excludes weekends)</th></tr></thead><tbody>'
        )
        for project in projects.iterator():
            days = np.busday_count(datetime.today(), project.client_due_date)
            if days < 0:
                overdue = overdue + 1
            row = (
                '<tr class="text-center"><td style="text-align:center;"><a href="http://goval1.novoco.com/jobcore/projects/%s/view/">%s</a></td><td style="text-align:center;">%s</td><td style="text-align:center;">%s</td><td style="text-align:center;">%s</td></tr>'
                % (
                    project.id,
                    project.name,
                    project.stage,
                    project.client_due_date,
                    days,
                )
            )
            table = table + row
        table = table + "</tbody></table>"

        line1 = (
            '<p style="font-family: sans-serif; font-size: 1em;">%s,</p><p style="font-family: sans-serif; font-size: 1em;">This is an automated summary of active projects under your management.</p>'
            % (i.first)
        )

        line2 = (
            '<p style="font-family: sans-serif; font-size: 1em;">There are currently %s projects past their due date. If any of the listed projects are completed, please update the project status to "Complete"</p>'
            % (overdue)
        )

        message = line1 + line2 + table

        daily_project_summary(i, message)


# --------------------------------------------------------------------------------------------------
# Overdue Project Completeion Check
projects = Projects.objects.filter(is_active=True).order_by(
    "client_due_date"
)
for project in projects.iterator():
    days = np.busday_count(datetime.today(), project.client_due_date)
    if days < -30:
        
        line = (
            '<p style="font-family: sans-serif; font-size: 1em;">%s,</p><p style="font-family: sans-serif; font-size: 1em;">This is an automated message to check the status of your project.</p>'
            % (project.biller.first)
        )
        
        line = line + (
            '<p style="font-family: sans-serif; font-size: 1em;">If <a href="http://goval1.novoco.com/jobcore/projects/%s/view/">%s</a> has been completed, please update the project status to "Complete" in JobCore.</p>'
            % (project.id,
               project.name,
               )
        )
        
        message = line
        
        if project.biller:
            project_overdue_check(project.biller, days, message)
