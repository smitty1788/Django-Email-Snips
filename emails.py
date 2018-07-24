import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def project_created(opportunity_obj, employee, attachment=[]):
    
    fromaddr = "JobCore@novoco.com"
    toaddr = 'goval-new-engmt@novoco.com'
    
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Cc'] = employee.email
    msg['Subject'] = "Project Created: %s" % (opportunity_obj.name)
    
    line = '<p style="font-family: sans-serif; font-size: 1em;">Hello,</p><p style="font-family: sans-serif; font-size: 1em;">This is a courtesy e-mail to let you know that Project <a href="http://goval1.novoco.com/jobcore/projects/%s/view/"><b>%s</b></a> has be created.</p>' % (opportunity_obj.id, opportunity_obj.name)
    
    line = line + '<b>Client</b>: <a href="http://goval1.novoco.com/jobcore/accounts/%s/view/"><b>%s</b></a><br>' % (opportunity_obj.account.id, opportunity_obj.account)
    
    if opportunity_obj.contact:
        line = line + '<b>Contact</b>: <a href="http://goval1.novoco.com/jobcore/contacts/%s/view/"><b>%s</b></a><br>' % (opportunity_obj.contact.id, opportunity_obj.contact)
        
    line = line + '<b>Project ID</b>: %s<br>' % (opportunity_obj.id)
    
    line = line + '<b>Fee</b>: %s<br>' % (opportunity_obj.fee)
    
    if opportunity_obj.inclusive_expenses == '0':
        line = line + '<b>Expenses</b>: Inclusive<br>'
    elif opportunity_obj.inclusive_expenses == '1':
        line = line + '<b>Expenses</b>: $%s (Plus Exp)<br>' % opportunity_obj.exspense
        
    line = line + '<b>Retainer</b>: $%s<br>' % (opportunity_obj.retainer)
    
    line = line + '<b>Due Date</b>: %s<br>' % (opportunity_obj.client_due_date)
    
    if opportunity_obj.eng_type.all():
        for i in opportunity_obj.eng_type.all():
            line = line + '<b>Engagement Type</b>: %s<br>' % (i)
    else:
        line = line + '<b>Engagement Type</b>: Not Currently Assigned<br>'
        
    line = line + '<b>Property Name</b>: %s<br>' % (opportunity_obj.name)
    
    line = line + '<b>Property Location</b>: %s, %s<br>' % (opportunity_obj.city, opportunity_obj.state)
    
    line = line + '<b>Managing Partner</b>: %s<br>' % (opportunity_obj.partner)
    
    if opportunity_obj.principal:
        line = line + '<b>Principal</b>: %s<br>' % (opportunity_obj.principal)
    else:
        line = line + '<b>Principal</b>: Not Assigned<br>'
        
    line = line + '<b>Manager</b>: %s<br>' % (opportunity_obj.manager)
    
    if opportunity_obj.biller:
        line = line + '<b>Biller</b>: %s<br>' % (opportunity_obj.biller)
    else:
        line = line + '<b>Biller</b>: Not Assigned<br>'
        
    message = line
    
    msg.attach(MIMEText(message, 'html'))
    
    for f in attachment:
        filepath = r"%s" % (str(f.file))
        with open(filepath, 'rb') as a_file:
            basename = f.name
            part = MIMEApplication(a_file.read(), Name=basename)
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename
            msg.attach(part)
            
    server = smtplib.SMTP('colomx2.novoco.com', 587)
    server.starttls()
    server.login('gis-requests@novoco.com', "x@qYv4ZE!j5AF3%8sXlhmWUbo")
    text = msg.as_string()
    server.sendmail(fromaddr, ['goval-new-engmt@novoco.com', employee.email], text)
    server.quit()


