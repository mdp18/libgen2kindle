import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import configparser

settings = configparser.ConfigParser()
settings.read('settings.ini')

#The email and password which your kindle is registered with -- Approved Personal Document E-mail List
fromaddr = settings['general']['your-email']
fromaddrpw = settings['general']['your-email-password']

#Your kindle email [@kindle.com] - Find under [Send-to-Kindle E-Mail Settings]
toaddr = settings['general']['kindle-email']



def getEmailProvider():
    email_provider = settings['general']['email-provider']
    if email_provider == 'gmail':
        return 'smtp.gmail.com'
    elif email_provider == 'outlook' or email_provider == 'hotmail' or email_provider == 'live':
        return 'smtp.office365.com'
    elif email_provider == 'yahoo':
        return 'smtp.mail.yahoo.com'
    elif email_provider == 'aol':
        return 'smtp.aol.com'
    else:
        return Exception('Unknown email provider.')

def getEmailProviderPort():
    email_provider = settings['general']['email-provider']
    if email_provider == 'gmail':
        return 587
    elif email_provider == 'outlook' or email_provider == 'hotmail' or email_provider == 'live':
        return 587
    elif email_provider == 'yahoo':
        return 465
    elif email_provider == 'aol':
        return 587
    else:
        return Exception('Unknown email provider')

def send(subject, path):
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject

    body = ""

    msg.attach(MIMEText(body, 'plain'))

    attachment = open(path, "rb")

    part = MIMEBase('application/x-mobipocket-ebook', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % subject)

    msg.attach(part)

    ### IMPORTANT ###
    # Microsoft Live = smtp.live.com, For gmail use smtp.gmail.com and so on..

    server = smtplib.SMTP(getEmailProvider(), getEmailProviderPort())
    server.starttls()

    #Password of the email your kindle is registed with
    server.login(fromaddr, fromaddrpw)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
