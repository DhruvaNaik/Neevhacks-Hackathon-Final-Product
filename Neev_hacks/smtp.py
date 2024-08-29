import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = 'SMTP.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'quantaamail@gmail.com'
SMTP_PASSWORD = 'pnpo ffjq gfoh gujs'

def send_email(recipient_email, subject, body):
    
    sender_email = 'quantaamail@gmail.com'
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
        server.login(SMTP_USER, SMTP_PASSWORD)  # Login to the SMTP server

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())

    
        server.quit()

        print(f"Email sent successfully to {recipient_email}")
        return True

    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