def deltek_update(opportunity_obj, deltek, employee):
    
    fromaddr = "JobCore@novoco.com"
    partneraddr = opportunity_obj.partner.email
    manageraddr = opportunity_obj.manager.email
    toaddr = partneraddr + ";" + manageraddr
    for i in opportunity_obj.assigned_to.all():
            toaddr = toaddr + ";" + i.email

    partneraddr = [opportunity_obj.partner.email]
    manageraddr = [opportunity_obj.manager.email]
    analystaddr = []
    for i in opportunity_obj.assigned_to.all():
        analystaddr.append(i.email)

    final_toaddr = manageraddr + analystaddr + partneraddr

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Project Update: Deltek # Assigned for %s" % (opportunity_obj.name)

    line = '<p style="font-family: sans-serif; font-size: 1em;">Hello,</p><p style="font-family: sans-serif; font-size: 1em;">This is a courtesy e-mail to let you know that Deltek Engagment #%s has been assigned for <a href="http://goval1.novoco.com/jobcore/projects/%s/view/"><b>%s</b></a>.</p>' % (deltek, opportunity_obj.id, opportunity_obj.name)

    line = line + '<b>Client</b>: <a href="http://goval1.novoco.com/jobcore/accounts/%s/view/"><b>%s</b></a><br>' % (opportunity_obj.account.id, opportunity_obj.account)
    
    if opportunity_obj.contact:
        line = line + '<b>Contact</b>: <a href="http://goval1.novoco.com/jobcore/contacts/%s/view/"><b>%s</b></a><br>' % (opportunity_obj.contact.id, opportunity_obj.contact)
        
    line = line + '<b>Project ID</b>: %s<br>' % (opportunity_obj.id)
    
    line = line + '<b>Fee</b>: %s<br>' % (opportunity_obj.fee)
    
    if opportunity_obj.inclusive_expenses == '0':
        line = line + '<b>Expenses</b>: Inclusive<br>'
    elif opportunity_obj.inclusive_expenses == '1':
        line = line + '<b>Expenses</b>: $%s (Plus Exp)<br>' % opportunity_obj.exspense
        
    line = line + '<b>Retainer</b>: $%s<br>' % (opportunity_obj.retainer)
    
    line = line + '<b>Due Date</b>: %s<br>' % (opportunity_obj.client_due_date)
    
    if opportunity_obj.eng_type.all():
        for i in opportunity_obj.eng_type.all():
            line = line + '<b>Engagement Type</b>: %s<br>' % (i)
    else:
        line = line + '<b>Engagement Type</b>: Not Currently Assigned<br>'
        
    line = line + '<b>Property Name</b>: %s<br>' % (opportunity_obj.name)
    
    line = line + '<b>Property Location</b>: %s, %s<br>' % (opportunity_obj.city, opportunity_obj.state)
    
    line = line + '<b>Managing Partner</b>: %s<br>' % (opportunity_obj.partner)
    
    if opportunity_obj.principal:
        line = line + '<b>Principal</b>: %s<br>' % (opportunity_obj.principal)
    else:
        line = line + '<b>Principal</b>: Not Assigned<br>'
        
    line = line + '<b>Manager</b>: %s<br>' % (opportunity_obj.manager)
    
    if opportunity_obj.biller:
        line = line + '<b>Biller</b>: %s<br>' % (opportunity_obj.biller)
    else:
        line = line + '<b>Biller</b>: Not Assigned<br>'

    message = line

    msg.attach(MIMEText(message, 'html'))

    server = smtplib.SMTP('colomx2.novoco.com', 587)
    server.starttls()
    server.login('gis-requests@novoco.com', "x@qYv4ZE!j5AF3%8sXlhmWUbo")
    text = msg.as_string()
    server.sendmail(fromaddr, final_toaddr, text)
    server.quit()


def assigned_to_project(opportunity_obj, value, employee):
    
    fromaddr = "JobCore@novoco.com"
    toaddr = value.email

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Project Assigned: %s" % (opportunity_obj.name)

    line1 = '<p style="font-family: sans-serif; font-size: 1em;">Hello,</p><p style="font-family: sans-serif; font-size: 1em;">This is a courtesy e-mail to let you know that you have been assigned to <a href="http://goval1.novoco.com/jobcore/projects/%s/view/"><b>%s</b></a>.</p>' % (opportunity_obj.id, opportunity_obj.name)

    line2 = '<b>Project ID</b>: %s<br>' % (opportunity_obj.id)

    line3 = '<b>Project Name</b>: %s<br>' % (opportunity_obj.name)

    line4 = '<b>Client Due Date</b>: %s<br>' % (opportunity_obj.client_due_date)

    line5 = '<b>Assigned to project by</b>: %s<br>' % (employee.fullname)
    
    message = line1 + line2 + line3 + line4 + line5

    msg.attach(MIMEText(message, 'html'))

    server = smtplib.SMTP('colomx2.novoco.com', 587)
    server.starttls()
    server.login('gis-requests@novoco.com', "x@qYv4ZE!j5AF3%8sXlhmWUbo")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def assigned_self(opportunity_record, employee):
    
    fromaddr = "JobCore@novoco.com"
    toaddr = opportunity_record.manager.email

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Project Update: %s" % (opportunity_record.name)


    line1 = '<p style="font-family: sans-serif; font-size: 1em;">%s,</p><p style="font-family: sans-serif; font-size: 1em;">%s has assigned themselves to Project <a href="http://goval1.novoco.com/jobcore/projects/%s/view/"><b>%s</b></a></p>' % (opportunity_record.manager.fullname, employee.fullname, opportunity_record.id, opportunity_record.name)
    
    message = line1

    msg.attach(MIMEText(message, 'html'))

    server = smtplib.SMTP('colomx2.novoco.com', 587)
    server.starttls()
    server.login('gis-requests@novoco.com', "x@qYv4ZE!j5AF3%8sXlhmWUbo")
    text = msg.as_string()
    server.sendmail(fromaddr, [toaddr, employee.email], text)
    server.quit()


