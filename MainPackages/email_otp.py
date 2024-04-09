import random
import smtplib
from email.message import EmailMessage


def generateOTP(otp_size=6):
    final_otp = ""
    for i in range(otp_size):
        final_otp = final_otp + str(random.randint(0, 9))
    return final_otp


def sendEmailVerificationRequest(
    receiver,
    sender="ajeshrandam@gmail.com",
    custom_text="Hello, Your OTP is ",
    subject="Digival Solutions Registration ",
):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    google_app_password = "hehf ufkw qdpa dlnt"
    server.login(sender, google_app_password)
    cur_otp = generateOTP()

    msg = EmailMessage()
    msg.set_content(custom_text + cur_otp)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver
    server.send_message(msg)

    # msg = custom_text + cur_otp
    # server.sendmail(sender, receiver, msg)
    # server.sendmail()
    server.quit()
    return cur_otp
