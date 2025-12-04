import smtplib
from email.message import EmailMessage
import os

EMAIL_ADDRESS = 'your_email@gmail.com'
EMAIL_PASSWORD = 'your_password'

def send(to_email, pdf_file):
    msg = EmailMessage()
    msg['Subject'] = 'Your Event Certificate'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.set_content('Congratulations! Find your certificate attached.')

    with open(pdf_file, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename=os.path.basename(pdf_file))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