def manager_review(opportunity_record, employee):
    
    fromaddr = "JobCore@novoco.com"
    toaddr = opportunity_record.manager.email

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Project Manager Review: %s" % (opportunity_record.name)


    line1 = '<p style="font-family: sans-serif; font-size: 1em;">%s,</p><p style="font-family: sans-serif; font-size: 1em;">Project <a href="http://goval1.novoco.com/jobcore/projects/%s/view/"><b>%s</b></a></p> has been submited for manager review by %s' % (opportunity_record.manager.fullname, opportunity_record.id, opportunity_record.name, employee.fullname)
    
    message = line1

    msg.attach(MIMEText(message, 'html'))

    server = smtplib.SMTP('colomx2.novoco.com', 587)
    server.starttls()
    server.login('gis-requests@novoco.com', "x@qYv4ZE!j5AF3%8sXlhmWUbo")
    text = msg.as_string()
    server.sendmail(fromaddr, [toaddr, employee.email], text)
    server.quit()
    

def partner_review(opportunity_record, employee):
    
    fromaddr = "JobCore@novoco.com"
    toaddr = opportunity_record.partner.email

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Project Partner Review: %s" % (opportunity_record.name)


    line1 = '<p style="font-family: sans-serif; font-size: 1em;">%s,</p><p style="font-family: sans-serif; font-size: 1em;">Project <a href="http://goval1.novoco.com/jobcore/projects/%s/view/"><b>%s</b></a></p> has been submited for partner review by %s' % (opportunity_record.partner.fullname, opportunity_record.id, opportunity_record.name, employee.fullname)
    
    message = line1

    msg.attach(MIMEText(message, 'html'))

    server = smtplib.SMTP('colomx2.novoco.com', 587)
    server.starttls()
    server.login('gis-requests@novoco.com', "x@qYv4ZE!j5AF3%8sXlhmWUbo")
    text = msg.as_string()
    server.sendmail(fromaddr, [toaddr, employee.email], text)
    server.quit()


def project_complete(opportunity_obj, employee):
    
    
    fromaddr = "JobCore@novoco.com"
    manageraddr = opportunity_obj.manager.email
    toaddr = manageraddr
    for i in opportunity_obj.assigned_to.all():
            toaddr = toaddr + ";" + i.email

    manageraddr = [opportunity_obj.manager.email]
    analystaddr = []
    for i in opportunity_obj.assigned_to.all():
        analystaddr.append(i.email)

    final_toaddr = manageraddr + analystaddr

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Project Complete: %s" % (opportunity_obj.name)


    line1 = '<p style="font-family: sans-serif; font-size: 1em;">Hello,</p><p style="font-family: sans-serif; font-size: 1em;">This is a courtesy e-mail to let you know that <a href="http://goval1.novoco.com/jobcore/projects/%s/view/"><b>%s</b></a> has been marked as completed by %s</p>' % (opportunity_obj.id, opportunity_obj.name, employee.fullname)

    message = line1

    msg.attach(MIMEText(message, 'html'))

    server = smtplib.SMTP('colomx2.novoco.com', 587)
    server.starttls()
    server.login('gis-requests@novoco.com', "x@qYv4ZE!j5AF3%8sXlhmWUbo")
    text = msg.as_string()
    server.sendmail(fromaddr, final_toaddr, text)
    server.quit()
