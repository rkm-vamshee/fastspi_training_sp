from email.mime.text import MIMEText
import random
import smtplib


def generateOtp():
    return str(random.randint(100000, 9999999))


def sendEmailForOtp(toEmail: str, otp: str):

    msg = MIMEText(f"Your OTP is: {otp}")
    msg["Subject"] = "Email Verification OTP"
    msg["From"] = "noreply@yourapp.com"
    msg["To"] = toEmail

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    # server.login("your_email@gmail.com", "APP_PASSWORD")
    server.login("TestingEmailID", "dfgdfg")
    server.send_message(msg)
    server.quit()
    
    
    
