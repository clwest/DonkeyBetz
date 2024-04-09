import smtplib

def send_email(subject, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("your_email", "your_password")
    msg = f"Subject: {subject}\n\n{message}"
    server.sendmail("from_email", "to_email", msg)
    server.quit()
